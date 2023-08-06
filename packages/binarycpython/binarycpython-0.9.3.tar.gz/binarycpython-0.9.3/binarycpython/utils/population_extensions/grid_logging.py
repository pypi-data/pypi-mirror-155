"""
The class extension for the population object that contains logging functionality
"""

# pylint: disable=E1101

import os
import sys
import time
import logging
import strip_ansi

import binarycpython.utils.functions

from binarycpython.utils.functions import (
    format_number,
    trem,
    remove_file,
    verbose_print,
)
from binarycpython.utils.population_extensions.grid_options_defaults import secs_per_day

from binarycpython.utils.custom_logging_functions import (
    binary_c_log_code,
    create_and_load_logging_function,
    autogen_C_logging_code,
)


class grid_logging:
    """
    The class extension for the population object that contains logging functionality
    """

    def __init__(self, **kwargs):
        """
        Init function for the grid_logging class
        """

        return

    def _set_custom_logging(self):
        """
        Function/routine to set all the custom logging so that the function memory pointer
        is known to the grid.

        When the memory adress is loaded and the library file is set we'll skip rebuilding the library
        """

        # Only if the values are the 'default' unset values
        if (
            self.grid_options["custom_logging_func_memaddr"] == -1
            and self.grid_options["_custom_logging_shared_library_file"] is None
        ):
            self.verbose_print(
                "Creating and loading custom logging functionality",
                self.grid_options["verbosity"],
                1,
            )
            # C_logging_code gets priority of C_autogen_code
            if self.grid_options["C_logging_code"]:
                # Generate entire shared lib code around logging lines
                custom_logging_code = binary_c_log_code(
                    self.grid_options["C_logging_code"],
                    verbosity=self.grid_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Load memory address
                (
                    self.grid_options["custom_logging_func_memaddr"],
                    self.grid_options["_custom_logging_shared_library_file"],
                ) = create_and_load_logging_function(
                    custom_logging_code,
                    verbosity=self.grid_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                    custom_tmp_dir=self.grid_options["tmp_dir"],
                )

            elif self.grid_options["C_auto_logging"]:
                # Generate real logging code
                logging_line = autogen_C_logging_code(
                    self.grid_options["C_auto_logging"],
                    verbosity=self.grid_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Generate entire shared lib code around logging lines
                custom_logging_code = binary_c_log_code(
                    logging_line,
                    verbosity=self.grid_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                )

                # Load memory address
                (
                    self.grid_options["custom_logging_func_memaddr"],
                    self.grid_options["_custom_logging_shared_library_file"],
                ) = create_and_load_logging_function(
                    custom_logging_code,
                    verbosity=self.grid_options["verbosity"]
                    - (self._CUSTOM_LOGGING_VERBOSITY_LEVEL - 1),
                    custom_tmp_dir=self.grid_options["tmp_dir"],
                )
        else:
            self.verbose_print(
                "Custom logging library already loaded. Not setting them again.",
                self.grid_options["verbosity"],
                1,
            )

    def _print_info(self, run_number, total_systems, full_system_dict):
        """
        Function to print info about the current system and the progress of the grid.

        # color info tricks from https://ozzmaker.com/add-colour-to-text-in-python/
        https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
        """

        # Define frequency
        if self.grid_options["verbosity"] == 1:
            print_freq = 1
        else:
            print_freq = 10

        if run_number % print_freq == 0:
            binary_cmdline_string = self._return_argline(full_system_dict)
            info_string = "{color_part_1} \
            {text_part_1}{end_part_1}{color_part_2} \
            {text_part_2}{end_part_2}".format(
                color_part_1="\033[1;32;41m",
                text_part_1="{}/{}".format(run_number, total_systems),
                end_part_1="\033[0m",
                color_part_2="\033[1;32;42m",
                text_part_2="{}".format(binary_cmdline_string),
                end_part_2="\033[0m",
            )
            print(info_string)

    def _set_loggers(self):
        """
        Function to set the loggers for the execution of the grid
        """

        # Set log file
        binary_c_logfile = self.grid_options["log_file"]

        # Create directory
        os.makedirs(os.path.dirname(binary_c_logfile), exist_ok=True)

        # Set up logger
        self.logger = logging.getLogger("binary_c_python_logger")
        self.logger.setLevel(self.grid_options["verbosity"])

        # Reset handlers
        self.logger.handlers = []

        # Set formatting of output
        log_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Make and add file handlers
        # make handler for output to file
        handler_file = logging.FileHandler(filename=os.path.join(binary_c_logfile))
        handler_file.setFormatter(log_formatter)
        handler_file.setLevel(logging.INFO)

        # Make handler for output to stdout
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setFormatter(log_formatter)
        handler_stdout.setLevel(logging.INFO)

        # Add the loggers
        self.logger.addHandler(handler_file)
        self.logger.addHandler(handler_stdout)

    ######################
    # Status logging

    def vb1print(self, ID, now, system_number, system_dict):
        """
        Verbosity-level 1 printing, to keep an eye on a grid.

        Input:
            ID: thread ID for debugging (int): TODO fix this
            now: the time now as a UNIX-style epoch in seconds (float)
            system_number: the system number
        """

        # calculate estimated time of arrive (eta and eta_secs), time per run (tpr)
        localtime = time.localtime(now)

        # calculate stats
        n = self.shared_memory["n_saved_log_stats"].value
        if n < 2:
            # simple 1-system calculation: inaccurate
            # but best for small n
            dt = now - self.shared_memory["prev_log_time"][0]
            dn = system_number - self.shared_memory["prev_log_system_number"][0]
        else:
            # average over n_saved_log_stats
            dt = (
                self.shared_memory["prev_log_time"][0]
                - self.shared_memory["prev_log_time"][n - 1]
            )
            dn = (
                self.shared_memory["prev_log_system_number"][0]
                - self.shared_memory["prev_log_system_number"][n - 1]
            )

        eta, units, tpr, eta_secs = trem(
            dt, system_number, dn, self.grid_options["_total_starcount"]
        )

        # compensate for multithreading and modulo
        tpr *= self.grid_options["num_processes"] * self.grid_options["modulo"]

        if eta_secs < secs_per_day:
            fintime = time.localtime(now + eta_secs)
            etf = "{hours:02d}:{minutes:02d}:{seconds:02d}".format(
                hours=fintime.tm_hour, minutes=fintime.tm_min, seconds=fintime.tm_sec
            )
        else:
            d = int(eta_secs / secs_per_day)
            if d == 1:
                etf = "Tomorrow"
            else:
                etf = "In {} days".format(d)

        # modulo information
        if self.grid_options["modulo"] == 1:
            modulo = ""  # usual case
        else:
            modulo = "%" + str(self.grid_options["modulo"])

        # add up memory use from each thread
        total_mem_use = sum(self.shared_memory["memory_use_per_thread"])

        # make a string to describe the system e.g. M1, M2, etc.
        system_string = ""

        # use the multiplicity if given
        if "multiplicity" in system_dict:
            nmult = int(system_dict["multiplicity"])
        else:
            nmult = 4

        # masses
        for i in range(nmult):
            i1 = str(i + 1)
            if "M_" + i1 in system_dict:
                system_string += (
                    "M{}=".format(i1) + format_number(system_dict["M_" + i1]) + " "
                )

        # separation and orbital period
        if "separation" in system_dict:
            system_string += "a=" + format_number(system_dict["separation"])
        if "orbital_period" in system_dict:
            system_string += "P=" + format_number(system_dict["orbital_period"])

        # do the print
        if self.grid_options["_total_starcount"] > 0:
            self.verbose_print(
                "{opening_colour}{system_number}/{total_starcount}{modulo} {pc_colour}{pc_complete:5.1f}% complete {time_colour}{hours:02d}:{minutes:02d}:{seconds:02d} {ETA_colour}ETA={ETA:7.1f}{units} tpr={tpr:2.2e} {ETF_colour}ETF={ETF} {mem_use_colour}mem:{mem_use:.1f}MB {system_string_colour}{system_string}{closing_colour}".format(
                    opening_colour=self.ANSI_colours["reset"]
                    + self.ANSI_colours["yellow on black"],
                    system_number=system_number,
                    total_starcount=self.grid_options["_total_starcount"],
                    modulo=modulo,
                    pc_colour=self.ANSI_colours["blue on black"],
                    pc_complete=(100.0 * system_number)
                    / (1.0 * self.grid_options["_total_starcount"])
                    if self.grid_options["_total_starcount"]
                    else -1,
                    time_colour=self.ANSI_colours["green on black"],
                    hours=localtime.tm_hour,
                    minutes=localtime.tm_min,
                    seconds=localtime.tm_sec,
                    ETA_colour=self.ANSI_colours["red on black"],
                    ETA=eta,
                    units=units,
                    tpr=tpr,
                    ETF_colour=self.ANSI_colours["blue"],
                    ETF=etf,
                    mem_use_colour=self.ANSI_colours["magenta"],
                    mem_use=total_mem_use,
                    system_string_colour=self.ANSI_colours["yellow"],
                    system_string=system_string,
                    closing_colour=self.ANSI_colours["reset"],
                ),
                self.grid_options["verbosity"],
                1,
            )
        else:
            self.verbose_print(
                "{opening_colour}{system_number}{modulo} {time_colour}{hours:02d}:{minutes:02d}:{seconds:02d} tpr={tpr:2.2e} {mem_use_colour}mem:{mem_use:.1f}MB {system_string_colour}{system_string}{closing_colour}".format(
                    opening_colour=self.ANSI_colours["reset"]
                    + self.ANSI_colours["yellow on black"],
                    system_number=system_number,
                    modulo=modulo,
                    time_colour=self.ANSI_colours["green on black"],
                    hours=localtime.tm_hour,
                    minutes=localtime.tm_min,
                    seconds=localtime.tm_sec,
                    tpr=tpr,
                    mem_use_colour=self.ANSI_colours["magenta"],
                    mem_use=total_mem_use,
                    system_string_colour=self.ANSI_colours["yellow"],
                    system_string=system_string,
                    closing_colour=self.ANSI_colours["reset"],
                ),
                self.grid_options["verbosity"],
                1,
            )

    def vb2print(self, system_dict, cmdline_string):
        """
        Extra function for verbose printing
        """

        print(
            "Running this system now on thread {ID}\n{blue}{cmdline}{reset}:\n\t{system_dict}\n".format(
                ID=self.process_ID,
                blue=self.ANSI_colours["blue"],
                cmdline=cmdline_string,
                reset=self.ANSI_colours["reset"],
                system_dict=system_dict,
            )
        )

    def verbose_print(self, *args, **kwargs):
        """
        Wrapper method for the verbose print that calls the verbose print with the correct newline

        TODO: consider merging the two
        """

        # wrapper for functions.verbose_print to use the correct newline
        newline = kwargs.get("newline", self.grid_options["log_newline"])
        if newline is None:
            newline = "\n"
        kwargs["newline"] = newline

        # Pass the rest to the original verbose print
        verbose_print(*args, **kwargs)

    def _boxed(
        self, *stringlist, colour="yellow on black", boxchar="*", separator="\n"
    ):
        """
        Function to output a list of strings in a single box.

        Args:
            list = a list of strings to be output. If these contain the separator
                   (see below) these strings are split by it.
            separator = strings are split on this, default "\n"
            colour = the colour to be used, usually this is 'yellow on black'
                     as set in the ANSI_colours dict
            boxchar = the character used to make the box, '*' by default

        Note: handles tabs (\t) badly, do not use them!
        """
        strlen = 0
        strings = []
        lengths = []

        # make a list of strings
        if separator:
            for l in stringlist:
                strings += l.split(sep=separator)
        else:
            strings = stringlist

        # get lengths without ANSI codes
        for string in strings:
            lengths.append(len(strip_ansi.strip_ansi(string)))

        # hence the max length
        strlen = max(lengths)
        strlen += strlen % 2
        header = boxchar * (4 + strlen)

        # start output
        out = self.ANSI_colours[colour] + header + "\n"

        # loop over strings to output, padding as required
        for n, string in enumerate(strings):
            if lengths[n] % 2 == 1:
                string = " " + string
            pad = " " * int((strlen - lengths[n]) / 2)
            out = out + boxchar + " " + pad + string + pad + " " + boxchar + "\n"

        # close output and return
        out = out + header + "\n" + self.ANSI_colours["reset"]
        return out

    def _get_stream_logger(self, level=logging.DEBUG):
        """
        Function to set up the streamlogger
        """

        # Format
        fmt = "[%(asctime)s %(levelname)-8s %(processName)s] --- %(message)s"
        formatter = logging.Formatter(fmt)

        # Streamhandle
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setLevel(level)
        sh.setFormatter(formatter)

        # Logger itself
        stream_logger = logging.getLogger("stream_logger")
        stream_logger.handlers = []
        stream_logger.setLevel(level)
        stream_logger.addHandler(sh)

        return stream_logger

    def _clean_up_custom_logging(self, evol_type):
        """
        Function to clean up the custom logging.
        Has two types:
            'single':
                - removes the compiled shared library
                    (which name is stored in grid_options['_custom_logging_shared_library_file'])
                - TODO: unloads/frees the memory allocated to that shared library
                    (which is stored in grid_options['custom_logging_func_memaddr'])
                - sets both to None
            'multiple':
                - TODO: make this and design this
        """

        if evol_type == "single":
            self.verbose_print(
                "Cleaning up the custom logging stuff. type: single",
                self.grid_options["verbosity"],
                1,
            )

            # TODO: Explicitly unload the library

            # Reset the memory adress location
            self.grid_options["custom_logging_func_memaddr"] = -1

            # remove shared library files
            if self.grid_options["_custom_logging_shared_library_file"]:
                remove_file(
                    self.grid_options["_custom_logging_shared_library_file"],
                    self.grid_options["verbosity"],
                )
                self.grid_options["_custom_logging_shared_library_file"] = None

        if evol_type == "population":
            self.verbose_print(
                "Cleaning up the custom logging stuffs. type: population",
                self.grid_options["verbosity"],
                1,
            )

            # TODO: make sure that these also work. not fully sure if necessary tho.
            #   whether its a single file, or a dict of files/mem addresses

        if evol_type == "MC":
            pass
