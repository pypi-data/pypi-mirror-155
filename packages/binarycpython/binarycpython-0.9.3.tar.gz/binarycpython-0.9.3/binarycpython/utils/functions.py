"""
Module containing most of the utility functions for the binarycpython package

Functions here are mostly functions used in other classes/functions, or
useful functions for the user

Tasks:
    - TODO: change all prints to verbose_prints
"""

import os
import sys
import time
import json
import datetime
import collections
import resource
import tempfile
import subprocess
import types

from typing import Union
from io import StringIO

import h5py
import humanize
import numpy as np
import psutil
from colorama import Fore, Back, Style

from binarycpython import _binary_c_bindings
from binarycpython.utils.dicts import filter_dict_through_values

########################################################
# Unsorted
########################################################


def now(now_object=None, style=None, custom_format=None):
    """
    convenience function to return a string of the current time, using the format ``%m/%d/%Y %H:%M:%S``

    Args:
        style : if "nospace" then return the date/time with the format ``%Y%m%d_%H%M%S``, else use format ``%m/%d/%Y %H:%M:%S``

        custom_format: if set, uses this as a format rather than whatever is set by default or in the style variable
    """

    if not now_object:
        now_object = datetime.datetime.now()

    if not custom_format:
        if style == "nospace":
            # special case
            date_format = "%Y%m%d_%H%M%S"
        else:
            # our default
            date_format = "%m/%d/%Y %H:%M:%S"
    else:
        date_format = custom_format

    return datetime.datetime.strftime(now_object, date_format)


def format_number(number):
    """
    Function to take a number, express format it in scientific notation, and remove the trailing 0 if the exponent is 0
    """

    string = "{number:.2g}".format(number=number)
    string = string.replace("e+0", "e+")
    string = string.replace("e-0", "e-")

    return string


def check_if_in_shell():
    """
    Function to check whether the script is running from a shell
    """

    return bool(sys.stdin and sys.stdin.isatty())


def timedelta(delta):
    """
    Function to convert a length of time (float, seconds) to a string for
    human-readable output.
    """
    # currently use the humanize module to do this
    t = humanize.time.precisedelta(
        datetime.timedelta(seconds=delta),
        format="%0.2f",
        minimum_unit="milliseconds",
        suppress=["milliseconds"],
    )
    # and use more compact units
    t = t.replace(" days and", "d")
    t = t.replace(" hours and", "h")
    t = t.replace(" minutes and", "m")
    t = t.replace(" seconds and", "s")
    t = t.replace(" days", "d")
    t = t.replace(" hours", "h")
    t = t.replace(" minutes", "m")
    t = t.replace(" seconds", "s")
    return t


def get_ANSI_colours():
    """
    Function that returns a dictionary with text-colors in ANSI formatting
    """

    # ANSI colours dictionary
    foreground_colours = {
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN,
        "green": Fore.GREEN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
        "bold": Style.BRIGHT,
    }

    background_colours = {
        "red": Back.RED,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "cyan": Back.CYAN,
        "green": Back.GREEN,
        "magenta": Back.MAGENTA,
        "white": Back.WHITE,
        "black": Back.BLACK,
    }

    default_style = Style.BRIGHT
    colours = {}

    for c, foreground_colour in foreground_colours.items():
        colours[c] = default_style + foreground_colour
        for d, background_colour in background_colours.items():
            colours[c + " on " + d] = foreground_colour + background_colour
    colours["reset"] = Style.RESET_ALL
    return colours


def mem_use():
    """
    Return current process memory use in MB. (Takes no arguments)

    Note: this is per-thread only.
    """

    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def trem(dt, count, dn, n):
    """
    Estimate time remaining (seconds) given a differential time and count (i.e. ``progress = count/n``).

    Args:
        dt: is the time since the last call.
        count: is the current progress count.
        dn: is the number run since the last call.
        n: is the total number required.
    """

    tpr = dt / max(1, dn)
    etasecs = tpr * (n - count)
    (eta, units) = conv_time_units(etasecs)

    return (eta, units, tpr, etasecs)


def conv_time_units(t):
    """
    Converts time (t, in seconds, passing in as the only argument) to seconds, minutes or hours depending on its magnitude. Returns a tuple (t,units).
    """
    units = "s"
    # default to seconds
    if t > 60:
        t /= 60
        units = "m"
    if t > 60:
        t /= 60
        units = "h"
    return (t, units)


def bin_data(value, binwidth):
    """
    Function that bins the data using the absolute value of binwidth using the following formula::

        ((0.5 if value > 0.0 else -0.5) + int(value / abs(binwidth))) * abs(binwidth)

    Args:
        value: value that we want to bin
        binwidth: width of the binning

    Returns:
        binned value
    """

    return ((0.5 if value > 0.0 else -0.5) + int(value / abs(binwidth))) * abs(binwidth)


def convert_bytes(size):
    """
    Function to return the size + a magnitude string
    """

    for name in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, name)
        size /= 1024.0

    return size


def get_size(obj, seen=None):
    """
    Recursively finds size of objects

    From https://github.com/bosswissam/pysize
    """

    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def imports():
    """
    Generator that generates the names of all the modules that are loaded in the globals
    """

    for _, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


def isfloat(x: Union[str, float, int]):
    """
    Function to return `True` if the "number" x, which could be a string, is an float, otherwise return `False`.

    Args:
        x: string float or int that we will attempt to convert to an `float` value.
    """

    try:
        _ = float(x)
        return True
    except ValueError:
        return False


def isint(x: Union[str, float, int]):
    """
    Function to return `True` if the "number" x, which could be a string, is an int, otherwise return `False`.

    Args:
        x: string float or int that we will attempt to convert to an `int` value.
    """

    try:
        _ = int(x)
        return True
    except ValueError:
        return False


def convfloat(x):
    """
    Convert scalar x to a float if we can, in which case return the float, otherwise just return x without changing it. Usually, x is a string, but could be anything that float() can handle without failure.
    """

    try:
        y = float(x)
        return y
    except ValueError:
        return x


def datalinedict(line: str, parameters: list):
    """
    Convert a line of data to a more convenient dictionary.

    Arguments:
       line = a line of data as a string
       parameters = a list of the parameter names

    Note:
        If the parameter is a floating point number, it will be converted to Python's float type.
    """

    return {param: convfloat(value) for param, value in zip(parameters, line.split())}


def pad_output_distribution(dist: dict, binwidth: float):
    """
    Given a distribution, dist (a dictionary), which should be binned every binwidth (float), fill the distribution with zeros when there is no data. Note: this changes the data in place.

    Args:
        dist: dictionary containing the distribution data.
        binwidth: binwidth that is used to fill the distribution with 0 in places where there is no value/key.
    """

    # sorted list of the keys
    skeys = sorted(dist.keys(), key=lambda x: float(x))

    # get min and max, offset by the binwidth
    min_val = skeys[0] - binwidth
    max_val = skeys[-1] + binwidth

    # pad with zeros
    x = min_val
    while x <= max_val:
        dist[x] = dist.setdefault(x, 0.0)
        x += binwidth

    return dist


class catchtime:
    """
    Context manager to calculate time spent
    """

    def __enter__(self):
        """On entry we start the clock"""
        self.t = time.process_time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """On exit we stop the clock and measure the time spent"""
        self.t = time.process_time() - self.t
        print("Took {}s".format(self.t))


def is_capsule(o):
    """
    Function to tell whether object is a capsule
    """

    t = type(o)
    return t.__module__ == "builtins" and t.__name__ == "PyCapsule"


class Capturing(list):
    """
    Context manager to capture output and store it
    """

    def __enter__(self):
        """On entry we capture the stdout output"""

        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        """On exit we release the capture again"""

        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def call_binary_c_config(argument):
    """
    Function to interface with the binary_c config file

    Args:
        argument: argument for the binary_c config

    Returns:
        raw output of binary_c-config
    """

    BINARY_C_DIR = os.getenv("BINARY_C", None)
    if not BINARY_C_DIR:
        msg = "Error: the BINARY_C environment variable is not set. Aborting"
        raise ValueError(msg)

    BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")
    if not os.path.isfile(BINARY_C_CONFIG):
        msg = "binary_c-config file does not exist. Aborting"
        raise ValueError(msg)

    output = subprocess.run(
        [BINARY_C_CONFIG, argument], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")

    return output


########################################################
# utility functions
########################################################


def verbose_print(
    message: str, verbosity: int, minimal_verbosity: int, newline: str = "\n"
) -> None:
    """
    Function that decides whether to print a message based on the current verbosity
    and its minimum verbosity. If verbosity is equal or higher than the minimum, then we print.

    Args:
        message: message to print.
        verbosity: current verbosity level.
        minimal_verbosity: threshold verbosity above which to print.
        newline: newline character (or set of characters), defaults to ``\\n`` but ``\\x0d`` (carriage return) might be useful.
    """

    if verbosity >= minimal_verbosity:
        if newline == "\n":
            print(message)
        else:
            print(message, newline, sep="", end="")
        sys.stdout.flush()


def remove_file(file: str, verbosity: int = 0) -> None:
    """
    Function to remove files but with verbosity

    Args:
        file: full file path to the file that will be removed.
        verbosity: current verbosity level (Optional)

    Returns:
        the path of a sub directory called binary_c_python in the TMP of the file system

    """

    if os.path.exists(file):
        if not os.path.isfile(file):
            verbose_print(
                "This path ({}) is a directory, not a file".format(file), verbosity, 0
            )

        try:
            verbose_print("Removed {}".format(file), verbosity, 1)
            os.remove(file)

        except FileNotFoundError as inst:
            print("Error while deleting file {}: {}".format(file, inst))
    else:
        verbose_print(
            "File/directory {} doesn't exist. Can't remove it.".format(file),
            verbosity,
            1,
        )


def get_username():
    """
    Function to get the username of the user that spawned the current process
    """

    return psutil.Process().username()


def temp_dir(*child_dirs: str) -> str:
    """
    Function to create directory within the TMP directory of the file system, starting with `/<TMP>/binary_c_python-<username>`

    Makes use of os.makedirs exist_ok which requires python 3.2+

    Args:
        *child_dirs: str input where each next input will be a child of the previous full_path. e.g. ``temp_dir('tests', 'grid')`` will become ``'/tmp/binary_c_python-<username>/tests/grid'``

    Returns:
        the path of a sub directory called binary_c_python in the TMP of the file system
    """

    tmp_dir = tempfile.gettempdir()
    username = get_username()
    path = os.path.join(tmp_dir, "binary_c_python-{}".format(username))

    # loop over the other paths if there are any:
    if child_dirs:
        for extra_dir in child_dirs:
            path = os.path.join(path, extra_dir)

    #
    os.makedirs(path, exist_ok=True)

    return path


def create_hdf5(data_dir: str, name: str) -> None:
    """
    Function to create an hdf5 file from the contents of a directory:
     - settings file is selected by checking on files ending on settings
     - data files are selected by checking on files ending with .dat

    TODO: fix missing settings files

    Args:
        data_dir: directory containing the data files and settings file
        name: name of hdf5file.

    """

    # Make HDF5:
    # Create the file
    hdf5_filename = os.path.join(data_dir, "{}".format(name))
    print("Creating {}".format(hdf5_filename))
    hdf5_file = h5py.File(hdf5_filename, "w")

    # Get content of data_dir
    content_data_dir = os.listdir(data_dir)

    # Settings
    if any(file.endswith("_settings.json") for file in content_data_dir):
        print("Adding settings to HDF5 file")
        settings_file = os.path.join(
            data_dir,
            [file for file in content_data_dir if file.endswith("_settings.json")][0],
        )

        with open(settings_file, "r", encoding="utf-8") as settings_file:
            settings_json = json.load(settings_file)

        # Create settings group
        settings_grp = hdf5_file.create_group("settings")

        # Write version_string to settings_group
        settings_grp.create_dataset(
            "used_settings", data=json.dumps(settings_json, ensure_ascii=False)
        )

    # Get data files
    data_files = [el for el in content_data_dir if el.endswith(".dat")]
    if data_files:
        print("Adding data to HDF5 file")

        # Create the data group
        data_grp = hdf5_file.create_group("data")

        # Write the data to the file:
        # Make sure:
        for data_file in data_files:
            # filename stuff
            filename = data_file
            full_path = os.path.join(data_dir, filename)
            base_name = os.path.splitext(os.path.basename(filename))[0]

            # Get header info
            header_name = "{base_name}_header".format(base_name=base_name)
            data_headers = np.genfromtxt(full_path, dtype="str", max_rows=1)
            data_headers = np.char.encode(data_headers)
            data_grp.create_dataset(header_name, data=data_headers)

            # Add data
            data = np.loadtxt(full_path, skiprows=1)
            data_grp.create_dataset(base_name, data=data)

        hdf5_file.close()


########################################################
# binary_c output functions
########################################################


def output_lines(output: str) -> list:
    """
    Function that outputs the lines that were received from the binary_c run, but now as an iterator.

    Args:
        output: raw binary_c output

    Returns:
        Iterator over the lines of the binary_c output
    """

    if output:
        return output.splitlines()
    return []


def example_parse_output(output: str, selected_header: str) -> dict:
    """
    Function that parses output of binary_c. This version serves as an example and is quite
    detailed. Custom functions can be easier:

    This function works in two cases:
    if the caught line contains output like 'example_header time=12.32 mass=0.94 ..'
    or if the line contains output like 'example_header 12.32 0.94'
    Please don't the two cases.

    You can give a 'selected_header' to catch any line that starts with that.
    Then the values will be put into a dictionary.

    Tasks:
        - TODO: Think about exporting to numpy array or pandas instead of a defaultdict
        - TODO: rethink whether this function is necessary at all
        - TODO: check this function again

    Args:
        output: binary_c output string
        selected_header: string header of the output (the start of the line that you want to
            process)

    Returns:
        dictionary containing parameters as keys and lists for the values
    """

    value_dicts = []

    # split output on newlines
    for line in output.split("\n"):
        # Skip any blank lines
        if not line == "":
            split_line = line.split()

            # Select parts
            header = split_line[0]
            values_list = split_line[1:]

            # print(values_list)
            # Catch line starting with selected header
            if header == selected_header:
                # Check if the line contains '=' symbols:
                value_dict = {}
                if all("=" in value for value in values_list):
                    for value in values_list:
                        key, val = value.split("=")
                        value_dict[key.strip()] = val.strip()
                    value_dicts.append(value_dict)
                else:
                    if any("=" in value for value in values_list):
                        raise ValueError(
                            "Caught line contains some = symbols but not \
                            all of them do. aborting run"
                        )

                    for j, val in enumerate(values_list):
                        value_dict[j] = val
                    value_dicts.append(value_dict)

    if len(value_dicts) == 0:
        print(
            "Sorry, didn't find any line matching your header {}".format(
                selected_header
            )
        )
        return None

    keys = value_dicts[0].keys()

    # Construct final dict.
    final_values_dict = collections.defaultdict(list)
    for value_dict in value_dicts:
        for key in keys:
            final_values_dict[key].append(value_dict[key])

    return final_values_dict


########################################################
# Argument and default value functions
########################################################


def get_defaults(filter_values: bool = False) -> dict:
    """
    Function that calls the binaryc get args function and cast it into a dictionary.

    All the values are strings

    Args:
        filter_values: whether to filter out NULL and Function defaults.

    Returns:
        dictionary containing the parameter name as key and the parameter default as value
    """

    default_output = _binary_c_bindings.return_arglines()
    default_dict = {}

    for default in default_output.split("\n"):
        if not default in ["__ARG_BEGIN", "__ARG_END", ""]:
            key, value = default.split(" = ")
            default_dict[key] = value

    if filter_values:
        default_dict = filter_arg_dict(default_dict)

    return default_dict


def get_arg_keys() -> list:
    """
    Function that return the list of possible keys to give in the arg string.
    This function calls get_defaults()

    Returns:
        list of all the parameters that binary_c accepts (and has default values for, since
        we call get_defaults())
    """

    return list(get_defaults().keys())


def filter_arg_dict(arg_dict: dict) -> dict:
    """
    Function to filter out keys that contain values included in ['NULL', 'Function', '']

    This function is called by get_defaults()

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c

    Returns:
        filtered dictionary (pairs with NULL and Function values are removed)
    """

    return filter_dict_through_values(arg_dict.copy(), ["NULL", "Function", ""])


def create_arg_string(
    arg_dict: dict, sort: bool = False, filter_values: bool = False
) -> str:
    """
    Function that creates the arg string for binary_c. Takes a dictionary containing the arguments
    and writes them to a string
    This string is missing the 'binary_c ' at the start.

    Args:
        arg_dict: dictionary
        sort: (optional, default = False) Boolean whether to sort the order of the keys.
        filter_values: (optional, default = False) filters the input dict on keys that have NULL or `function` as value.

    Returns:
        The string built up by combining all the key + value's.
    """

    arg_string = ""

    # Whether to filter the arguments
    if filter_values:
        arg_dict = filter_arg_dict(arg_dict)

    #
    keys = sorted(arg_dict.keys()) if sort else arg_dict.keys()

    #
    for key in keys:
        arg_string += "{key} {value} ".format(key=key, value=arg_dict[key])

    arg_string = arg_string.strip()
    return arg_string


########################################################
# Help functions
########################################################


def get_help(
    param_name: str = "", print_help: bool = True, fail_silently: bool = False
) -> Union[dict, None]:
    """
    Function that returns the help info for a given parameter, by interfacing with binary_c

    Will check whether it is a valid parameter.

    Binary_c will output things in the following order:
    - Did you mean?
    - binary_c help for variable
    - default
    - available macros

    This function reads out that structure and catches the different components of this output

    Args:
        param_name: name of the parameter that you want info from. Will get checked whether its a
            valid parameter name
        print_help: (optional, default = True) whether to print out the help information
        fail_silently: (optional, default = False) Whether to print the errors raised if the
        parameter isn't valid

    Returns:
        Dictionary containing the help info. This dictionary contains `parameter_name`,
        `parameter_value_input_type`, `description`, optionally `macros`
    """

    available_arg_keys = get_arg_keys()

    if not param_name:
        print(
            "Please set the param_name to any of the following:\n {}".format(
                sorted(available_arg_keys)
            )
        )
        return None

    if param_name in available_arg_keys:
        help_info = _binary_c_bindings.return_help(param_name)
        cleaned = [el for el in help_info.split("\n") if not el == ""]

        # Get line numbers
        did_you_mean_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Did you mean")
        ]
        parameter_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("binary_c help")
        ]
        default_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Default")
        ]
        macros_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Available")
        ]

        help_info_dict = {}

        # Get alternatives
        if did_you_mean_nr:
            alternatives = cleaned[did_you_mean_nr[0] + 1 : parameter_line_nr[0]]
            alternatives = [el.strip() for el in alternatives]
            help_info_dict["alternatives"] = alternatives

        # Information about the parameter
        parameter_line = cleaned[parameter_line_nr[0]]
        parameter_name = parameter_line.split(":")[1].strip().split(" ")[0]
        parameter_value_input_type = (
            " ".join(parameter_line.split(":")[1].strip().split(" ")[1:])
            .replace("<", "")
            .replace(">", "")
        )

        help_info_dict["parameter_name"] = parameter_name
        help_info_dict["parameter_value_input_type"] = parameter_value_input_type

        description_line = " ".join(
            cleaned[parameter_line_nr[0] + 1 : default_line_nr[0]]
        )
        help_info_dict["description"] = description_line

        # Default:
        default_line = cleaned[default_line_nr[0]]
        default_value = default_line.split(":")[-1].strip()

        help_info_dict["default"] = default_value

        # Get Macros:
        if macros_line_nr:
            macros = cleaned[macros_line_nr[0] + 1 :]
            help_info_dict["macros"] = macros

        if print_help:
            for key, value in help_info_dict.items():
                print("{}:\n\t{}".format(key, value))

        return help_info_dict

    if not fail_silently:
        print(
            "{} is not a valid parameter name. Please choose from the \
            following parameters:\n\t{}".format(
                param_name, list(available_arg_keys)
            )
        )

    return {}


def get_help_all(print_help: bool = True) -> dict:
    """
    Function that reads out the output of the return_help_all API call to binary_c. This return_help_all binary_c returns all the information for the parameters, their descriptions and other properties. The output is categorised in sections.

    Args:
        print_help: (optional, default = True) prints all the parameters and their descriptions.

    Returns:
        returns a dictionary containing dictionaries per section. These dictionaries contain the parameters and descriptions etc for all the parameters in that section
    """

    # Call function
    help_all = _binary_c_bindings.return_help_all()

    # String manipulation
    split = help_all.split(
        "############################################################\n"
    )
    cleaned = [el for el in split if not el == "\n"]

    section_nums = [i for i in range(len(cleaned)) if cleaned[i].startswith("#####")]

    # Create dicts
    help_all_dict = {}

    # Select the section name and the contents of that section. Note, not all sections have content!
    for i, section_num in enumerate(section_nums):
        if not i == len(section_nums) - 1:
            params = cleaned[section_num + 1 : section_nums[i + 1]]
        else:
            params = cleaned[section_num + 1 : len(cleaned)]
        section_name = (
            cleaned[section_nums[i]]
            .lstrip("#####")
            .strip()
            .replace("Section ", "")
            .lower()
        )

        #
        params_dict = {}

        if params:

            # Clean it, replace in-text newlines with a space and then split on newlines.
            split_params = params[0].strip().replace("\n ", " ").split("\n")

            # Process params and descriptions per section
            for split_param in split_params:
                split_param_info = split_param.split(" : ")
                if not len(split_param_info) == 3:
                    # there are occasions where the semicolon
                    # is used in the description text itself.
                    if len(split_param_info) == 4:
                        split_param_info = [
                            split_param_info[0],
                            ": ".join([split_param_info[1], split_param_info[2]]),
                            split_param_info[3],
                        ]

                    # other occasions?

                # Put the information in a dict
                param_name = split_param_info[0]
                param_description = split_param_info[1]

                if len(split_param_info) > 2:
                    rest = split_param_info[2:]
                else:
                    rest = None

                params_dict[param_name] = {
                    "param_name": param_name,
                    "description": param_description,
                    "rest": "".join(rest) if rest else "",
                }

            # make section_dict
            section_dict = {
                "section_name": section_name,
                "parameters": params_dict.copy(),
            }

            # Put in the total dict
            help_all_dict[section_name] = section_dict.copy()

    # Print things
    if print_help:
        for section in sorted(help_all_dict.keys()):
            print(
                "##################\n###### Section {}\n##################".format(
                    section
                )
            )
            section_dict = help_all_dict[section]
            for param_name in sorted(section_dict["parameters"].keys()):
                param = section_dict["parameters"][param_name]
                print(
                    "\n{}:\n\t{}: {}".format(
                        param["param_name"], param["description"], param["rest"]
                    )
                )

    # # Loop over all the parameters an call the help() function on it.
    # # Takes a long time but this is for testing
    # for section in help_all_dict.keys():
    #     section_dict = help_all_dict[section]
    #     for param in section_dict['parameters'].keys():
    #         get_help(param)

    return help_all_dict


def get_help_super(print_help: bool = False, fail_silently: bool = True) -> dict:
    """
    Function that first runs get_help_all, and then per argument also run
    the help function to get as much information as possible.

    Args:
        print_help: (optional, default = False) Whether to print the information
        fail_silently: (optional, default = True) Whether to fail silently or to print the errors

    Returns:
        dictionary containing all dictionaries per section, which then contain as much info as possible per parameter.
    """

    # Get help_all information
    help_all_dict = get_help_all(print_help=False)

    #
    help_all_super_dict = help_all_dict.copy()

    # Loop over all sections and stuff
    for section_name, section in help_all_dict.items():
        # Skipping the section i/o because that one shouldn't be available to python anyway
        if not section_name == "i/o":
            for parameter_name in section["parameters"].keys():
                parameter = section["parameters"][parameter_name]

                # Get detailed help info
                detailed_help = get_help(
                    parameter_name,
                    print_help=False,
                    fail_silently=fail_silently,
                )

                if detailed_help:
                    # check whether the descriptions of help_all and detailed help are the same
                    if not fail_silently:
                        if not parameter["description"] == detailed_help["description"]:
                            print(json.dumps(parameter, indent=4, ensure_ascii=False))

                    ## put values into help all super dict
                    # input type
                    parameter["parameter_value_input_type"] = detailed_help[
                        "parameter_value_input_type"
                    ]

                    # default
                    parameter["default"] = detailed_help["default"]

                    # macros
                    if "macros" in detailed_help:
                        parameter["macros"] = detailed_help["macros"]

                section["parameters"][parameter_name] = parameter

    if print_help:
        print(json.dumps(help_all_super_dict, indent=4, ensure_ascii=False))

    return help_all_super_dict


def make_build_text() -> str:
    """
    Function to make build text

    Returns:
        string containing information about the build and the git branch
    """
    from binarycpython.utils.grid import Population

    version_pop = Population()
    version_info = version_pop.return_binary_c_version_info(parsed=True)
    # version_info = return_binary_c_version_info(parsed=True)

    git_revision = version_info["miscellaneous"]["git_revision"]
    git_branch = version_info["miscellaneous"]["git_branch"]
    build_datetime = version_info["miscellaneous"]["build"]

    info_string = """
This information was obtained by the following binary_c build:
\t**binary_c git branch**: {}\t**binary_c git revision**: {}\t**Built on**: {}
""".format(
        git_branch, git_revision, build_datetime
    )

    return info_string.strip()


def write_binary_c_parameter_descriptions_to_rst_file(output_file: str) -> None:
    """
    Function that calls the get_help_super() to get the help text/descriptions for all the
    parameters available in that build.

    Writes the results to a .rst file that can be included in the docs.

    Args:
        output_file: name of the output .rst file containing the ReStructuredText formatted output
            of all the binary_c parameters.
    """

    # Get the whole arguments dictionary
    arguments_dict = get_help_super()

    build_info = make_build_text()

    if not output_file.endswith(".rst"):
        raise ValueError(
            "Filename ({}) doesn't end with .rst, please provide a proper filename.".format(
                output_file
            )
        )

    with open(output_file, "w", encoding="utf-8") as f:

        print("Binary\\_c parameters", file=f)
        print("{}".format("=" * len("Binary\\_c parameters")), file=f)
        print(
            "The following chapter contains all the parameters that the current version of binary\\_c can handle, along with their descriptions and other properties.",
            file=f,
        )
        print("\n", file=f)
        print(build_info, file=f)
        print("\n", file=f)

        for el in arguments_dict.keys():
            print("Section: {}".format(el), file=f)
            print("{}\n".format("-" * len("Section: {}".format(el))), file=f)

            for arg in arguments_dict[el]["parameters"].keys():
                argdict = arguments_dict[el]["parameters"][arg]

                print("| **Parameter**: {}".format(argdict["param_name"]), file=f)
                print(
                    "| **Description**: {}".format(
                        argdict["description"].replace(
                            "|Rout/Rin-1|", "abs(Rout/Rin-1)"
                        )
                    ),
                    file=f,
                )
                if "parameter_value_input_type" in argdict:
                    print(
                        "| **Parameter input type**: {}".format(
                            argdict["parameter_value_input_type"]
                        ),
                        file=f,
                    )
                if "default" in argdict:
                    print("| **Default value**: {}".format(argdict["default"]), file=f)
                if "macros" in argdict:
                    print("| **Macros**: {}".format(argdict["macros"]), file=f)
                if not argdict["rest"] == "(null)":
                    print("| **Extra**: {}".format(argdict["rest"]), file=f)
                print("", file=f)


########################################################
# log file functions
########################################################


def load_logfile(logfile: str) -> None: # pragma: no cover
    """
    Experimental function that parses the generated log file of binary_c.

    This function is not finished and shouldn't be used yet.

    Tasks:
        - TODO: fix this function

    Args:
        - logfile: filename of the log file you want to parse

    Returns:

    """

    with open(logfile, "r", encoding="utf-8") as file:
        logfile_data = file.readlines()

    time_list = []
    m1_list = []
    m2_list = []
    k1_list = []
    k2_list = []
    sep_list = []
    ecc_list = []
    rel_r1_list = []
    rel_r2_list = []
    event_list = []

    # random_seed = logfile_data[0].split()[-2]
    # random_count = logfile_data[0].split()[-1]
    # probability = logfile_data[-1].split()

    for line in logfile_data[1:-1]:
        split_line = line.split()

        time_list.append(split_line[0])
        m1_list.append(split_line[1])
        m2_list.append(split_line[2])
        k1_list.append(split_line[3])
        k2_list.append(split_line[4])
        sep_list.append(split_line[5])
        ecc_list.append(split_line[6])
        rel_r1_list.append(split_line[7])
        rel_r2_list.append(split_line[8])
        event_list.append(" ".join(split_line[9:]))

    print(event_list)

def quotewrap(list):
    """
    Given a list, wrap each item in double quotes and return the new list
    """
    return ['"' + _x + '"' for _x in list]

def command_string_from_list(list):
    """
    Given a list, turn it into a quoted command string
    """
    return ' '.join(quotewrap(list))
