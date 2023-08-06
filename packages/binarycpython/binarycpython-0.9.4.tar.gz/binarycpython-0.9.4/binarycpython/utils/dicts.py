"""
Module containing functions that binary_c-python uses to modify dictionaries.
"""

import collections
from typing import Union

import astropy.units as u
import numpy as np

# Define all numerical types

ALLOWED_NUMERICAL_TYPES = (int, float, complex, np.number)
UNION_ALLOWED_NUMERICAL_TYPES = Union[int, float, complex, np.number]


def keys_to_floats(input_dict: dict) -> dict:
    """
    Function to convert all the keys of the dictionary to float to float

    we need to convert keys to floats:
        this is ~ a factor 10 faster than David's ``recursive_change_key_to_float`` routine, probably because this version only does the float conversion, nothing else.

    Args:
        input_dict: dict of which we want to turn all the keys to float types if possible

    Returns:
        new_dict: dict of which the keys have been turned to float types where possible
    """

    # this adopts the type correctly *and* is fast
    new_dict = type(input_dict)()

    for k, v in input_dict.items():
        # convert key to a float, if we can
        # otherwise leave as is
        try:
            newkey = float(k)
        except ValueError:
            newkey = k

        # act on value(s)
        if isinstance(v, list):
            # list data
            new_dict[newkey] = [
                keys_to_floats(item)
                if isinstance(item, collections.abc.Mapping)
                else item
                for item in v
            ]
        elif isinstance(v, collections.abc.Mapping):
            # dict, ordereddict, etc. data
            new_dict[newkey] = keys_to_floats(v)
        else:
            # assume all other data are scalars
            new_dict[newkey] = v

    return new_dict


def recursive_change_key_to_float(input_dict: dict) -> dict:
    """
    Function to recursively change the key to float

    This only works if the dict contains just sub-dicts or numbers/strings.

    Does not work with lists as values

    Args:
        input_dict: dict of which we want to turn all the keys to float types if possible

    Returns:
        new_dict: dict of which the keys have been turned to float types where possible

    If input_dict is None or empty, returns an empty dict
    """

    new_dict = collections.OrderedDict()

    # if the input dict is None or empty, return an empty dict
    if input_dict is None or not input_dict:
        pass

    else:
        # dict has keys, loop over them
        for key in input_dict:
            if isinstance(input_dict[key], (dict, collections.OrderedDict)):
                try:
                    num_key = float(key)
                    new_dict[num_key] = recursive_change_key_to_float(input_dict[key])
                except ValueError:
                    new_dict[key] = recursive_change_key_to_float(input_dict[key])
            else:
                try:
                    num_key = float(key)
                    new_dict[num_key] = input_dict[key]
                except ValueError:
                    new_dict[key] = input_dict[key]

    return new_dict


def recursive_change_key_to_string(input_dict: dict, custom_format: str = "{:g}"):
    """
    Function to recursively change the key back to a string but this time in a format that we decide. We'll try to turn a string key into a float key before formatting the key

    Args:
        input_dict: dict of which we want to turn all the keys to string types (with a custom format)
        custom_format: custom format used when turning the key to strings

    Returns:
        new_dict: dict of which the keys have been turned to string types where possible
    """

    new_dict = collections.OrderedDict()

    for key in input_dict:
        # Try to turn into a float
        try:
            string_key = float(key)
        except ValueError:
            string_key = key

        # Turn into string with new format
        if not isinstance(string_key, str):
            string_key = custom_format.format(string_key)

        # If dictionary type, call function again
        if isinstance(input_dict[key], (dict, collections.OrderedDict)):
            new_dict[string_key] = recursive_change_key_to_string(
                input_dict[key], custom_format
            )
        else:
            new_dict[string_key] = input_dict[key]

    return new_dict


def _nested_set(dic, keys, value):
    """
    Code to set a value of a nested dict based on a list of keys. We take into account the fact that the vallue in the dict might not be set at all by the setdefault call and the reverse looping of the keys

    https://stackoverflow.com/questions/13687924/setting-a-value-in-a-nested-python-dictionary-given-a-list-of-indices-and-value

    TODO: describe better
    """

    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def _nested_get(dic, keys):
    """
    Code to get a value of a nested dict based on a list of keys. We take into account the fact that the vallue in the dict might not be set at all by the setdefault call and the reverse looping of the keys

    TODO: unused. Remove?
    """

    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    return dic[keys[-1]]


def _recursive_normalize_floats(path, input_dict, factor, parent=None, ignore=None):
    """
    Function to walk through the dictionary, multiplying only float values by a factor
    """

    if not parent:
        parent = input_dict

    for k, v in input_dict.items():
        if ignore and k in ignore:
            continue

        if isinstance(v, float):
            path.append(k)
            # must be a float, multiply by the factor
            _nested_set(parent, path, v * factor)
            path.pop()
        elif isinstance(v, (str, int)):
            path.append(k)
            # do nothing to strings or ints
            path.pop()
        elif v is None:
            path.append(k)
            path.pop()

        # dicts
        # note: isinstance isn't enough, we need to check the Mapping
        elif isinstance(v, collections.abc.Mapping):
            path.append(k)
            # nested dict
            _recursive_normalize_floats(path, v, factor, parent=parent)
            path.pop()
        else:
            print(
                "###Type {} not recognized: {}.{}={}".format(
                    type(v), ".".join(path), k, v
                )
            )


def multiply_float_values(input_dict, factor, ignore=None):
    """
    A function to recursively multiply values of a (nested) dictionary that are floats by a constant. Nested dictionaries call this function recursively.

    Args:
        input_dict: the dictionary
        factor: the constant that multiplies float values
    """

    path = []
    _recursive_normalize_floats(
        path, input_dict, factor, parent=input_dict, ignore=ignore
    )


def subtract_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to subtract two dictionaries, i.e. ``dict_1 - dict_2``

    Only allows values to be either a dict or a numerical type

    For the overlapping keys (key name present in both dicts):
        When the keys are of the same type: If the types are of numerical type we subtract the value at dict 2 from dict 1. If the types are both dictionaries: call this function with the subdicts

        When the keys are not of the same type: If the keys are all of numerical types we do the subtraction. If they are not numerical we raise an error.

    For the unique keys:
        If the key is from dict 1: adds the value to the new dict (be it numerical value or dict)

        If the key is from dict 2: Adds the negative of its value in case of numerical type. If the type is a dict, the result of ``subtract_dicts({}, dict_2[key])`` will be set

    If the result is 0, the key will be removed from the resulting dict.

    If that results in an empty dict, the dict will be removed too.

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        Subtracted dictionary, i.e. ``dict_1 - dict_2``
    """

    # Set up new dict
    new_dict = {}

    #
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        # If these items are numerical types
        if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES):
            new_dict[key] = dict_1[key]
            if new_dict[key] == 0:
                del new_dict[key]

        elif isinstance(dict_1[key], dict):
            new_dict[key] = dict_1[key]
        else:
            msg = "Error: using unsupported type for key {}: {}".format(
                key, type(dict_1[key])
            )
            print(msg)
            raise ValueError(msg)

    # Add the unique keys to the new dict
    for key in unique_to_dict_2:
        # If these items are numerical type, we should add the negative of the value
        if isinstance(dict_2[key], ALLOWED_NUMERICAL_TYPES):
            new_dict[key] = -dict_2[key]
            if new_dict[key] == 0:
                del new_dict[key]

        # Else we should place the negative of that dictionary in the new place
        elif isinstance(dict_2[key], dict):
            new_dict[key] = subtract_dicts({}, dict_2[key])
        else:
            msg = "Error: using unsupported type for key {}: {}".format(
                key, type(dict_2[key])
            )
            print(msg)
            raise ValueError(msg)

    # Go over the common keys:
    for key in overlapping_keys:

        # See whether the types are actually the same
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions:
            if (type(dict_1[key]) in ALLOWED_NUMERICAL_TYPES) and (
                type(dict_2[key]) in ALLOWED_NUMERICAL_TYPES
            ):
                # We can safely subtract the values since they are all numeric
                new_dict[key] = dict_1[key] - dict_2[key]
                if new_dict[key] == 0:
                    del new_dict[key]

            else:
                msg = "Error key: {key} value: {value1} type: {type} and key: {key} value: {value2} type: {type2} are not of the same type and cannot be merged".format(
                    key=key,
                    value1=dict_1[key],
                    type=type(dict_1[key]),
                    value2=dict_2[key],
                    type2=type(dict_2[key]),
                )

                print(msg)
                raise ValueError(msg)

        # This is where the keys are the same
        else:
            # If these items are numeric types
            if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES):
                new_dict[key] = dict_1[key] - dict_2[key]

                # Remove entry if the value is 0
                if new_dict[key] == 0:
                    del new_dict[key]

            elif isinstance(dict_1[key], dict):
                new_dict[key] = subtract_dicts(dict_1[key], dict_2[key])

                # Remove entry if it results in an empty dict
                if not new_dict[key]:
                    del new_dict[key]
            else:
                msg = "Error: using unsupported type for key {}: {}".format(
                    key, type(dict_2[key])
                )
                print(msg)
                raise ValueError(msg)

    #
    return new_dict


class AutoVivificationDict(dict):
    """
    Implementation of perl's autovivification feature, by overriding the
    get item and the __iadd__ operator (https://docs.python.org/3/reference/datamodel.html?highlight=iadd#object.__iadd__)

    This allows to set values within a subdict that might not exist yet:

    Example:
        newdict = {}
        newdict['example']['mass'] += 10
        print(newdict)
        >>> {'example': {'mass': 10}}
    """

    def __getitem__(self, item):
        """
        Getitem function for the autovivication dict
        """

        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

    def __iadd__(self, other):
        """
        iadd function (handling the +=) for the autovivication dict.
        """

        # if a value does not exist, assume it is 0.0
        try:
            self += other
        except:
            self = other
        return self


def inspect_dict(
    input_dict: dict, indent: int = 0, print_structure: bool = True
) -> dict:
    """
    Function to (recursively) inspect a (nested) dictionary.
    The object that is returned is a dictionary containing the key of the input_dict, but as value
    it will return the type of what the value would be in the input_dict

    In this way we inspect the structure of these dictionaries, rather than the exact contents.

    Args:
        input_dict: dictionary you want to inspect
        print_structure: (optional, default = True)
        indent: (optional, default = 0) indent of the first output

    Returns:
        Dictionary that has the same structure as the input_dict, but as values it has the
            type(input_dict[key]) (except if the value is a dict)
    """

    structure_dict = collections.OrderedDict()

    #
    for key, value in input_dict.items():
        structure_dict[key] = type(value)

        if print_structure:
            print("\t" * indent, key, type(value))

        if isinstance(value, dict):
            structure_dict[key] = inspect_dict(
                value, indent=indent + 1, print_structure=print_structure
            )

    return structure_dict


def count_keys_recursive(input_dict: dict) -> int:
    """
    Function to recursively count the total number of keys in a dictionary.

    Args:
        input_dict: dictionary that we want to know the total amount of keys from.

    Returns:
        local_count: total amount of keys within the input_dict.
    """

    local_count = 0
    for key in input_dict.keys():
        local_count += 1
        if isinstance(input_dict[key], (dict, collections.OrderedDict)):
            local_count += count_keys_recursive(input_dict[key])

    return local_count


def merge_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to merge two dictionaries in a custom way.

    Behaviour:

    When dict keys are only present in one of either:
        - we just add the content to the new dict

    When dict keys are present in both, we decide based on the value types how to combine them:
        - dictionaries will be merged by calling recursively calling this function again
        - numbers will be added
        - (opt) lists will be appended
        - booleans are merged with logical OR
        - identical strings are just set to the string
        - non-identical strings are concatenated
        - NoneTypes are set to None
        - In the case that the instances do not match: for now I will raise an error

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        Merged dictionary

    """

    # Set up new dict
    new_dict = collections.OrderedDict()

    #
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        new_dict[key] = dict_1[key]

    for key in unique_to_dict_2:
        new_dict[key] = dict_2[key]

    # Go over the common keys:
    for key in overlapping_keys:

        # If they keys are not the same, it depends on their type whether we still deal with them at all, or just raise an error
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions: numbers can be added
            if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES) and isinstance(
                dict_2[key], ALLOWED_NUMERICAL_TYPES
            ):
                new_dict[key] = dict_1[key] + dict_2[key]

            # Exceptions: versions of dicts can be merged
            elif isinstance(
                dict_1[key], (dict, collections.OrderedDict, type(AutoVivificationDict))
            ) and isinstance(
                dict_2[key], (dict, collections.OrderedDict, type(AutoVivificationDict))
            ):
                new_dict[key] = merge_dicts(dict_1[key], dict_2[key])

            # string-int clash : convert both to ints and save
            elif (
                isinstance(dict_1[key], str)
                and isinstance(dict_2[key], int)
                or isinstance(dict_1[key], int)
                and isinstance(dict_2[key], str)
            ):
                try:
                    new_dict[key] = int(dict_1[key]) + int(dict_2[key])
                except ValueError as e:
                    msg = "{}: Failed to convert string (either '{}' or '{}') to an int".format(
                        key, dict_1[key], dict_2[key]
                    )
                    raise ValueError(msg) from e

            # string-float clash : convert both to floats and save
            elif (
                isinstance(dict_1[key], str)
                and isinstance(dict_2[key], float)
                or isinstance(dict_1[key], float)
                and isinstance(dict_2[key], str)
            ):
                try:
                    new_dict[key] = float(dict_1[key]) + float(dict_2[key])
                except ValueError as e:
                    msg = "{}: Failed to convert string (either '{}' or '{}') to an float".format(
                        key, dict_1[key], dict_2[key]
                    )
                    raise ValueError(msg) from e

            # If the above cases have not dealt with it, then we should raise an error
            else:
                msg = "merge_dicts error: key: {key} value: {value1} type: {type1} and key: {key} value: {value2} type: {type2} are not of the same type and cannot be merged".format(
                    key=key,
                    value1=dict_1[key],
                    type1=type(dict_1[key]),
                    value2=dict_2[key],
                    type2=type(dict_2[key]),
                )
                raise ValueError(msg)

        # Here the keys are the same type
        # Here we check for the cases that we want to explicitly catch. Ints will be added,
        # floats will be added, lists will be appended (though that might change) and dicts will be
        # dealt with by calling this function again.
        else:
            # ints
            # Booleans (has to be the type Bool, not just a 0 or 1)
            if isinstance(dict_1[key], bool) and isinstance(dict_2[key], bool):
                new_dict[key] = dict_1[key] or dict_2[key]

            elif isinstance(dict_1[key], int) and isinstance(dict_2[key], int):
                new_dict[key] = dict_1[key] + dict_2[key]

            # floats
            elif isinstance(dict_1[key], float) and isinstance(dict_2[key], float):
                new_dict[key] = dict_1[key] + dict_2[key]

            # lists
            elif isinstance(dict_1[key], list) and isinstance(dict_2[key], list):
                new_dict[key] = dict_1[key] + dict_2[key]

            # Astropy quantities (using a dummy type representing the numpy array)
            elif isinstance(dict_1[key], type(np.array([1]) * u.m)) and isinstance(
                dict_2[key], type(np.array([1]) * u.m)
            ):
                new_dict[key] = dict_1[key] + dict_2[key]

            # dicts
            elif isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                new_dict[key] = merge_dicts(dict_1[key], dict_2[key])

            # strings
            elif isinstance(dict_1[key], str) and isinstance(dict_2[key], str):
                if dict_1[key] == dict_2[key]:
                    # same strings
                    new_dict[key] = dict_1[key]
                else:
                    # different strings: just concatenate them
                    new_dict[key] = dict_1[key] + dict_2[key]

            # None types
            elif dict_1[key] is None and dict_2[key] is None:
                new_dict[key] = None

            else:
                msg = "Object types {}: {} ({}), {} ({}) not supported.".format(
                    key,
                    dict_1[key],
                    type(dict_1[key]),
                    dict_2[key],
                    type(dict_2[key]),
                )
                raise ValueError(msg)

    #
    return new_dict


def update_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to update dict_1 with values of dict_2 in a recursive way.

    Behaviour:
        When dict keys are only present in one of either: we just add the content to the new dict

        When dict keys are present in both, we decide based on the value types how to combine them: value of dict2 will be taken

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        New dictionary with Updated values

    """

    # Set up new dict of the same type as dict_1
    new_dict = dict_1.__class__()

    # Get keys
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        new_dict[key] = dict_1[key]

    for key in unique_to_dict_2:
        new_dict[key] = dict_2[key]

    # Go over the common keys:
    for key in overlapping_keys:

        # See whether the types are actually the same
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions:
            if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES) and isinstance(
                dict_2[key], ALLOWED_NUMERICAL_TYPES
            ):
                new_dict[key] = dict_2[key]

            else:
                print(
                    "Error key: {key} value: {value1} type: {type1} and key: {key} value: {value2} type: {type2} are not of the same type and cannot be merged".format(
                        key=key,
                        value1=dict_1[key],
                        type1=type(dict_1[key]),
                        value2=dict_2[key],
                        type2=type(dict_2[key]),
                    )
                )
                raise ValueError

        # Here we check for the cases that we want to explicitly catch. Ints will be added,
        # floats will be added, lists will be appended (though that might change) and dicts will be
        # dealt with by calling this function again.
        else:
            # dicts
            if isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                new_dict[key] = update_dicts(dict_1[key], dict_2[key])
            else:
                new_dict[key] = dict_2[key]

    #
    return new_dict


def multiply_values_dict(input_dict: dict, factor: UNION_ALLOWED_NUMERICAL_TYPES):
    """
    Function that goes over dictionary recursively and multiplies the value if possible by a factor

    If the key equals "general_info", the multiplication gets skipped.

    This function changes the values in-place, so the original dict is modified

    Args:
        input_dict: dictionary of which we want to multiply the values by <factor>
        factor: factor that we want to multiply the values with

    Returns:
        multiplied_dict: dict containing the multiplied keys. This is the same object as we passed as input.
    """

    for key in input_dict:
        if not key == "general_info":
            if isinstance(input_dict[key], (dict, collections.OrderedDict)):
                input_dict[key] = multiply_values_dict(input_dict[key], factor)
            else:
                if isinstance(input_dict[key], (int, float)):
                    input_dict[key] = input_dict[key] * factor

    return input_dict


def custom_sort_dict(input_dict: dict) -> dict:
    """
    Returns a dictionary that is ordered, but can handle numbers better than normal OrderedDict

    When the keys of the current dictionary are of mixed type, we first find all the unique types.
    Sort that list of type names. Then find the values that fit that type.
    Sort those and append them to the sorted keys list.
    This is done until all the keys are sorted.

    All objects other than dictionary types are directly return as they are

    Args:
        input_dict: object which will be sorted (and returned as a new object) if its a dictionary, otherwise it will be returned without change.
    """

    # If the new input is a dictionary, then try to sort it
    if isinstance(input_dict, (dict, collections.OrderedDict)):
        new_dict = collections.OrderedDict()

        keys = input_dict.keys()

        # Check if types are the same
        all_types_keys = []
        for key in keys:
            if not type(key) in all_types_keys:
                all_types_keys.append(type(key))

        # If there are multiple types, then we loop over them and do a piece wise sort
        if len(all_types_keys) > 1:
            msg = "Different types in the same dictionary key set"
            print(msg)

            # Create a string repr of the type name to sort them afterwards
            str_types = {repr(el): el for el in all_types_keys}

            # Set up sorted keys list
            sorted_keys = []

            for key_str_type in sorted(str_types.keys()):
                cur_type = str_types[key_str_type]

                cur_list = [key for key in keys if isinstance(key, cur_type)]
                cur_sorted_list = sorted(cur_list)

                sorted_keys = sorted_keys + cur_sorted_list
        else:
            sorted_keys = sorted(keys)

        for key in sorted_keys:
            new_dict[key] = custom_sort_dict(input_dict[key])

        return new_dict

    return input_dict


def filter_dict(arg_dict: dict, filter_list: list) -> dict:
    """
    Function to filter out keys that are contains in filter_list

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c
        filter_list: lists of keys to be filtered out
    Returns:
        filtered dictionary
    """

    new_dict = arg_dict.copy()

    for key in filter_list:
        if key in new_dict:
            del new_dict[key]

    return new_dict


def filter_dict_through_values(arg_dict: dict, filter_list: list) -> dict:
    """
    Function to filter out keys that contain values included in filter_list

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c
        filter_list: lists of values to be filtered out
    Returns:
        filtered dictionary
    """

    new_dict = {}

    for key in arg_dict:
        if not arg_dict[key] in filter_list:
            new_dict[key] = arg_dict[key]

    return new_dict


def prepare_dict(global_dict: dict, list_of_sub_keys: list) -> None:
    """
    Function that makes sure that the global dict is prepared to have a value set there.
    This dictionary will store values and factors for the distribution functions,
    so that they don't have to be calculated each time.

    Args:
        global_dict: globally accessible dictionary where factors are stored in
        list_of_sub_keys: List of keys that must become be(come) present in the global_dict
    """

    internal_dict_value = global_dict

    # This loop almost mimics a recursive loop into the dictionary.
    # It checks whether the first key of the list is present, if not; set it with an empty dict.
    # Then it overrides itself to be that (new) item, and goes on to do that again, until the list
    # exhausted
    for k in list_of_sub_keys:
        # If the sub key doesnt exist then make an empty dict
        if not internal_dict_value.get(k, None):
            internal_dict_value[k] = {}
        internal_dict_value = internal_dict_value[k]


def set_opts(opts: dict, newopts: dict) -> dict:
    """
    Function to take a default dict and override it with newer values.

    # TODO: consider changing this to just a dict.update

    Args:
        opts: dictionary with default values
        newopts: dictionary with new values

    Returns:
        returns an updated dictionary
    """

    if newopts:
        for opt in newopts.keys():
            if opt in opts.keys():
                opts[opt] = newopts[opt]

    return opts


def normalize_dict(result_dict: dict) -> dict:
    """
    Function to normalise a dictionary by summing all the values and dividing each term by the total. Designed for dictionary containing only positive values.

    Args:
        result_dict: dictionary where values should be positive number objects

    Returns:
        normalized_dict: dictionary where the values are normalised to sum to 1
    """

    normalized_dict = {}

    sum_result = sum(list(result_dict.values()))
    for key in result_dict.keys():
        normalized_dict[key] = result_dict[key] / sum_result

    return normalized_dict
