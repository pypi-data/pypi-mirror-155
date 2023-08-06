"""
Module containing the Population grid class object.

Here all the functionality of a Population object is defined.

TODO: the save_snapshots and save_snapshot, are they actually distinct?

Tasks:
    - TODO: add functionality to 'on-init' set arguments
    - TODO: add functionality to return the initial_abundance_hash
    - TODO: add functionality to return the isotope_hash
    - TODO: add functionality to return the isotope_list
    - TODO: add functionality to return the nuclear_mass_hash
    - TODO: add functionality to return the nuclear_mass_list
    - TODO: add functionality to return the source_list
    - TODO: add functionality to return the ensemble_list
    - TODO: consider spreading the functions over more files.
    - TODO: type the private functions
    - TODO: fix the correct object types for the default values of the bse_options
    - TODO: think of a clean and nice way to unload and remove the custom_logging_info library from memory (and from disk)
    - TODO: think of a nice way to remove the loaded grid_code/ generator from memory.

TODO: Some of the methods that we have defined in the (mixin) class are designed to be used as a portal to information (return_binary_c_version_info for example.) THe current design is that they are all instance methods, but that is not always necessary. We can decorate them with @staticmethod, or @classmethod to make it easier to use them (https://realpython.com/instance-class-and-static-methods-demystified/)
"""

import os
import gc
import sys
import time
import copy
import json
import uuid
import queue
import signal
import datetime
import functools
import traceback
import multiprocessing

from collections import (
    OrderedDict,
)
from collections.abc import Iterable  # drop `.abc` with Python 2.7 or lower
from typing import Union, Any

import psutil
import setproctitle
import str2bool
from colorama import init as colorama_init

from binarycpython.utils.functions import (
    check_if_in_shell,
    filter_arg_dict,
    get_ANSI_colours,
    get_defaults,
    get_help_all,
    mem_use,
    timedelta,
    now,
)
from binarycpython.utils.ensemble import (
    binaryc_json_serializer,
    extract_ensemble_json_from_string,
    format_ensemble_results,
)
from binarycpython.utils.dicts import (
    AutoVivificationDict,
    merge_dicts,
    keys_to_floats,
)

from binarycpython.utils.population_extensions.analytics import analytics
from binarycpython.utils.population_extensions.cache import cache
from binarycpython.utils.population_extensions.dataIO import dataIO
from binarycpython.utils.population_extensions.distribution_functions import (
    distribution_functions,
)
from binarycpython.utils.population_extensions.grid_logging import grid_logging
from binarycpython.utils.population_extensions.grid_options_defaults import (
    grid_options_defaults,
)
from binarycpython.utils.population_extensions.gridcode import gridcode
from binarycpython.utils.population_extensions.HPC import HPC
from binarycpython.utils.population_extensions.metadata import metadata
from binarycpython.utils.population_extensions.Moe_di_Stefano_2017 import (
    Moe_di_Stefano_2017,
)
from binarycpython.utils.population_extensions.spacing_functions import (
    spacing_functions,
)
from binarycpython.utils.population_extensions.version_info import version_info

from binarycpython import _binary_c_bindings

# Initialise the colorama stuff
colorama_init()


class Population(
    analytics,
    cache,
    dataIO,
    distribution_functions,
    grid_logging,
    grid_options_defaults,
    gridcode,
    HPC,
    metadata,
    Moe_di_Stefano_2017,
    spacing_functions,
    version_info,
):
    """
    Population Object. Contains all the necessary functions to set up, run and process a
    population of systems
    """

    def __init__(self, **kwargs):
        """
        Initialisation function of the population class
        """

        # Initialise the parent classes
        analytics.__init__(self)
        cache.__init__(self)
        dataIO.__init__(self)
        distribution_functions.__init__(self)
        grid_logging.__init__(self)
        grid_options_defaults.__init__(self)
        gridcode.__init__(self)
        HPC.__init__(self)
        metadata.__init__(self)
        Moe_di_Stefano_2017.__init__(self)
        spacing_functions.__init__(self)
        version_info.__init__(self)

        # caches
        self.caches = {}
        self.cached_function_cache = {}
        self.original_function_cache = {}

        # Different sections of options
        # get binary_c defaults and create a cleaned up dict
        # Setting stuff will check against the defaults to see if the input is correct.
        self.defaults = get_defaults()
        self.cleaned_up_defaults = self._cleanup_defaults()
        self.available_keys = list(self.defaults.keys())
        self.special_params = [
            el for el in list(self.defaults.keys()) if el.endswith("%d")
        ]
        self.preloaded_population = None
        self.signal_count = {}

        # make the input dictionary
        self.bse_options = {}  # bse_options is just empty.

        # Grid options
        self.grid_options = copy.deepcopy(self.get_grid_options_defaults_dict())

        # Custom options
        # TODO: is this really necessary here? The custom options should be empty on start i think
        self.custom_options = {
            "save_snapshot": False,
        }

        # grid code generation
        self.indent_depth = 0
        self.indent_string = "    "
        self.code_string = ""

        # cached value of minimum stellar mass
        self._minimum_stellar_mass = None

        # logging levels
        self._LOGGER_VERBOSITY_LEVEL = 1
        self._CUSTOM_LOGGING_VERBOSITY_LEVEL = 2

        # Set the options that are passed at creation of the object
        self.set(**kwargs)

        # Load Moe and di Stefano options
        self.grid_options["Moe2017_options"] = copy.deepcopy(
            self.get_Moe_di_Stefano_2017_default_options()
        )

        # Write MOE2017 options to a file. NOTE: (david) not sure why i put this here anymore
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "moe_distefano"), exist_ok=True
        )
        with self.open(
            os.path.join(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                "moeopts.dat",
            ),
            "w",
        ) as f:
            json.dump(
                self.grid_options["Moe2017_options"], f, indent=4, ensure_ascii=False
            )

        # Argline dict
        self.argline_dict = {}

        # Set some memory dicts
        self.persistent_data_memory_dict = {}

        # shared memory used for logging
        self.shared_memory = {}

        # variable to test if we're running in a shell
        self.in_shell = check_if_in_shell()

        # ANSI colours: use them if in a shell
        self.ANSI_colours = get_ANSI_colours()
        if self.in_shell is False:
            for c in self.ANSI_colours:
                self.ANSI_colours[c] = ""

        # Set global (OS) process id
        self.grid_options["_main_pid"] = os.getpid()

        # local process ID
        self.process_ID = 0

        # Create location to store results. Users should write to this dictionary.
        # The AutoVivificationDict allows for Perl-like addition of possibly
        # non-existant subdicts.
        self.grid_results = AutoVivificationDict()

        # Create grid ensemble data location
        self.grid_ensemble_results = self._new_grid_ensemble_results()

        # add metadata
        self.add_system_metadata()

        # set up function cache.
        # NOTE: (david) I added this here to be able to test the distributions functions without actually running anything.
        self.setup_function_cache()

    def jobID(self):
        """
        Function to return the job ID number of this process as a string.

        Normal processes return their process ID (PID)
        HPC processes return whatever HPC_jobID() gives.
        """
        if self.HPC_job():
            jobID = self.HPC_jobID()
            if not jobID:
                # fallback: use process ID but with "HPC" prepended
                # (this should never happen!)
                jobID = "HPC{}".format(self.process_ID)
        else:
            jobID = "{}".format(self.process_ID)
        return jobID

    def exit(self, code=None, message=True, flush=True, stacktrace=False):
        """
        Exit function: use this to exit from a Population object.
        Really it's just a wrapper for sys.exit() to return the correct exit code,
        but also to post a message (if message is True, default is True)
        and perhaps a stacktrace (if stacktrace is True, default is False).
        """
        # if we've been killed, set exit code to 1
        if self.grid_options["exit_code"] == 0 and self.grid_options["_killed"]:
            self.grid_options["exit_code"] = 1
        # but override with code passed in
        if code:
            self.grid_options["exit_code"] = code
        if message:
            print(
                "exit from binary_c-python Population with code {}".format(
                    self.grid_options["exit_code"]
                )
            )
        if flush:
            sys.stdout.flush()
        if stacktrace or self.grid_options["print_stack_on_exit"]:
            traceback.print_stack()
        sys.exit(self.grid_options["exit_code"])

    ###################################################
    # Argument functions
    ###################################################

    # General flow of generating the arguments for the binary_c call:
    # - user provides parameter and value via set (or manually but that is risky)
    # - The parameter names of these input get compared to the parameter names in the self.defaults;
    #    with this, we know that its a valid parameter to give to binary_c.
    # - For a single system, the bse_options will be written as a arg line
    # - For a population the bse_options will get copied to a temp_bse_options dict and updated with
    #   all the parameters generated by the grid

    # I will not create the argument line by fully writing all the defaults and overriding user
    # input, that seems not necessary because by using the get_defaults() function we already
    # know for sure which parameter names are valid for the binary_c version
    # And because binary_c uses internal defaults, its not necessary to explicitly pass them.
    # I do however suggest everyone to export the binary_c defaults to a file, so that you know
    # exactly which values were the defaults.

    def set(self, **kwargs) -> None:
        """
        Function to set the values of the population. This is the preferred method to set values
        of functions, as it provides checks on the input.

        the bse_options will get populated with all the those that have a key that is present
        in the self.defaults

        the grid_options will get updated with all the those that have a key that is present
        in the self.grid_options

        If neither of above is met; the key and the value get stored in a custom_options dict.

        Args:
            via kwargs all the arguments are either set to binary_c parameters, grid_options or custom_options (see above)
        """

        # Go over all the input
        for key in kwargs:
            # Filter out keys for the bse_options
            if key in self.defaults:
                self.verbose_print(
                    "adding: {}={} to BSE_options".format(key, kwargs[key]),
                    self.grid_options["verbosity"],
                    2,
                )
                self.bse_options[key] = kwargs[key]

            # Extra check to check if the key fits one of parameter names that end with %d
            # TODO: abstract this function
            elif any(
                bool(key.startswith(param[:-2]) and len(param[:-2]) < len(key))
                for param in self.special_params
            ):
                self.verbose_print(
                    "adding: {}={} to BSE_options by catching the %d".format(
                        key, kwargs[key]
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
                self.bse_options[key] = kwargs[key]

            # Filter out keys for the grid_options
            elif key in self.grid_options.keys():
                self.verbose_print(
                    "adding: {}={} to grid_options".format(key, kwargs[key]),
                    self.grid_options["verbosity"],
                    1,
                )
                self.grid_options[key] = kwargs[key]

            # The of the keys go into a custom_options dict
            else:
                self.verbose_print(
                    "<<<< Warning: Key does not match previously known parameter: \
                    adding: {}={} to custom_options >>>>".format(
                        key, kwargs[key]
                    ),
                    self.grid_options["verbosity"],
                    0,  # NOTE: setting this to be 0 prevents mistakes being overlooked.
                )
                self.custom_options[key] = kwargs[key]

    def parse_cmdline(self) -> None:
        """
        Function to handle settings values via the command line in the form x=y, w=z, etc.

        Best to be called after all the .set(..) lines, and just before the .evolve() is called

        If you input any known parameter (i.e. contained in grid_options, defaults/bse_options
        or custom_options), this function will attempt to convert the input from string
        (because everything is string) to the type of the value that option had before.

        The values of the bse_options are initially all strings, but after user input they
        can change to ints.

        The value of any new parameter (which will go to custom_options) will be a string.
        """

        # get the cmd-line args in the form x=y
        cmdline_args = sys.argv[1:]

        if cmdline_args:
            self.verbose_print(
                "Found cmdline args. Parsing them now",
                self.grid_options["verbosity"],
                1,
            )

            # Grab the input and split them up, while accepting only non-empty entries
            # cmdline_args = args
            self.grid_options["_commandline_input"] = cmdline_args

            # Make dict and fill it
            cmdline_dict = {}
            for cmdline_arg in cmdline_args:
                split = cmdline_arg.split("=")

                if len(split) == 2:
                    parameter = split[0]
                    value = split[1]
                    old_value_found = False

                    # Find an old value
                    if parameter in self.grid_options:
                        old_value = self.grid_options[parameter]
                        old_value_found = True

                    elif parameter in self.custom_options:
                        old_value = self.custom_options[parameter]
                        old_value_found = True

                    elif parameter in self.bse_options:
                        old_value = self.bse_options[parameter]
                        old_value_found = True

                    elif parameter in self.defaults:
                        # this will revert to a string type, always
                        old_value = self.defaults[parameter]
                        old_value_found = True

                    # (attempt to) convert type
                    if old_value_found:
                        if old_value is not None:
                            try:
                                self.verbose_print(
                                    "Converting type of {} from {} to {}".format(
                                        parameter, type(value), type(old_value)
                                    ),
                                    self.grid_options["verbosity"],
                                    3,
                                )
                                try:
                                    if isinstance(old_value, bool):
                                        value = str2bool.str2bool(value)
                                    else:
                                        value = type(old_value)(value)
                                    self.verbose_print(
                                        "Success!", self.grid_options["verbosity"], 2
                                    )
                                except Exception as e:
                                    print(
                                        "Failed to convert {param} value with type {type}: old_value is '{old}', new value is '{new}', {e}".format(
                                            param=parameter,
                                            old=old_value,
                                            type=type(old_value),
                                            new=split[1],
                                            e=e,
                                        )
                                    )
                                    self.exit(code=1)

                            except ValueError:

                                # might be able to eval the parameter, e.g.
                                # an expression like "2-1" can eval to "1"
                                # which would be valid
                                try:
                                    evaled = eval(value)
                                    value = type(old_value)(evaled)
                                    self.verbose_print(
                                        "Success! (evaled)",
                                        self.grid_options["verbosity"],
                                        2,
                                    )

                                except ValueError:
                                    self.verbose_print(
                                        "Tried to convert the given parameter {}/value {} to its correct type {} (from old value {}). But that wasn't possible.".format(
                                            parameter, value, type(old_value), old_value
                                        ),
                                        self.grid_options["verbosity"],
                                        0,
                                    )
                    # Add to dict
                    self.verbose_print(
                        "setting {} = {} ".format(parameter, value),
                        self.grid_options["verbosity"],
                        3,
                    )
                    cmdline_dict[parameter] = value

                else:
                    print(
                        "Error: I do not know how to process",
                        cmdline_arg,
                        " : cmdline args should be in the format x=y, yours appears not to be.",
                    )
                    self.exit(1)

            # unpack the dictionary into the setting function that handles where the values are set
            self.set(**cmdline_dict)

    def _return_argline(self, parameter_dict=None):
        """
        Function to create the string for the arg line from a parameter dict
        """

        if not parameter_dict:
            parameter_dict = self.bse_options

        argline = "binary_c "

        for param_name in sorted(parameter_dict):
            argline += "{} {} ".format(param_name, parameter_dict[param_name])
        argline = argline.strip()

        return argline

    ###################################################
    # Return functions
    ###################################################

    def return_population_settings(self) -> dict:
        """
        Function that returns all the options that have been set.

        Can be combined with JSON to make a nice file.

        Returns:
            dictionary containing "bse_options", "grid_options", "custom_options"
        """
        options = {
            "bse_options": self.bse_options,
            "grid_options": self.grid_options,
            "custom_options": self.custom_options,
        }

        return options

    def return_binary_c_defaults(self):
        """
        Function that returns the defaults of the binary_c version that is used.
        """

        return self.defaults

    def return_all_info(
        self,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
    ) -> dict:
        """
        Function that returns all the information about the population and binary_c

        Args:
            include_population_settings:
                whether to include the population_settings (see function return_population_settings)
            include_binary_c_defaults:
                whether to include a dict containing the binary_c parameters and their default
                values
            include_binary_c_version_info:
                whether to include a dict containing all the binary_c version info
                (see return_binary_c_version_info)
            include_binary_c_help_all:
                whether to include a dict containing all the information about
                the binary_c parameters (see get_help_all)

        Return:
            dictionary containing all, or part of, the above dictionaries
        """

        #
        all_info = {}
        #
        if include_population_settings:
            population_settings = self.return_population_settings()
            all_info["population_settings"] = population_settings

        #
        if include_binary_c_defaults:
            binary_c_defaults = self.return_binary_c_defaults()
            all_info["binary_c_defaults"] = binary_c_defaults

        if include_binary_c_version_info:
            binary_c_version_info = self.return_binary_c_version_info(parsed=True)
            all_info["binary_c_version_info"] = binary_c_version_info

        if include_binary_c_help_all:
            binary_c_help_all_info = get_help_all(print_help=False)
            all_info["binary_c_help_all"] = binary_c_help_all_info

        return all_info

    def export_all_info(
        self,
        use_datadir: bool = True,
        outfile: Union[str, None] = None,
        include_population_settings: bool = True,
        include_binary_c_defaults: bool = True,
        include_binary_c_version_info: bool = True,
        include_binary_c_help_all: bool = True,
        ensure_ascii: str = False,
        indent: int = 4,
    ) -> Union[str, None]:
        """
        Function that exports the all_info to a JSON file

        Tasks:
            - TODO: Fix to write things to the directory. which options do which etc
            - TODO: there's flawed logic here. rewrite this part pls
            - TODO: consider actually just removing the whole 'output to file' part and let the
                user do this.

        Args:
            include_population_settings: whether to include the population_settings
                (see function return_population_settings)
            include_binary_c_defaults: whether to include a dict containing the binary_c parameters
                and their default values
            include_binary_c_version_info: whether to include a dict containing all the binary_c
                version info (see return_binary_c_version_info)
            include_binary_c_help_all: whether to include a dict containing all the information
                about the binary_c parameters (see get_help_all)
            use_datadir: Boolean whether to use the custom_options['data_dir'] to write the file to.
                If the  custom_options["base_filename"] is set, the output file will be called
                <custom_options["base_filename"]>_settings.json. Otherwise a file called
                simulation_<date+time>_settings.json will be created
            outfile: if use_datadir is false, a custom filename will be used
            ensure_ascii: the ensure_ascii flag passed to json.dump and/or json.dumps
                           (Default: False)
            indent: indentation passed to json.dump and/or json.dumps (default 4)
        """

        all_info = self.return_all_info(
            include_population_settings=include_population_settings,
            include_binary_c_defaults=include_binary_c_defaults,
            include_binary_c_version_info=include_binary_c_version_info,
            include_binary_c_help_all=include_binary_c_help_all,
        )

        # Copy dict
        all_info_cleaned = copy.deepcopy(all_info)

        if use_datadir:
            if self.custom_options.get("data_dir", None):
                if not self.custom_options.get("base_filename", None):
                    base_name = "simulation_{}".format(now(style="nospace"))
                else:
                    base_name = os.path.splitext(self.custom_options["base_filename"])[
                        0
                    ]

                # save settings as gzipped JSON
                settings_name = base_name + "_settings.json.gz"

                # Check directory, make if necessary
                os.makedirs(self.custom_options["data_dir"], exist_ok=True)

                settings_fullname = os.path.join(
                    self.custom_options["data_dir"], settings_name
                )

                print("ok")

                # open locked settings file, then output if we get the lock
                (f, lock) = self.locked_open_for_write(settings_fullname, vb=True)
                print("ok")

                if lock and f:
                    self.verbose_print(
                        "Writing settings to {}".format(settings_fullname),
                        self.grid_options["verbosity"],
                        1,
                    )
                    json.dump(
                        all_info_cleaned,
                        f,
                        indent=indent,
                        default=binaryc_json_serializer,
                        ensure_ascii=ensure_ascii,
                    )
                print("ok pre")
                self.locked_close(f, lock)
                print("ok ret")
                return settings_fullname

            # TODO: turn it around and have the exception be within the if statement
            msg = "Exporting all info without passing a value for `outfile` requires custom_options['data_dir'] to be present. That is not the cause. Either set the `data_dir` or pass a value for `outfile` "
            raise ValueError(msg)

        else:
            self.verbose_print(
                "Writing settings to {}".format(outfile),
                self.grid_options["verbosity"],
                1,
            )
            if not outfile.endswith("json"):
                self.verbose_print(
                    "Error: outfile ({}) must end with .json".format(outfile),
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

            with self.open(outfile, "w") as file:
                json.dump(
                    all_info_cleaned,
                    file,
                    indent=indent,
                    default=binaryc_json_serializer,
                    ensure_ascii=ensure_ascii,
                )
            return outfile

    ###################################################
    # Evolution functions
    ###################################################

    def _set_nprocesses(self):
        """
        Function to set the number of processes used in multiprocessing.

        If grid_options['num_cores'] <= 0, set automatically

        If grid_options['num_cores'] is 0, we use as many as we have available
        """
        # backwards compatibility
        if "amt_cores" in self.grid_options:
            self.grid_options["num_processes"] = self.grid_options["amt_cores"]
            self.grid_options["num_cores"] = self.grid_options["amt_cores"]

        if self.grid_options["num_cores"] == 0:
            # use all logical cores available to us
            self.grid_options["num_processes"] = max(1, psutil.cpu_count(logical=True))
        elif self.grid_options["num_cores"] == -1:
            # use all physical cores available to us
            self.grid_options["num_processes"] = max(1, psutil.cpu_count(logical=False))
        else:
            # manually specify number of cores made available
            self.grid_options["num_processes"] = self.grid_options["num_cores"]

    def _pre_run_setup(self) -> None:
        """
        Function to clean up some stuff in the grid before a run (like results, ensemble results etc)
        """

        # empty results
        self.grid_results = AutoVivificationDict()
        self.grid_ensemble_results = self._new_grid_ensemble_results()

        # set number of processes/cores we want to use
        self._set_nprocesses()

        # Reset the process ID (should not have a value initially, but can't hurt if it does)
        self.process_ID = 0

        # Reset population ID:
        self.grid_options["_population_id"] = uuid.uuid4().hex

        # save number of stored log stats
        self.shared_memory["n_saved_log_stats"] = multiprocessing.Value("i", 0)

        # set previous logging time
        _t = time.time()
        self.shared_memory["prev_log_time"] = multiprocessing.Array(
            "d", [_t] * self.grid_options["n_logging_stats"]
        )

        # set previous logging system number to 0
        self.shared_memory["prev_log_system_number"] = multiprocessing.Array(
            "i", [0] * self.grid_options["n_logging_stats"]
        )

        # arrays to store memory and max memory use per-thread
        mem = 1.0 * mem_use()
        for x in ["", "max_"]:
            self.shared_memory[x + "memory_use_per_thread"] = multiprocessing.Array(
                "d", [mem] * self.grid_options["num_processes"]
            )

        ############################################################
        # set and check default directory locations
        ############################################################

        # check tmp_dir exists
        if self.grid_options["tmp_dir"] is None or not os.path.isdir(
            self.grid_options["tmp_dir"]
        ):
            print(
                "grid_options['tmp_dir'] is not set or it is not a directory : this should point to a temporary directory location, preferably local to your CPUs"
            )
            self.exit(code=1)

        # check any HPC requirements are met
        if self.HPC_job() and not self.HPC_check_requirements()[0]:
            print(self.HPC_check_requirements()[1])
            self.exit(code=1)

        # default status_dir and cache_dir to be in tmp_dir
        #
        # NOTE: binary_c-python uses its own status_dir, which is not
        #       the same dir as HPC jobs use (so tmp_dir can be local
        #       to an HPC job, while the HPC status dir is common to
        #       all jobs)
        for x in ["status", "cache"]:
            if self.grid_options[x + "_dir"] is None:
                self.grid_options[x + "_dir"] = os.path.join(
                    self.grid_options["tmp_dir"], x
                )

        # make list of directories we want to use
        dirs = ["tmp_dir", "status_dir", "cache_dir"] + self.HPC_dirs()

        for dir in dirs:
            # try to make directories if they don't exist
            path = self.grid_options[dir]
            if path is not None:
                os.makedirs(path, exist_ok=True)

            # check directories exist and can be written to
            if path is not None and self.dir_ok(path) is False:
                print(
                    "Directory {dir} currently set to {path} cannot be written to. Please check that this directory is correct and you have write access.".format(
                        dir=dir, path=path
                    )
                )
                self.exit(code=1)

        # Make sure the subdirs of the tmp dir exist
        subdirs = [
            "failed_systems",
            "process_summary",
            "runtime_systems",
            "snapshots",
        ]
        for subdir in subdirs:
            path = os.path.join(self.grid_options["tmp_dir"], subdir)
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path) is False:
                print(
                    "Sub-Directory {subdir} (in tmp_dir) currently set to {path} cannot be written to. Please check that this directory is correct and you have write access.".format(
                        subdir=subdir, path=path
                    )
                )
                self.exit(code=1)

        # make sure the arg logging directory exists if we need it
        if self.grid_options["log_args"]:
            path = os.path.join(
                    self.grid_options["log_args_dir"]
                )
            os.makedirs(path, exist_ok=True)
            if self.dir_ok(path) is False:
                print(
                    "Failed to make directory at {log_args_dir} for output of system arguments. Please check that this directory is correct and you have write access.".format(
                        subdir=subdir, path=path
                    )
                )
                self.exit(code=1)

        # restore from existing HPC files
        self.HPC_restore()

        # set up function cache
        self.setup_function_cache()

        return

    def clean(self) -> None:
        """
        Clean the contents of the population object so it can be reused.

        Calling _pre_run_setup()

        TODO: decide to deprecate this function
        """

        self._pre_run_setup()

    def evolve(self) -> None:
        """
        Entry point function of the whole object. From here, based on the settings,
        we set up a grid and (probably) evolve the population.

        There are no direct arguments to this function, the grid_options
        contain all the relevant settings.

        Returns:
               a dictionary containing the analytics of the run.
        """

        # Just to make sure we don't have stuff from a previous run hanging around
        self._pre_run_setup()

        if self.HPC_job():
            # run HPC grid: if this returns True, then exit immediately
            self.grid_options["symlink_latest_gridcode"] = False
            if self.HPC_grid():
                self.exit(code=0)

        if self.grid_options["evolution_type"] == "join":
            # join previously calculated data and return immediately
            self.HPC_join_previous()
            return

        # Execute population evolution subroutines
        self._evolve_population()

        # make analytics information
        analytics_dict = self.make_analytics_dict()

        if self.HPC_job():
            self.HPC_dump_status("HPC grid after analytics")

        if self.custom_options["save_snapshot"]:
            # we must save a snapshot, not the population object
            # ... also save the new starting point: this has to take into
            # account where we originally started, and that the modulo may
            # not be == 1.
            self.grid_options["start_at"] = (
                self.grid_options["start_at"]
                + self.grid_options["_count"] * self.grid_options["modulo"]
            )
            # then save the snapshot
            self.save_snapshot()
            exitcode = 1 if self.was_killed() else 0
            self.exit(code=exitcode)

        # Save object to a pickle file
        elif self.grid_options["save_population_object"]:
            self.save_population_object()

        # if we're running an HPC grid, exit here
        # unless we're joining
        if self.HPC_job() and self.grid_options["evolution_type"] != "join":
            self.exit()

        ##
        # Clean up code: remove files, unset values, unload interpolators etc. This is placed in the general evolve function,
        # because that makes for easier control
        self._cleanup()

        return analytics_dict

    def _evolve_population(self):
        """
        Function to evolve populations. This handles the setting up, evolving
        and cleaning up of a population of stars.

        Choices here are:
            to evolve a population via multiprocessing or linearly on 1 core.
            NOT IMPLEMENTED YET to evolve a population via a variable grid, a source file or MC

        Tasks:
            - TODO: include options for different ways of generating a population here. (i.e. MC or source file)
        """

        ############################################################
        # Prepare code/initialise grid.
        # set custom logging, set up store_memaddr, build grid code. dry run grid code.
        if self._setup() is False:
            return

        ############################################################
        # Evolve systems
        self.set_time("start")
        if (
            self.grid_options["evolution_type"]
            in self.grid_options["_evolution_type_options"]
        ):
            if self.grid_options["evolution_type"] in ["grid", "custom_generator"]:
                self._evolve_population_grid()

            # elif self.grid_options["evolution_type"] == "mc":
            #     # TODO: add MC option
        else:
            print(
                "Warning. you chose a wrong option for the grid evolution types.\
                Please choose from the following: {}.".format(
                    self.grid_options["_evolution_type_options"]
                )
            )
        self.set_time("end")

        ############################################################
        # Log and print some information
        string1 = "Population-{} finished!\nThe total probability is {:g}.".format(
            self.grid_options["_population_id"], self.grid_options["_probtot"]
        )
        string2 = "It took a total of {dtsecs} to run {starcount} systems on {ncores} cores\n = {CPUtime} of CPU time.\nMaximum memory use {memuse:.3f} MB".format(
            dtsecs=timedelta(self.grid_options["_time_elapsed"]),
            starcount=self.grid_options[
                "_count"
            ],  # not _total_count! we may have ended the run early...
            ncores=self.grid_options["num_processes"],
            CPUtime=timedelta(self.CPU_time()),
            memuse=sum(self.shared_memory["max_memory_use_per_thread"]),
        )

        ############################################################
        # add warning about a grid that was killed
        ############################################################
        if self.was_killed():
            string2 += "\n>>> Grid was killed <<<"
            self.set_status("killed")

        self.verbose_print(
            self._boxed(string1, string2), self.grid_options["verbosity"], 0
        )

        ############################################################
        # handle errors
        ############################################################
        if self.grid_options["_errors_found"]:
            # Some information afterwards
            self.verbose_print(
                self._boxed(
                    "During the run {} failed systems were found\nwith a total probability of {:g}\nwith the following unique error codes: {} ".format(
                        self.grid_options["_failed_count"],
                        self.grid_options["_failed_prob"],
                        self.grid_options["_failed_systems_error_codes"],
                    )
                ),
                self.grid_options["verbosity"],
                0,
            )
            # Some information afterwards
            self.verbose_print(
                "The full argline commands for {} these systems have been written to {}".format(
                    "ALL"
                    if not self.grid_options["_errors_exceeded"]
                    else "SOME (only the first ones, as there were too many to log all of them)",
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "failed_systems_{}_X.txt".format(
                            self.grid_options["_population_id"]
                        ),
                    ),
                ),
                self.grid_options["verbosity"],
                0,
            )
        else:
            self.verbose_print(
                "No failed systems were found in this run.",
                self.grid_options["verbosity"],
                0,
            )

        return

    def _system_queue_filler(self, job_queue, num_processes):
        """
        Function that is responsible for keeping the queue filled.

        This will generate the systems until it is full, and then keeps trying to fill it.
        Will have to play with the size of this.

        This function is called as part of the parent process.
        """

        stream_logger = self._get_stream_logger()
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"setting up the system_queue_filler now")

        # Setup of the generator
        # Check again if we use custom generator or not:
        if self.grid_options["evolution_type"] == "custom_generator":
            generator = self.grid_options["custom_generator"]
        else:
            self._generate_grid_code(dry_run=False)

            self._load_grid_function()

            generator = self.grid_options["_system_generator"](
                self, print_results=False
            )

        # start_at can be an expression : we should eval it
        # prior to running the loop
        self.grid_options["start_at"] = eval(str(self.grid_options["start_at"]))
        if self.grid_options["start_at"] > 0:
            print("Starting at model {} ".format(self.grid_options["start_at"]))

        # Continuously fill the queue while we are allowed to
        for system_number, system_dict in enumerate(generator):
            if self.grid_options["stop_queue"]:
                break

            # skip systems before start_at
            elif system_number < self.grid_options["start_at"]:
                self.verbose_print(
                    "skip system {n} because < start_at = {start}".format(
                        n=system_number, start=self.grid_options["start_at"]
                    ),
                    self.grid_options["verbosity"],
                    3,
                )
                continue

            # apply modulo
            if not (
                (system_number - self.grid_options["start_at"])
                % self.grid_options["modulo"]
                == 0
            ):
                self.verbose_print(
                    "skip system {n} because modulo {mod} == {donemod}".format(
                        n=system_number,
                        mod=self.grid_options["modulo"],
                        donemod=(system_number - self.grid_options["start_at"])
                        % self.grid_options["modulo"],
                    ),
                    self.grid_options["verbosity"],
                    3,
                )

                continue

            # Put job in queue
            if self.grid_options["stop_queue"]:
                break
            else:
                try:
                    job_queue.put((system_number, system_dict), block=True)
                except Exception as e:
                    # error on queueing : stop the queue
                    self.grid_options["stop_queue"] = True

                # Print some info
                self.verbose_print(
                    "Queue produced system {}".format(system_number),
                    self.grid_options["verbosity"],
                    3,
                )

        self.grid_options["_queue_done"] = True

        # Send closing signal to workers. When they receive this they will terminate
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Signalling processes to stop")  # DEBUG

        if True:  # not self.grid_options['stop_queue']:
            for _ in range(num_processes):
                job_queue.put("STOP")

    def _evolve_population_grid(self):
        """
        Function that handles running the population using multiprocessing.

        First we set up the multiprocessing manager and the job and result queue.

        Then we spawn <self.grid_options["num_processes"]> number of process instances,
        and signal them to start.

        While the processes are waiting for their instructions, we start the queue filler,
        which goes over the grid code and puts all the tasks in a queue until its full.

        The processes take these jobs, evolve the and store results.

        When all the systems have been put in the queue we pass a STOP signal
        that will make the processes wrap up.

        We then add any previous population

        We read out the information in the result queue and store them in the grid object
        """

        # Set process name
        setproctitle.setproctitle("binarycpython parent process")

        # if max_queue_size is zero, calculate automatically
        # to be double the number of processes - you don't want to
        # make the queue too large because when it's killed you
        # want to end quickly
        if self.grid_options["max_queue_size"] == 0:
            self.grid_options["max_queue_size"] = 2 * self.grid_options["num_processes"]

        # Set up the manager object that can share info between processes
        manager = multiprocessing.Manager()
        job_queue = manager.Queue(maxsize=self.grid_options["max_queue_size"])
        result_queue = manager.Queue(maxsize=self.grid_options["num_processes"])

        # data to be sent to signal handlers
        signal_data = {
            "where": "_evolve_population_grid",
            "queue": job_queue,
        }

        # Create process instances to run the stars
        processes = []
        for ID in range(self.grid_options["num_processes"]):
            processes.append(
                multiprocessing.Process(
                    target=self._process_run_population_grid,
                    args=(job_queue, result_queue, ID),
                )
            )

        # Activate the processes
        for p in processes:
            p.start()

        # activate signal handlers
        # * the child processes ignore these signals
        # * the parent will be in _system_queue_filler when these are caught
        signal.signal(
            signal.SIGTERM, functools.partial(self._parent_signal_handler, signal_data)
        )
        signal.signal(
            signal.SIGINT, functools.partial(self._parent_signal_handler, signal_data)
        )

        # Set up the system_queue in the parent process
        self._system_queue_filler(
            job_queue, num_processes=self.grid_options["num_processes"]
        )

        # Join the processes
        print("Do join of subprocesses ...")
        for p in processes:
            p.join()
        print("Joined subprocesses.")

        # todo: error codes

        # Handle the results by merging all the dictionaries. How that merging happens exactly is
        # described in the merge_dicts description.
        #
        # If there is a preloaded_population, we add this first,
        # then we add the populations run just now

        # 1)
        # use preloaded population's data as a basis
        # for our combined_output_dict
        if self.preloaded_population:
            combined_output_dict = {
                "ensemble_results": keys_to_floats(
                    self.preloaded_population.grid_ensemble_results
                ),
                "results": keys_to_floats(self.preloaded_population.grid_results),
            }

            for x in self._metadata_keylist():
                try:
                    combined_output_dict[x] = self.preloaded_population.grid_options[x]
                except Exception as e:
                    print(
                        "Tried to set combined_output_dict key",
                        x,
                        "from preloaded_popuation, but this failed:",
                        e,
                    )
            print(
                "Pre-loaded data from {} stars".format(combined_output_dict["_count"])
            )

            # do not propagate _killed
            # combined_output_dict['results']['_killed'] = False
            # combined_output_dict['_killed'] = False

            self.preloaded_population = None
            gc.collect()
        else:
            # new empty combined output
            combined_output_dict = OrderedDict()
            combined_output_dict["ensemble_results"] = OrderedDict()
            combined_output_dict["results"] = OrderedDict()

        # 2)
        # combine the dicts that were output from our
        # subprocesses
        sentinel = object()
        for output_dict in iter(result_queue.get, sentinel):
            if output_dict:
                # don't let Xinit be added
                if (
                    "ensemble_results" in combined_output_dict
                    and "ensemble" in combined_output_dict["ensemble_results"]
                    and "Xinit" in combined_output_dict["ensemble_results"]["ensemble"]
                ):
                    del combined_output_dict["ensemble_results"]["ensemble"]["Xinit"]

                # merge dicts
                combined_output_dict = merge_dicts(
                    combined_output_dict, keys_to_floats(output_dict)
                )
            if result_queue.empty():
                break

        # Extra ensemble result manipulation:
        if "ensemble_results" in combined_output_dict:
            combined_output_dict["ensemble_results"][
                "ensemble"
            ] = format_ensemble_results(
                combined_output_dict["ensemble_results"].get("ensemble", {})
            )
        gc.collect()

        # Put the values back as object properties
        self.grid_results = combined_output_dict["results"]

        #################################
        # Put Ensemble results
        self.grid_ensemble_results = combined_output_dict[
            "ensemble_results"
        ]  # Ensemble results are also passed as output from that dictionary

        # Add metadata
        self.add_ensemble_metadata(combined_output_dict)

        # if we were killed, save snapshot
        if self.grid_options["save_snapshots"] and self.grid_options["_killed"]:
            self.custom_options["save_snapshot"] = True

    def _evolve_system_mp(self, full_system_dict):
        """
        Function that the multiprocessing evolution method calls to evolve a system

        this function is called by _process_run_population_grid
        """

        binary_cmdline_string = self._return_argline(full_system_dict)

        persistent_data_memaddr = -1
        if self.bse_options.get("ensemble", 0) == 1:
            persistent_data_memaddr = self.persistent_data_memory_dict[self.process_ID]
            # print("thread {}: persistent_data_memaddr: ".format(self.process_ID), persistent_data_memaddr)

        # vb2 logging
        if self.grid_options["verbosity"] >= 2:
            self.vb2print(full_system_dict, binary_cmdline_string)

        # Get results binary_c
        # print("running: {}".format(binary_cmdline_string))
        out = _binary_c_bindings.run_system(
            argstring=binary_cmdline_string,
            custom_logging_func_memaddr=self.grid_options[
                "custom_logging_func_memaddr"
            ],
            store_memaddr=self.grid_options["_store_memaddr"],
            population=1,  # since this system is part of a population, we set this flag to prevent the store from being freed
            persistent_data_memaddr=persistent_data_memaddr,
        )

        # Check for errors
        _ = self._check_binary_c_error(out, full_system_dict)

        # Have some user-defined function do stuff with the data.
        if self.grid_options["parse_function"]:
            self.custom_options["parameter_dict"] = full_system_dict
            self.grid_options["parse_function"](self, out)

        return

    def _parent_signal_handler(self, signal_data, signum, frame):
        """
        Signal handling function for the parent process.
        """

        # this function is called by both queues when they
        # catch a signal
        sigstring = signal.Signals(signum).name

        if sigstring in self.signal_count:
            self.signal_count[sigstring] += 1
        else:
            self.signal_count[sigstring] = 1

        if self.signal_count[sigstring] > 3:
            print("caught > 3 times : exit")
            self.exit(code=2)

        # tell the user what has happened
        print(
            "Parent signal {} caught (count {}) handler set in {} [ keys {} ]".format(
                sigstring,
                self.signal_count[sigstring],
                signal_data["where"],
                ",".join(signal_data.keys()),
            )
        )

        # set status files
        self.set_status("signal {sig}".format(sig=sigstring))

        if signum == signal.SIGINT:
            # caught SIGINT: e.g. CTRL-C or HPC job manager
            # shutting us down
            print("Parent set stop_queue to True")
            self.grid_options["stop_queue"] = True
            self.custom_options["save_snapshot"] = True
            self.grid_options["_killed"] = True
            return
        else:
            # what to do?
            return

    def _child_signal_handler(self, signal_data, signum, frame):
        """
        Signal handler for child processes.
        """
        sigstring = signal.Signals(signum).name

        if sigstring in self.signal_count:
            self.signal_count[sigstring] += 1
        else:
            self.signal_count[sigstring] = 1

        # if we receive the signal three times, exit
        if self.signal_count[sigstring] > 3:
            print("caught > 3 times : exit")
            self.exit(code=2)

        print(
            "Child signal {} caught (count {}) handler set in {} [ keys {} ]".format(
                sigstring,
                self.signal_count[sigstring],
                signal_data["where"],
                ",".join(signal_data.keys()),
            )
        )

        # SIGINT should stop the queue nicely
        if signum == signal.SIGINT:
            self.grid_options["stop_queue"] = True
            self.grid_options["_killed"] = True

        # propagate signal to parent
        os.kill(self.grid_options["_main_pid"], signum)

    def _process_run_population_grid(self, job_queue, result_queue, ID):
        """
        Worker process that gets items from the job_queue and runs those systems.
        It keeps track of several things like failed systems, total time spent on systems etc.

        Input:
            job_queue: Queue object containing system dicts
            result_queue: Queue where the resulting analytic dictionaries will be put in
            ID: id of the worker process

        """

        # ignore SIGINT and SIGTERM : these are
        # handled by our parent process (hence in
        # _evolve_population_grid)
        signal.signal(
            signal.SIGTERM,
            functools.partial(
                self._child_signal_handler, {"where": "_process_run_population_grid"}
            ),
        )
        signal.signal(
            signal.SIGINT,
            functools.partial(
                self._child_signal_handler, {"where": "_process_run_population_grid"}
            ),
        )

        # set start timer
        start_process_time = datetime.datetime.now()

        # set the process ID
        self.process_ID = ID

        stream_logger = self._get_stream_logger()
        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Setting up processor: process-{self.process_ID}")

        # Set the process names
        name_proc = "binarycpython population process {}".format(ID)
        setproctitle.setproctitle(name_proc)

        # Set to starting up
        self.set_status("starting")

        # lets try out making stores for all the grids:
        self.grid_options["_store_memaddr"] = _binary_c_bindings.return_store_memaddr()

        self.verbose_print(
            "Process {} started at {}.\tUsing store memaddr {}".format(
                ID,
                now(),
                self.grid_options["_store_memaddr"],
            ),
            self.grid_options["verbosity"],
            3,
        )

        # Set the ensemble memory address
        if self.bse_options.get("ensemble", 0) == 1:
            # set persistent data memory address if necessary.
            persistent_data_memaddr = (
                _binary_c_bindings.return_persistent_data_memaddr()
            )

            self.persistent_data_memory_dict = {
                self.process_ID: persistent_data_memaddr
            }

            self.verbose_print(
                "\tUsing persistent_data memaddr: {}".format(persistent_data_memaddr),
                self.grid_options["verbosity"],
                3,
            )

        # Set up local variables
        localcounter = (
            0  # global counter for the whole loop. (need to be ticked every loop)
        )
        probability_of_systems_run = (
            0  # counter for the probability of the actual systems this tread ran
        )
        number_of_systems_run = (
            0  # counter for the actual number of systems this thread ran
        )
        zero_prob_stars_skipped = 0
        total_time_calling_binary_c = 0
        total_mass_run = 0
        total_probability_weighted_mass_run = 0

        # variables for the statu bar prints
        start_grid_time = time.time()
        next_log_time = (
            self.shared_memory["prev_log_time"][0] + self.grid_options["log_dt"]
        )
        next_mem_update_time = start_grid_time + self.grid_options["log_dt"]

        # Set status to running
        self.set_status("running")

        ############################################################
        # Run stellar systems in the queue
        ############################################################
        for system_number, system_dict in iter(job_queue.get, "STOP"):

            if False:
                print(
                    "Child: Job Queue system_number = {}, dict={}, n={} check {}".format(
                        system_number,
                        system_dict,
                        number_of_systems_run,
                        self.grid_options["stop_queue"],
                    )
                )
                sys.stdout.flush()

            # Combine that with the other settings
            full_system_dict = self.bse_options.copy()
            full_system_dict.update(system_dict)

            # In the first system, explicitly check all the keys that are passed to see if
            # they match the keys known to binary_c.
            # Won't do that every system cause that is a bit of a waste of computing time.
            # TODO: check if we can rename the below var
            if number_of_systems_run == 0:
                # TODO: Put this someplace else and wrap in a function call
                for key in full_system_dict.keys():
                    if not key in self.available_keys:
                        # Deal with special keys
                        if not any(
                            [
                                True
                                if (
                                    key.startswith(param[:-2])
                                    and len(param[:-2]) < len(key)
                                )
                                else False
                                for param in self.special_params
                            ]
                        ):
                            msg = "Error: Found a parameter unknown to binary_c: {}. Abort".format(
                                key
                            )
                            raise ValueError(msg)

            ######################
            # Print status of runs
            # save the current time (used often)
            time_now = time.time()

            # update memory use stats every log_dt seconds (not every time, this is likely a bit expensive)
            if time_now > next_mem_update_time:
                m = mem_use()
                self.shared_memory["memory_use_per_thread"][ID] = m
                next_mem_update_time = time_now + self.grid_options["log_dt"]
                if m > self.shared_memory["max_memory_use_per_thread"][ID]:
                    self.shared_memory["max_memory_use_per_thread"][ID] = m

            # calculate the next logging time
            next_log_time = (
                self.shared_memory["prev_log_time"][0] + self.grid_options["log_dt"]
            )

            # Check if we need to log info again
            # TODO: Check if we can put this functionality elsewhere
            if time_now > next_log_time:
                # we have exceeded the next log time : output and update timers
                # Lock the threads. TODO: Do we need to release this?
                lock = multiprocessing.Lock()

                # Do the printing itself
                self.vb1print(ID, time_now, system_number, system_dict)

                # Set some values for next time
                next_log_time = time_now + self.grid_options["log_dt"]

                # print("PREV ",self.shared_memory["prev_log_time"])
                # print("N LOG STATS",self.shared_memory["n_saved_log_stats"].value)

                # shift the arrays
                self.shared_memory["prev_log_time"][
                    -(self.grid_options["n_logging_stats"] - 1) :
                ] = self.shared_memory["prev_log_time"][
                    : (self.grid_options["n_logging_stats"] - 1)
                ]
                self.shared_memory["prev_log_system_number"][
                    -(self.grid_options["n_logging_stats"] - 1) :
                ] = self.shared_memory["prev_log_system_number"][
                    : (self.grid_options["n_logging_stats"] - 1)
                ]

                # set the current time and system number
                self.shared_memory["prev_log_time"][0] = time_now
                self.shared_memory["prev_log_system_number"][0] = system_number

                # increase the number of stats
                self.shared_memory["n_saved_log_stats"].value = min(
                    self.shared_memory["n_saved_log_stats"].value + 1,
                    self.grid_options["n_logging_stats"],
                )

                # print("FIRST (0) ",self.shared_memory["prev_log_time"][0])
                # print("LAST (",self.shared_memory["n_saved_log_stats"].value-1,")",self.shared_memory["prev_log_time"][self.shared_memory["n_saved_log_stats"].value-1])

            ###############
            # Log current system info

            # In some cases, the whole run crashes. To be able to figure out which system
            # that was on, we log each current system to a file (each thread has one).
            # Each new system overrides the previous
            if self.grid_options["log_args"]:
                argfile = os.path.join(
                    self.grid_options["log_args_dir"],
                    "process_{}.txt".format(self.jobID()),
                )
                with self.open(
                        argfile,
                        "w",
                        encoding="utf-8",
                ) as f:
                    binary_c_cmdline_string = self._return_argline(full_system_dict)
                    f.write(binary_c_cmdline_string)
                    f.close()

            ##############
            # Running the system
            start_runtime_binary_c = time.time()

            # If we want to actually evolve the systems
            if self.grid_options["_actually_evolve_system"]:
                run_system = True

                # Check option to ignore 0 probability systems
                if not self.grid_options["run_zero_probability_system"]:
                    if full_system_dict.get("probability", 1) == 0:
                        run_system = False
                        zero_prob_stars_skipped += 1

                if run_system:
                    # Evolve the system
                    self._evolve_system_mp(full_system_dict)

            end_runtime_binary_c = time.time()

            total_time_calling_binary_c += (
                end_runtime_binary_c - start_runtime_binary_c
            )  # keep track of total binary_c call time

            ############
            # Logging runtime

            # Debug line: logging all the lines
            if self.grid_options["log_runtime_systems"] == 1:
                with self.open(
                    os.path.join(
                        self.grid_options["tmp_dir"],
                        "runtime_systems",
                        "process_{}.txt".format(self.process_ID),
                    ),
                    "a+",
                    encoding="utf-8",
                ) as f:
                    binary_cmdline_string = self._return_argline(full_system_dict)
                    f.write(
                        "{} {} '{}'\n".format(
                            start_runtime_binary_c,
                            end_runtime_binary_c - start_runtime_binary_c,
                            binary_cmdline_string,
                        )
                    )
                    f.close()

            ####################
            # Tallying system information

            # Keep track of systems:
            probability_of_systems_run += full_system_dict.get("probability", 1)
            number_of_systems_run += 1
            localcounter += 1

            # Tally up some numbers
            total_mass_system = (
                full_system_dict.get("M_1", 0)
                + full_system_dict.get("M_2", 0)
                + full_system_dict.get("M_3", 0)
                + full_system_dict.get("M_4", 0)
            )
            total_mass_run += total_mass_system
            total_probability_weighted_mass_run += (
                total_mass_system * full_system_dict.get("probability", 1)
            )

            if self.grid_options["stop_queue"]:
                print("Child: Stop queue at system {n}".format(n=number_of_systems_run))
                break

        if self.grid_options["stop_queue"]:
            # any remaining jobs should be ignored
            try:
                while True:
                    job_queue.get_nowait()
            except queue.Empty:
                pass

        # Set status to finishing
        self.set_status("finishing")

        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finishing.")

        ###########################
        # Handle ensemble outut

        # if ensemble==1, then either directly write that data to a file, or combine everything into 1 file.
        ensemble_json = {}  # Make sure it exists already
        if self.bse_options.get("ensemble", 0) == 1:
            self.verbose_print(
                "Process {}: is freeing ensemble output (using persistent_data memaddr {})".format(
                    ID, self.persistent_data_memory_dict[self.process_ID]
                ),
                self.grid_options["verbosity"],
                3,
            )

            ensemble_raw_output = (
                _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                    self.persistent_data_memory_dict[self.process_ID]
                )
            )

            if ensemble_raw_output is None:
                self.verbose_print(
                    "Process {}: Warning! Ensemble output is empty. ".format(ID),
                    self.grid_options["verbosity"],
                    1,
                )
                ensemble_output = None
            else:
                # convert ensemble_raw_output to a dictionary
                ensemble_output = extract_ensemble_json_from_string(ensemble_raw_output)

            # save the ensemble chunk to a file
            if (
                self.grid_options["save_ensemble_chunks"] is True
                or self.grid_options["combine_ensemble_with_thread_joining"] is False
            ):

                output_file = os.path.join(
                    self.custom_options["data_dir"],
                    "ensemble_output_{}_{}.json".format(
                        self.grid_options["_population_id"], self.process_ID
                    ),
                )
                self.verbose_print(
                    "Writing process {} JSON ensemble chunk output to {} ".format(
                        ID, output_file
                    ),
                    self.grid_options["verbosity"],
                    1,
                )

                ensemble_output = extract_ensemble_json_from_string(ensemble_raw_output)
                self.write_ensemble(output_file, ensemble_output)

            # combine ensemble chunks
            if self.grid_options["combine_ensemble_with_thread_joining"] is True:
                self.verbose_print(
                    "Process {}: Extracting ensemble info from raw string".format(ID),
                    self.grid_options["verbosity"],
                    1,
                )
                ensemble_json["ensemble"] = ensemble_output

        ##########################
        # Clean up and return
        self.verbose_print(
            "process {} free memory and return ".format(ID),
            self.grid_options["verbosity"],
            1,
        )
        # free store memory:
        _binary_c_bindings.free_store_memaddr(self.grid_options["_store_memaddr"])

        # Return a set of results and errors
        output_dict = {
            "results": self.grid_results,
            "ensemble_results": ensemble_json,
            "_failed_count": self.grid_options["_failed_count"],
            "_failed_prob": self.grid_options["_failed_prob"],
            "_failed_systems_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "_errors_exceeded": self.grid_options["_errors_exceeded"],
            "_errors_found": self.grid_options["_errors_found"],
            "_probtot": probability_of_systems_run,
            "_count": number_of_systems_run,
            "_total_mass_run": total_mass_run,
            "_total_probability_weighted_mass_run": total_probability_weighted_mass_run,
            "_zero_prob_stars_skipped": zero_prob_stars_skipped,
            "_killed": self.grid_options["_killed"],
        }

        end_process_time = datetime.datetime.now()

        killed = self.was_killed()

        # thread end message
        colour = "cyan on black"
        self.verbose_print(
            self._boxed(
                "{colour}Process {ID} finished:\ngenerator started at {start}\ngenerator finished at {end}\ntotal: {timesecs}\nof which {binary_c_secs} with binary_c\nRan {nsystems} systems\nwith a total probability of {psystems:g}\n{failcolour}This thread had {nfail} failing systems{colour}\n{failcolour}with a total failed probability of {pfail}{colour}\n{zerocolour}Skipped a total of {nzero} zero-probability systems{zeroreset}\n{failednotice}".format(
                    colour=self.ANSI_colours[colour],
                    ID=ID,
                    start=start_process_time.isoformat(),
                    end=end_process_time.isoformat(),
                    timesecs=timedelta(
                        (end_process_time - start_process_time).total_seconds()
                    ),
                    binary_c_secs=timedelta(total_time_calling_binary_c),
                    nsystems=number_of_systems_run,
                    psystems=probability_of_systems_run,
                    failcolour=self.ANSI_colours["red"]
                    if self.grid_options["_failed_count"] > 0
                    else "",
                    failreset=self.ANSI_colours[colour]
                    if self.grid_options["_failed_count"] > 0
                    else "",
                    nfail=self.grid_options["_failed_count"],
                    pfail=self.grid_options["_failed_prob"],
                    nzero=zero_prob_stars_skipped,
                    zerocolour=self.ANSI_colours["yellow"]
                    if zero_prob_stars_skipped > 0
                    else "",
                    zeroreset=self.ANSI_colours[colour]
                    if zero_prob_stars_skipped > 0
                    else "",
                    failednotice=">>> Process was killed <<<\n" if killed else "",
                ),
                colour=colour,
            ),
            self.grid_options["verbosity"],
            1,
        )

        # Write summary
        summary_dict = {
            "population_id": self.grid_options["_population_id"],
            "process_id": self.process_ID,
            "start_process_time": start_process_time.timestamp(),
            "end_process_time": end_process_time.timestamp(),
            "total_time_calling_binary_c": total_time_calling_binary_c,
            "number_of_systems_run": number_of_systems_run,
            "probability_of_systems_run": probability_of_systems_run,
            "failed_systems": self.grid_options["_failed_count"],
            "failed_probability": self.grid_options["_failed_prob"],
            "failed_system_error_codes": self.grid_options[
                "_failed_systems_error_codes"
            ],
            "zero_prob_stars_skipped": zero_prob_stars_skipped,
        }
        with self.open(
            os.path.join(
                self.grid_options["tmp_dir"],
                "process_summary",
                "process_{}.json".format(self.process_ID),
            ),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(summary_dict, f, indent=4, ensure_ascii=False)

        # Set status to finished
        if self.was_killed():
            self.set_status("killed")
        else:
            self.set_status("finished")

        self.verbose_print(
            "process {} queue put output_dict ".format(ID),
            self.grid_options["verbosity"],
            1,
        )

        result_queue.put(output_dict)

        if self.grid_options["verbosity"] >= self._LOGGER_VERBOSITY_LEVEL:
            stream_logger.debug(f"Process-{self.process_ID} is finished.")

        self.verbose_print(
            "process {} return ".format(ID),
            self.grid_options["verbosity"],
            1,
        )
        return

    # Single system
    def evolve_single(self, clean_up_custom_logging_files: bool = True) -> Any:
        """
        Function to run a single system, based on the settings in the grid_options

        The output of the run gets returned, unless a parse function is given to this function.

        Args:
            clean_up_custom_logging_files: whether the clean up all the custom_logging files.

        returns:
            either returns the raw binary_c output, or whatever the parse_function does
        """

        ### Custom logging code:
        self._set_custom_logging()

        # Check if there are actually arguments passed:
        if self.bse_options:

            # Get argument line and
            argline = self._return_argline(self.bse_options)

            self.verbose_print(
                "Running {}".format(argline), self.grid_options["verbosity"], 1
            )

            # Run system
            out = _binary_c_bindings.run_system(
                argstring=argline,
                custom_logging_func_memaddr=self.grid_options[
                    "custom_logging_func_memaddr"
                ],
                store_memaddr=self.grid_options["_store_memaddr"],
                population=0,
            )

            # Clean up custom logging
            if clean_up_custom_logging_files:
                self._clean_up_custom_logging(evol_type="single")

            # Parse output and return the result
            if self.grid_options["parse_function"]:
                return self.grid_options["parse_function"](self, out)

            # Otherwise just return the raw output
            return out

        else:
            msg = "No actual evolution options passed to the evolve call. Aborting"
            raise ValueError(msg)

    ############################################################
    def _setup(self):
        """
        Function to set up the necessary stuff for the population evolution.

        The idea is to do all the stuff that is necessary for a population to run.
        Since we have different methods of running a population, this setup function
        will do different things depending on different settings

        Returns:
        True if we want to continue.
        False if we should return to the original calling script.

        Tasks:
            TODO: Make other kinds of populations possible. i.e, read out type of grid,
                and set up accordingly
            TODO: make this function more general. Have it explicitly set the system_generator
                function
        """

        # Check for restore
        if self.grid_options["restore_from_snapshot_file"]:
            self.load_snapshot(self.grid_options["restore_from_snapshot_file"])

        # Check for parse function
        if not self.grid_options["parse_function"]:
            print("Warning: No parse function set. Make sure you intended to do this.")

        # #######################
        # ### Custom logging code:
        self._set_custom_logging()

        ### ensemble: make some checks for this
        ## check the settings and set all the warnings.
        if self.bse_options.get("ensemble", None):
            if not self.bse_options.get("ensemble_defer", 0) == 1:
                self.verbose_print(
                    "Error, if you want to run an ensemble in a population, the output needs to be deferred. Please set 'ensemble_defer' to 1",
                    self.grid_options["verbosity"],
                    0,
                )
                print("BSE",self.bse_options)
                raise ValueError

            if not any(
                [key.startswith("ensemble_filter_") for key in self.bse_options]
            ):
                self.verbose_print(
                    "Warning: Running the ensemble without any filter requires a lot of available RAM",
                    self.grid_options["verbosity"],
                    0,
                )

            if self.bse_options.get("ensemble_filters_off", 0) != 1:
                self.verbose_print(
                    "Warning: Running the ensemble without any filter requires a lot of available RAM",
                    self.grid_options["verbosity"],
                    0,
                )

            if self.grid_options["combine_ensemble_with_thread_joining"] == False:
                if not self.custom_options.get("data_dir", None):
                    self.verbose_print(
                        "Error: chosen to write the ensemble output directly to files but data_dir isn't set",
                        self.grid_options["verbosity"],
                        0,
                    )
                    raise ValueError

        # Unset some value
        self.grid_options["_probtot"] = 0

        ## Check which type of population generation
        # grid type
        if self.grid_options["evolution_type"] == "grid":
            ##################################################
            # Grid run
            ############################################################
            # Set up LRU cache
            self.setup_function_cache()

            ############################################################
            # Dry run and getting starcount
            ############################################################
            # Put in check
            if len(self.grid_options["_grid_variables"]) == 0:
                print("Error: you haven't defined any grid variables! Aborting")
                raise ValueError

            # Set up the grid code with a dry run option to see total probability
            print("Do dry run? {}".format(self.grid_options["do_dry_run"]))
            if self.grid_options["do_dry_run"]:
                print("Doing dry run to calculate total starcount and probability")
                self._generate_grid_code(dry_run=True)

                # Load the grid code
                self._load_grid_function()

                # Do a dry run
                self._dry_run()

                self.verbose_print(
                    self._boxed(
                        "Dry run",
                        "Total starcount is {starcount}".format(
                            starcount=self.grid_options["_total_starcount"]
                        ),
                        "Total probability is {probtot:g}".format(
                            probtot=self.grid_options["_probtot"]
                        ),
                    ),
                    self.grid_options["verbosity"],
                    0,
                )
                if self.grid_options["exit_after_dry_run"]:
                    print(
                        "Exiting after dry run {}".format(
                            self.grid_options["exit_after_dry_run"]
                        )
                    )
                    self.exit(code=0)
                elif self.grid_options["return_after_dry_run"]:
                    print(
                        "Returning after dry run {}".format(
                            self.grid_options["exit_after_dry_run"]
                        )
                    )
                    return False

            #######################
            # Reset values and prepare the grid function
            self.grid_options[
                "_probtot"
            ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way

            # # Making sure the loaded grid code isn't lingering in the main PID
            # self._generate_grid_code(dry_run=False)

            # #
            # self._load_grid_function()

            #
            self.grid_options["_system_generator"] = None

        # user-provided custom generator
        if self.grid_options["evolution_type"] == "custom_generator":
            if not isinstance(self.grid_options["custom_generator"], Iterable):
                print(
                    "Error. provided no or wrong custom value for the system generator (custom_generator: {})".format(
                        self.grid_options["custom_generator"]
                    )
                )
                raise ValueError

            # NOTE: In the part above i apparently have moved the load grid function call to another part. Now i wonder if that was useful, because it would be best if that is handled in this function
            # TODO: place the load grid function back to the part above

        # Source file
        elif self.grid_options["evolution_type"] == "source_file":
            # TODO: fix this function
            raise ValueError("This functionality is not available yet")

        # Monte-carlo
        elif self.grid_options["evolution_type"] == "montecarlo":
            if self.grid_options["do_dry_run"]:
                # Do a dry run
                self._dry_run_source_file()

            print(
                "Total starcount will be: {}".format(
                    self.grid_options["_total_starcount"]
                )
            )

            #######################
            # Reset values and prepare the grid function
            self.grid_options[
                "_probtot"
            ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way

            #
            # TODO: fix this function
            raise ValueError("This functionality is not available yet")

        #######################
        # Reset values and prepare the grid function
        self.grid_options[
            "_probtot"
        ] = 0  # To make sure that the values are reset. TODO: fix this in a cleaner way

        return True

    def _cleanup(self):
        """
        Function that handles all the cleaning up after the grid has been generated and/or run

        - reset values to 0
        - remove grid file
        - unload grid function/module
        - remove dry grid file
        - unload dry grid function/module
        """

        # Reset values
        for x in [
            "_count",
            "_probtot",
            "_failed_count",
            "_failed_prob",
            "_total_mass_run",
            "_total_probability_weighted_mass_run",
        ]:
            self.grid_options[x] = 0
        for x in ["_errors_found", "_errors_exceeded"]:
            self.grid_options[x] = False
        self.grid_options["_system_generator"] = None
        self.grid_options["_failed_systems_error_codes"] = []

    def _dry_run(self):
        """
        Function to dry run the grid and know how many stars it will run

        Requires the grid to be built as a dry run grid
        """
        self.verbose_print(
            "Doing a dry run of the grid.", self.grid_options["verbosity"], 1
        )
        system_generator = self.grid_options["_system_generator"]
        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    ###################################################
    # Population from file functions
    #
    # Functions below are used to run populations from
    # a file containing binary_c calls
    ###################################################
    def _dry_run_source_file(self):
        """
        Function to go through the source_file and count the number of lines and the total probability
        """

        system_generator = self.grid_options["_system_generator"]
        total_starcount = 0

        for _ in system_generator:
            total_starcount += 1

        total_starcount = system_generator(self)
        self.grid_options["_total_starcount"] = total_starcount

    def _load_source_file(self, check=False):
        """
        Function that loads the source_file that contains a binary_c calls
        """

        if not os.path.isfile(self.grid_options["source_file_filename"]):
            self.verbose_print(
                "Source file doesnt exist", self.grid_options["verbosity"], 0
            )

        self.verbose_print(
            message="Loading source file from {}".format(
                self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        # We can choose to perform a check on the source file, which checks if the lines start with 'binary_c'
        if check:
            source_file_check_filehandle = self.open(
                self.grid_options["source_file_filename"], "r", encoding="utf-8"
            )
            for line in source_file_check_filehandle:
                if not line.startswith("binary_c"):
                    failed = True
                    break
            if failed:
                self.verbose_print(
                    "Error, sourcefile contains lines that do not start with binary_c",
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError

        source_file_filehandle = self.open(
            self.grid_options["source_file_filename"], "r", encoding="utf-8"
        )

        self.grid_options["_system_generator"] = source_file_filehandle

        self.verbose_print("Source file loaded", self.grid_options["verbosity"], 1)

    def _dict_from_line_source_file(self, line):
        """
        Function that creates a dict from a binary_c arg line
        """
        if line.startswith("binary_c "):
            line = line.replace("binary_c ", "")

        split_line = line.split()
        arg_dict = {}

        for i in range(0, len(split_line), 2):
            if "." in split_line[i + 1]:
                arg_dict[split_line[i]] = float(split_line[i + 1])
            else:
                arg_dict[split_line[i]] = int(split_line[i + 1])

        return arg_dict

    ###################################################
    # Unordered functions
    #
    # Functions that aren't ordered yet
    ###################################################

    def _cleanup_defaults(self):
        """
        Function to clean up the default values:

        from a dictionary, removes the entries that have the following values:
        - "NULL"
        - ""
        - "Function"

        Uses the function from utils.functions

        TODO: Rethink this functionality. seems a bit double, could also be just outside of the class
        """

        binary_c_defaults = self.return_binary_c_defaults().copy()
        cleaned_dict = filter_arg_dict(binary_c_defaults)

        return cleaned_dict

    def _increment_probtot(self, prob):
        """
        Function to add to the total probability. For now not used
        """

        self.grid_options["_probtot"] += prob

    def _increment_count(self):
        """
        Function to add to the total number of stars. For now not used
        """
        self.grid_options["_count"] += 1

    def was_killed(self):
        """
        Function to determine if the process was killed. Returns True if so, false otherwise.
        """
        killed = self.grid_options["_killed"]

        if "_killed" in self.grid_ensemble_results.get("metadata", {}):
            killed = killed or self.grid_ensemble_results["metadata"]["_killed"]

        return killed

    def _check_binary_c_error(self, binary_c_output, system_dict):
        """
        Function to check whether binary_c throws an error and handle accordingly.
        """

        if binary_c_output:
            if (binary_c_output.splitlines()[0].startswith("SYSTEM_ERROR")) or (
                binary_c_output.splitlines()[-1].startswith("SYSTEM_ERROR")
            ):
                self.verbose_print(
                    "FAILING SYSTEM FOUND",
                    self.grid_options["verbosity"],
                    0,
                )

                # Keep track of the amount of failed systems and their error codes
                self.grid_options["_failed_prob"] += system_dict.get("probability", 1)
                self.grid_options["_failed_count"] += 1
                self.grid_options["_errors_found"] = True

                # Try catching the error code and keep track of the unique ones.
                try:
                    error_code = int(
                        binary_c_output.splitlines()[0]
                        .split("with error code")[-1]
                        .split(":")[0]
                        .strip()
                    )

                    if (
                        not error_code
                        in self.grid_options["_failed_systems_error_codes"]
                    ):
                        self.grid_options["_failed_systems_error_codes"].append(
                            error_code
                        )
                except ValueError:
                    self.verbose_print(
                        "Failed to extract the error-code",
                        self.grid_options["verbosity"],
                        1,
                    )

                # Check if we have exceeded the number of errors
                if (
                    self.grid_options["_failed_count"]
                    > self.grid_options["failed_systems_threshold"]
                ):
                    if not self.grid_options["_errors_exceeded"]:
                        self.verbose_print(
                            self._boxed(
                                "Process {} exceeded the maximum ({}) number of failing systems. Stopped logging them to files now".format(
                                    self.process_ID,
                                    self.grid_options["failed_systems_threshold"],
                                )
                            ),
                            self.grid_options["verbosity"],
                            1,
                        )
                        self.grid_options["_errors_exceeded"] = True

                # If not, write the failing systems to files unique to each process
                else:
                    # Write arg lines to file
                    argstring = self._return_argline(system_dict)
                    with self.open(
                        os.path.join(
                            self.grid_options["tmp_dir"],
                            "failed_systems",
                            "process_{}.txt".format(self.process_ID),
                        ),
                        "a+",
                        encoding="utf-8",
                    ) as f:
                        f.write(argstring + "\n")
                        f.close()
        else:
            self.verbose_print(
                "binary_c output nothing - this is strange. If there is ensemble output being generated then this is fine.",
                self.grid_options["verbosity"],
                3,
            )

    def _new_grid_ensemble_results(self):
        """
        Function to return a new grid_ensemble_results dict: this should
        be pre-filled by sub-dicts to prevent later errors.
        """
        return {
            'metadata' : {},
            'ensemble' : {}
        }
