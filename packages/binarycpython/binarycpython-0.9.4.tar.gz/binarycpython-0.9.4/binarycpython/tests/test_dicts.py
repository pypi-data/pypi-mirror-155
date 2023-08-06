"""
Unittests for dicts module

TODO: _nested_set
"""

import os
import unittest
from collections import OrderedDict

from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
)
from binarycpython.utils.dicts import (
    merge_dicts,
    set_opts,
    AutoVivificationDict,
    inspect_dict,
    normalize_dict,
    filter_dict,
    filter_dict_through_values,
    prepare_dict,
    custom_sort_dict,
    multiply_values_dict,
    keys_to_floats,
    count_keys_recursive,
    recursive_change_key_to_float,
    recursive_change_key_to_string,
    multiply_float_values,
    subtract_dicts,
    update_dicts,
    _nested_get,
    _nested_set,
)

TMP_DIR = temp_dir("tests", "test_dicts")


class dummy:
    """
    Dummy class to be used in the merge_dicts
    """

    def __init__(self, name):
        """
        init
        """
        self.name = name

    def __str__(self):
        """
        str returns self.name
        """
        return self.name


class test_merge_dicts(unittest.TestCase):
    """
    Unittests for function merge_dicts
    """

    def test_empty(self):
        with Capturing() as output:
            self._test_empty()

    def _test_empty(self):
        """
        Test merging an empty dict
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        dict_2 = {}
        output_dict = merge_dicts(input_dict, dict_2)
        self.assertTrue(output_dict == input_dict)

    def test_unequal_types(self):
        with Capturing() as output:
            self._test_unequal_types()

    def _test_unequal_types(self):
        """
        Test merging unequal types: should raise valueError
        """

        dict_1 = {"input": 10}
        dict_2 = {"input": "hello"}

        self.assertRaises(ValueError, merge_dicts, dict_1, dict_2)

    def test_bools(self):
        with Capturing() as output:
            self._test_bools()

    def _test_bools(self):
        """
        Test merging dict with booleans
        """

        dict_1 = {"bool": True}
        dict_2 = {"bool": False}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["bool"], bool))
        self.assertTrue(output_dict["bool"])

    def test_ints(self):
        with Capturing() as _:
            self._test_ints()

    def _test_ints(self):
        """
        Test merging dict with ints
        """

        dict_1 = {"int": 2}
        dict_2 = {"int": 1}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["int"], int))
        self.assertEqual(output_dict["int"], 3)

    def test_floats(self):
        with Capturing() as output:
            self._test_floats()

    def _test_floats(self):
        """
        Test merging dict with floats
        """

        dict_1 = {"float": 4.5}
        dict_2 = {"float": 4.6}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["float"], float))
        self.assertEqual(output_dict["float"], 9.1)

    def test_lists(self):
        with Capturing() as output:
            self._test_lists()

    def _test_lists(self):
        """
        Test merging dict with lists
        """

        dict_1 = {"list": [1, 2]}
        dict_2 = {"list": [3, 4]}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["list"], list))
        self.assertEqual(output_dict["list"], [1, 2, 3, 4])

    def test_dicts(self):
        with Capturing() as _:
            self._test_dicts()

    def _test_dicts(self):
        """
        Test merging dict with dicts
        """

        dict_1 = {"dict": {"same": 1, "other_1": 2.0}}
        dict_2 = {"dict": {"same": 2, "other_2": [4.0]}}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["dict"], dict))
        self.assertEqual(
            output_dict["dict"], {"same": 3, "other_1": 2.0, "other_2": [4.0]}
        )

    def test_unsupported(self):
        with Capturing() as output:
            self._test_unsupported()

    def _test_unsupported(self):
        """
        Test merging dict with unsupported types. should raise ValueError
        """

        dict_1 = {"new": dummy("david")}
        dict_2 = {"new": dummy("gio")}

        # output_dict = merge_dicts(dict_1, dict_2)
        self.assertRaises(ValueError, merge_dicts, dict_1, dict_2)


class test_setopts(unittest.TestCase):
    """
    Unit test class for setopts
    """

    def test_setopts(self):
        with Capturing() as output:
            self._test_setopts()

    def _test_setopts(self):
        """
        Unittest for function set_opts
        """

        default_dict = {"m1": 2, "m2": 3}
        output_dict_1 = set_opts(default_dict, {})
        self.assertTrue(output_dict_1 == default_dict)

        new_opts = {"m1": 10}
        output_dict_2 = set_opts(default_dict, new_opts)
        updated_dict = default_dict.copy()
        updated_dict["m1"] = 10

        self.assertTrue(output_dict_2 == updated_dict)


class test_AutoVivicationDict(unittest.TestCase):
    """
    Unittests for AutoVivicationDict
    """

    def test_add(self):
        """
        Tests to see if the adding is done correctly
        """

        result_dict = AutoVivificationDict()

        result_dict["a"]["b"]["c"] += 10

        self.assertEqual(result_dict["a"]["b"]["c"], 10)
        result_dict["a"]["b"]["c"] += 10
        self.assertEqual(result_dict["a"]["b"]["c"], 20)


class test_inspect_dict(unittest.TestCase):
    """
    Unittests for function inspect_dict
    """

    def test_compare_dict(self):
        with Capturing() as output:
            self._test_compare_dict()

    def _test_compare_dict(self):
        """
        Test checking if inspect_dict returns the correct structure by comparing it to known value
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        output_dict = inspect_dict(input_dict)
        compare_dict = {
            "int": int,
            "float": float,
            "list": list,
            "function": os.path.isfile.__class__,
            "dict": {"int": int, "float": float},
        }
        self.assertTrue(compare_dict == output_dict)

    def test_compare_dict_with_print(self):
        with Capturing() as output:
            self._test_compare_dict_with_print()

    def _test_compare_dict_with_print(self):
        """
        Test checking output is printed
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        _ = inspect_dict(input_dict, print_structure=True)


class test_custom_sort_dict(unittest.TestCase):
    """
    Unittests for function custom_sort_dict
    """

    def test_custom_sort_dict(self):
        with Capturing() as output:
            self._test_custom_sort_dict()

    def _test_custom_sort_dict(self):
        """
        Test custom_sort_dict
        """

        input_dict = {"2": 1, "1": {2: 1, 1: 10}, -1: 20, 4: -1}

        #
        output_1 = custom_sort_dict(input_dict)

        desired_output_1 = OrderedDict(
            [(-1, 20), (4, -1), ("1", OrderedDict([(1, 10), (2, 1)])), ("2", 1)]
        )

        #
        self.assertEqual(output_1, desired_output_1)


class test_filter_dict(unittest.TestCase):
    """
    Unittests for function filter_dict
    """

    def test_filter_dict(self):
        with Capturing() as output:
            self._test_filter_dict()

    def _test_filter_dict(self):
        """
        Test filter_dict
        """

        dict_1 = {"a": 10}
        input_1 = ["a"]

        res_1 = filter_dict(dict_1, input_1)

        self.assertIsInstance(res_1, dict)
        self.assertFalse(res_1)


class test_filter_dict_through_values(unittest.TestCase):
    """
    Unittests for function filter_dict_through_values
    """

    def test_filter_dict_through_values(self):
        with Capturing() as output:
            self._test_filter_dict_through_values()

    def _test_filter_dict_through_values(self):
        """
        Test filter_dict_through_values
        """

        dict_1 = {"a": 10}
        input_1 = [10]

        res_1 = filter_dict_through_values(dict_1, input_1)

        self.assertIsInstance(res_1, dict)
        self.assertFalse(res_1)


class test_prepare_dict(unittest.TestCase):
    """
    Unittests for function prepare_dict
    """

    def test_prepare_dict(self):
        with Capturing() as output:
            self._test_prepare_dict()

    def _test_prepare_dict(self):
        """
        Test prepare_dict
        """

        global_dict = {}

        # Call function to make sure the nested key contains an empty dict to store stuff in
        input_1 = ["a", "b"]
        prepare_dict(global_dict, input_1)

        #
        self.assertIsNotNone(global_dict.get("a", None))
        self.assertIsNotNone(global_dict["a"].get("b", None))
        self.assertIsInstance(global_dict["a"]["b"], dict)
        self.assertFalse(global_dict["a"]["b"])


class test_normalize_dict(unittest.TestCase):
    """
    Unittests for function normalize_dict
    """

    def test_normalize_dict(self):
        with Capturing() as output:
            self._test_normalize_dict()

    def _test_normalize_dict(self):
        """
        Test normalize_dict
        """

        input_1 = {"a": 10, "b": 20, "c": 4}

        res_1 = normalize_dict(input_1)

        self.assertEqual(sum(list(res_1.values())), 1.0)


class test_multiply_values_dict(unittest.TestCase):
    """
    Unittests for function multiply_values_dict
    """

    def test_multiply_values_dict(self):
        with Capturing() as output:
            self._test_multiply_values_dict()

    def _test_multiply_values_dict(self):
        """
        Test multiply_values_dict
        """

        input_1 = {"a": 1, "b": {"c": 10}}
        desired_output_1 = {"a": 2, "b": {"c": 20}}

        output_1 = multiply_values_dict(input_1, 2)

        #
        self.assertEqual(output_1, desired_output_1)


class test_count_keys_recursive(unittest.TestCase):
    """
    Unittests for function count_keys_recursive
    """

    def test_count_keys_recursive(self):
        with Capturing() as output:
            self._test_count_keys_recursive()

    def _test_count_keys_recursive(self):
        """
        Test count_keys_recursive
        """

        #
        input_1 = {"a": 2, "b": {"c": 20, "d": {"aa": 1, "bb": 2}}}
        output_1 = count_keys_recursive(input_1)

        #
        self.assertEqual(output_1, 6)


class test_keys_to_floats(unittest.TestCase):
    """
    Unittests for function keys_to_floats
    """

    def test_keys_to_floats(self):
        with Capturing() as output:
            self._test_keys_to_floats()

    def _test_keys_to_floats(self):
        """
        Test keys_to_floats
        """

        input_1 = {"a": 1, "1": 2, "1.0": 3, "b": {4: 10, "5": 1}}
        output_1 = keys_to_floats(input_1)

        desired_output_1 = {"a": 1, 1.0: 3, "b": {4.0: 10, 5.0: 1}}

        self.assertEqual(output_1, desired_output_1)


class test_recursive_change_key_to_float(unittest.TestCase):
    """
    Unittests for function recursive_change_key_to_float
    """

    def test_recursive_change_key_to_float(self):
        with Capturing() as output:
            self._test_recursive_change_key_to_float()

    def _test_recursive_change_key_to_float(self):
        """
        Test recursive_change_key_to_float
        """

        input_1 = {"a": 1, "1": 2, "1.0": 3, "b": {4: 10, "5": 1}}
        output_1 = recursive_change_key_to_float(input_1)

        desired_output_1 = OrderedDict(
            [("a", 1), (1.0, 3), ("b", OrderedDict([(4.0, 10), (5.0, 1)]))]
        )

        self.assertEqual(output_1, desired_output_1)


class test_recursive_change_key_to_string(unittest.TestCase):
    """
    Unittests for function recursive_change_key_to_string
    """

    def test_recursive_change_key_to_string(self):
        with Capturing() as output:
            self._test_recursive_change_key_to_string()

    def _test_recursive_change_key_to_string(self):
        """
        Test recursive_change_key_to_string
        """

        input_1 = {"a": 1, "1": 2, "1.0": 3, "b": {4: 10, "5": 1, 6: 10}}
        output_1 = recursive_change_key_to_string(input_1, "{:.2E}")

        desired_output_1 = OrderedDict(
            [
                ("a", 1),
                ("1.00E+00", 3),
                (
                    "b",
                    OrderedDict([("4.00E+00", 10), ("5.00E+00", 1), ("6.00E+00", 10)]),
                ),
            ]
        )

        self.assertEqual(output_1, desired_output_1)


class test_multiply_float_values(unittest.TestCase):
    """
    Unittests for function multiply_float_values
    """

    def test_multiply_float_values(self):
        with Capturing() as output:
            self._test_multiply_float_values()

    def _test_multiply_float_values(self):
        """
        Test multiply_float_values
        """

        # Test with all valid input
        input_1 = {1: 2.2, "2": {"a": 2, "b": 10, "c": 0.5}}
        multiply_float_values(input_1, 2)
        desired_output_1 = {1: 4.4, "2": {"a": 2, "b": 10, "c": 1.0}}

        #
        self.assertEqual(input_1, desired_output_1)

        # Test with unrecognised input:
        input_2 = {1: 2.2, "2": {"a": 2, "b": 10, "c": 0.5, "d": dummy("david")}}
        _ = multiply_float_values(input_2, 2)


class test_subtract_dicts(unittest.TestCase):
    """
    Unittests for function subtract_dicts
    """

    def test_empty(self):
        with Capturing() as output:
            self._test_empty()

    def _test_empty(self):
        """
        Test subtract_dicts with an empty dict
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "dict": {"int": 1, "float": 1.2},
        }
        dict_2 = {}
        output_dict = subtract_dicts(input_dict, dict_2)
        self.assertTrue(output_dict == input_dict)

    def test_unequal_types(self):
        with Capturing() as output:
            self._test_unequal_types()

    def _test_unequal_types(self):
        """
        Test subtract_dicts with unequal types: should raise valueError
        """

        dict_1 = {"input": 10}
        dict_2 = {"input": "hello"}

        self.assertRaises(ValueError, subtract_dicts, dict_1, dict_2)

    def test_ints(self):
        with Capturing() as _:
            self._test_ints()

    def _test_ints(self):
        """
        Test subtract_dicts with ints
        """

        dict_1 = {"int": 2}
        dict_2 = {"int": 1}
        output_dict = subtract_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["int"], int))
        self.assertEqual(output_dict["int"], 1)

    def test_floats(self):
        with Capturing() as output:
            self._test_floats()

    def _test_floats(self):
        """
        Test subtract_dicts with floats
        """

        dict_1 = {"float": 4.5}
        dict_2 = {"float": 4.6}
        output_dict = subtract_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["float"], float))
        self.assertAlmostEqual(output_dict["float"], -0.1, 2)

    def test_zero_result(self):
        with Capturing() as output:
            self._test_zero_result()

    def _test_zero_result(self):
        """
        Test subtract_dicts resulting in a 0 value. which should be removed
        """

        dict_1 = {"a": 4, "b": 0, "d": 1.0}
        dict_2 = {"a": 4, "c": 0, "d": 1}
        output_dict = subtract_dicts(dict_1, dict_2)

        self.assertIsInstance(output_dict, dict)
        self.assertFalse(output_dict)

    def test_unsupported(self):
        with Capturing() as output:
            self._test_unsupported()

    def _test_unsupported(self):
        """
        Test merging dict with lists
        """

        dict_1 = {"list": [1, 2], "b": [1]}
        dict_2 = {"list": [3, 4], "c": [1]}

        self.assertRaises(ValueError, subtract_dicts, dict_1, dict_2)

    def test_dicts(self):
        with Capturing() as _:
            self._test_dicts()

    def _test_dicts(self):
        """
        Test merging dict with dicts
        """

        dict_1 = {"dict": {"a": 1, "b": 1}}
        dict_2 = {"dict": {"a": 2, "c": 2}}
        output_dict = subtract_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["dict"], dict))
        self.assertEqual(output_dict["dict"], {"a": -1, "b": 1, "c": -2})


class test_update_dicts(unittest.TestCase):
    """
    Unittests for function update_dicts
    """

    def test_dicts(self):
        with Capturing() as _:
            self._test_dicts()

    def _test_dicts(self):
        """
        Test update_dicts with dicts
        """

        dict_1 = {"dict": {"a": 1, "b": 1}}
        dict_2 = {"dict": {"a": 2, "c": 2}}
        output_dict = update_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["dict"], dict))
        self.assertEqual(output_dict["dict"], {"a": 2, "b": 1, "c": 2})

    def test_unsupported(self):
        with Capturing() as output:
            self._test_unsupported()

    def _test_unsupported(self):
        """
        Test update_dicts with unsupported types
        """

        dict_1 = {"list": 2, "b": [1]}
        dict_2 = {"list": [3, 4], "c": [1]}

        self.assertRaises(ValueError, update_dicts, dict_1, dict_2)


class test__nested_get(unittest.TestCase):
    """
    Unittests for function _nested_get
    """

    def test__nested_get(self):
        with Capturing() as output:
            self._test__nested_get()

    def _test__nested_get(self):
        """
        Test _nested_get
        """

        input_1 = {"a": {"b": 2}}

        output_1 = _nested_get(input_1, ["a"])
        output_2 = _nested_get(input_1, ["a", "b"])

        self.assertEqual(output_1, {"b": 2})
        self.assertEqual(output_2, 2)


class test__nested_set(unittest.TestCase):
    """
    Unittests for function _nested_set
    """

    def test__nested_set(self):
        with Capturing() as output:
            self._test__nested_set()

    def _test__nested_set(self):
        """
        Test _nested_set
        """

        #
        input_1 = {"a": 0}
        desired_output_1 = {"a": 2}
        _nested_set(input_1, ["a"], 2)
        self.assertEqual(input_1, desired_output_1)

        #
        input_2 = {"a": {"b": 0}}
        desired_output_2 = {"a": {"b": 2}}
        _nested_set(input_2, ["a", "b"], 2)
        self.assertEqual(input_2, desired_output_2)

        #
        input_3 = {"a": {"b": 0}}
        desired_output_3 = {"a": {"b": 0, "d": {"c": 10}}}
        _nested_set(input_3, ["a", "d", "c"], 10)
        self.assertEqual(input_3, desired_output_3)


if __name__ == "__main__":
    unittest.main()
