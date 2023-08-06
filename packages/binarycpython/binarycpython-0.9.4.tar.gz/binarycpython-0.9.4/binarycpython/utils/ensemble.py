"""
Module containing functions to interact with binary_c's
population ensemble using the binarycpython package

"""

import sys
import bz2
import time
import json
from typing import Any
import gc
import gzip
import inspect

from halo import Halo
import msgpack
import py_rinterpolate

import simplejson

from binarycpython.utils.dicts import (
    keys_to_floats,
    recursive_change_key_to_float,
    custom_sort_dict,
    recursive_change_key_to_string,
)
from binarycpython.utils.functions import verbose_print


def ensemble_setting(ensemble, parameter_name):
    """
    Function to get the setting of parameter_name in the given ensemble, or return the default value.
    """
    value = None

    try:
        value = ensemble["metadata"]["settings"]["population_settings"]["bse_options"][
            parameter_name
        ]
    except KeyError:
        value = None

    if value is None:
        try:
            value = ensemble["metadata"]["settings"]["population_settings"][
                "grid_options"
            ][parameter_name]
        except KeyError:
            value = None

    if value is None:
        try:
            value = ensemble["metadata"]["settings"]["population_settings"][
                "custom_options"
            ][parameter_name]
        except KeyError:
            value = None

    # not found, try the default
    if value is None:
        try:
            value = ensemble["metadata"]["settings"]["binary_c_defaults"][
                parameter_name
            ]
        except KeyError:
            value = None

    return value


def open_ensemble(filename, encoding="utf-8"):
    """
    Function to open an ensemble at filename for reading and decompression if required.
    """

    compression = ensemble_compression(filename)
    if ensemble_file_type(filename) == "msgpack":
        flags = "rb"
    else:
        flags = "rt"
    if compression == "bzip2":
        file_object = bz2.open(filename, flags, encoding=encoding)
    elif compression == "gzip":
        file_object = gzip.open(filename, flags, encoding=encoding)
    else:
        file_object = open(filename, flags, encoding=encoding)
    return file_object


def ensemble_compression(filename):
    """
    Return the compression type of the ensemble file, based on its filename extension.
    """

    if filename.endswith(".bz2"):
        return "bzip2"
    if filename.endswith(".gz"):
        return "gzip"
    return None


def ensemble_file_type(filename):
    """
    Returns the file type of an ensemble file.
    """

    if ".json" in filename:
        filetype = "JSON"
    elif ".msgpack" in filename:
        filetype = "msgpack"
    else:
        filetype = None
    return filetype


def load_ensemble(
    filename, convert_float_keys=True, select_keys=None, timing=False, flush=False
):
    """
    Function to load an ensemeble file, even if it is compressed,
    and return its contents to as a Python dictionary.

    Args:
        convert_float_keys : if True, converts strings to floats.
        select_keys : a list of keys to be selected from the ensemble.
    """

    # open the file

    # load with some info to the terminal
    print("Loading JSON...", flush=flush)

    # open the ensemble and get the file type
    file_object = open_ensemble(filename)
    filetype = ensemble_file_type(filename)

    if not filetype or not file_object:
        print(
            "Unknown filetype : your ensemble should be saved either as JSON or msgpack data.",
            flush=flush,
        )
        sys.exit()

    with Halo(text="Loading", interval=250, spinner="moon", color="yellow"):
        tstart = time.time()
        _loaded = False

        def _hook(obj):
            """
            Hook to load ensemble
            """

            nonlocal _loaded
            if _loaded is False:
                _loaded = True
                print(
                    "\nLoaded {} data, now putting in a dictionary".format(filetype),
                    flush=True,
                )
            return obj

        if filetype == "JSON":
            # orjson promises to be fast, but it doesn't seem to be
            # and fails on "Infinity"... oops
            # data = orjson.loads(file_object.read())

            # simplejson is faster than standard json and "just works"
            # on the big Moe set in 37s
            data = simplejson.load(file_object, object_hook=_hook)
            file_object.close()

            # standard json module
            # on the big Moe set takes 42s
            # data = json.load(file_object,
            #                 object_hook=_hook)
        elif filetype == "msgpack":
            data = msgpack.load(file_object, object_hook=_hook)
            file_object.close()

        if timing:
            print(
                "\n\nTook {} s to load the data\n\n".format(time.time() - tstart),
                flush=True,
            )

    # strip non-selected keys, if a list is given in select_keys
    if select_keys:
        keys = list(data["ensemble"].keys())
        for key in keys:
            if not key in select_keys:
                del data["ensemble"][key]

    # perhaps convert floats?
    tstart = time.time()
    if convert_float_keys:
        # timings are for 100 iterations on the big Moe data set
        # data = format_ensemble_results(data) # 213s
        # data = recursive_change_key_to_float(data) # 61s
        data = keys_to_floats(data)  # 6.94s

        if timing:
            print(
                "\n\nTook {} s to convert floats\n\n".format(time.time() - tstart),
                flush=True,
            )

    # return data
    return data


#####
def extract_ensemble_json_from_string(binary_c_output: str) -> dict:
    """
    Function to extract the ensemble_json information from a raw binary_c output string

    Args:
        binary_c_output: raw binary_c output string

    Returns:
        JSON dictionary with the parsed ENSEMBLE_JSON data
    """

    json_dict = None

    try:
        # If there is no output just return an empty dict:
        if not binary_c_output:
            json_dict = {}
            return json_dict

        ensemble_jsons_strings = [
            line
            for line in binary_c_output.splitlines()
            if line.startswith("ENSEMBLE_JSON")
        ]

        json_dict = handle_ensemble_string_to_json(
            ensemble_jsons_strings[0][len("ENSEMBLE_JSON ") :]
        )

        if len(ensemble_jsons_strings) > 1:
            verbose_print(
                "Warning: There is more than one line starting with ENSEMBLE_JSON. Taking the first, but you should check this out.",
                1,
                0,
            )
    except IndexError:
        verbose_print(
            "Error: Couldn't extract the ensemble information from the output string",
            0,
            0,
        )

    return json_dict


def handle_ensemble_string_to_json(raw_output):
    """
    Function that deals with the raw output of the ensemble and
    creates a working JSON dictionary out of it.

    Having this wrapper makes it easy to

    Args:
        raw_output: raw output of the ensemble dump by binary_c

    Returns:
        json.loads(raw_output, cls=BinarycDecoder)

    """
    return json.loads(raw_output, cls=BinarycDecoder)


def binaryc_json_serializer(obj: Any) -> Any:
    """
    Custom serialiser for binary_c to use when functions are present in the dictionary
    that we want to export.

    Function objects will be turned into str representations of themselves

    Args:
        obj: The object that might not be serialisable

    Returns:
        Either string representation of object if the object is a function, or the object itself
    """

    if inspect.isfunction(obj) or isinstance(obj, py_rinterpolate.Rinterpolate):
        return str(obj)
    else:
        try:
            string_version = str(obj)
            return string_version
        except:
            raise TypeError(
                "Unserializable object {} of type {}. Attempted to convert to string but that failed.".format(obj, type(obj))
            )

class BinarycDecoder(json.JSONDecoder):
    """
    Custom decoder to transform the numbers that are strings to actual floats
    """

    def decode(self, s):
        """
        Entry point function for decoding
        """

        result = super().decode(
            s
        )  # result = super(Decoder, self).decode(s) for Python 2.x
        return self._decode(result)

    def _decode(self, o):
        """
        Depending on the type of object is will determine whether to loop over the elements,
        or try to change the type of the object from string to float

        The try except might be a somewhat rough solution but it catches all cases.
        """

        # Check if we can turn it into a float
        # if isinstance(o, str) or isinstance(o, unicode):
        if isinstance(o, str):
            try:
                return float(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


class BinarycEncoder(json.JSONEncoder):
    """
    Encoding class function to attempt to convert things to strings.
    """

    def default(self, o):
        """
        Converting function. Well, could be more precise. look at the JSON module
        """

        try:
            str_repr = str(o)
        except TypeError:
            pass
        else:
            return str_repr

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


def format_ensemble_results(ensemble_dictionary):
    """
    Function to handle all the steps of formatting the ensemble output again.

    Input:
        ensemble_dictionary: dictionary containing all the ensemble results
    """

    original_ensemble_results = ensemble_dictionary

    float_format_ensemble_results = recursive_change_key_to_float(
        original_ensemble_results
    )
    del original_ensemble_results
    gc.collect()

    # Then sort the dictionary
    sorted_ensemble_results = custom_sort_dict(float_format_ensemble_results)
    del float_format_ensemble_results
    gc.collect()

    # Then Change the keys back to a string but with a %g format.
    reformatted_ensemble_results = recursive_change_key_to_string(
        sorted_ensemble_results
    )
    del sorted_ensemble_results
    gc.collect()

    # Put back in the dictionary
    return reformatted_ensemble_results
