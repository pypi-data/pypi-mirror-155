"""
Unittests for the c-bindings
"""

import os
import sys
import time
import json
import textwrap
import unittest
import numpy as np

from binarycpython import _binary_c_bindings

from binarycpython.utils.functions import (
    temp_dir,
    verbose_print,
    is_capsule,
    Capturing,
)
from binarycpython.utils.ensemble import (
    BinarycDecoder,
    handle_ensemble_string_to_json,
    extract_ensemble_json_from_string,
)
from binarycpython.utils.dicts import (
    inspect_dict,
    merge_dicts,
)


TMP_DIR = temp_dir("tests", "test_c_bindings")

#### some useful functions
def return_argstring(
    m1=15.0,
    m2=14.0,
    separation=0,
    orbital_period=453000000000,
    eccentricity=0.0,
    metallicity=0.02,
    max_evolution_time=15000,
    defer_ensemble=0,
    ensemble_filters_off=1,
    ensemble_filter="SUPERNOVAE",
):
    """
    Function to make a argstring that we can use in these tests
    """

    # Make the argstrings
    argstring_template = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} \
eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g} ensemble 1 ensemble_defer {7} \
ensemble_filters_off {8} ensemble_filter_{9} 1 probability 0.1 ensemble_dt 1000"

    argstring = argstring_template.format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
        defer_ensemble,
        ensemble_filters_off,
        ensemble_filter,
    )

    return argstring


#######################################################################################################################################################
### General run_system test
#######################################################################################################################################################


class test_run_system(unittest.TestCase):
    """
    Unit test for run_system
    """

    def test_output(self):
        with Capturing() as output:
            self._test_output()

    def _test_output(self):
        """
        General test if run_system works
        """
        print(self.id())

        m1 = 15.0  # Msun
        m2 = 14.0  # Msun
        separation = 0  # 0 = ignored, use period
        orbital_period = 4530.0  # days
        eccentricity = 0.0
        metallicity = 0.02
        max_evolution_time = 15000
        argstring = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g}  ".format(
            m1,
            m2,
            separation,
            orbital_period,
            eccentricity,
            metallicity,
            max_evolution_time,
        )

        output = _binary_c_bindings.run_system(argstring=argstring)

        self.assertIn(
            "SINGLE_STAR_LIFETIME",
            output,
            msg="Output didn't contain SINGLE_STAR_LIFETIME",
        )


#######################################################################################################################################################
### memaddr test
#######################################################################################################################################################


class test_return_store_memaddr(unittest.TestCase):
    """
    Unit test for return_store_memaddr
    """

    def test_return_store_memaddr(self):
        with Capturing() as output:
            self._test_return_store_memaddr()

    def _test_return_store_memaddr(self):
        """
        Test to see if the memory adress is returned properly
        """

        output = _binary_c_bindings.return_store_memaddr()

        # print("function: test_return_store")
        # print("store memory adress:")
        # print(textwrap.indent(str(output), "\t"))

        self.assertTrue(is_capsule(output))
        # self.assertNotEqual(
        #     output, 0, "memory adress seems not to have a correct value"
        # )

        # TODO: check if we can built in some signal for how successful this was.
        _ = _binary_c_bindings.free_store_memaddr(output)


#######################################################################################################################################################
### ensemble tests
#######################################################################################################################################################


class test_ensemble_functions(unittest.TestCase):
    """
    Unittests for handling the ensemble outputs and adding those
    """

    def __init__(self, *args, **kwargs):
        """
        init function
        """
        super(test_ensemble_functions, self).__init__(*args, **kwargs)

    def test_return_persistent_data_memaddr(self):
        with Capturing() as output:
            self._test_return_persistent_data_memaddr()

    def _test_return_persistent_data_memaddr(self):
        """
        Test case to check if the memory adress has been created succesfully
        """
        print(self.id())

        output = _binary_c_bindings.return_persistent_data_memaddr()

        self.assertTrue(is_capsule(output), msg="Object must be a capsule")

    def test_minimal_ensemble_output(self):
        with Capturing() as output:
            self._test_minimal_ensemble_output()

    def _test_minimal_ensemble_output(self):
        """
        test_case to check if the ensemble output is correctly output
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1,
            m2=m2,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=0,  # no defer to memory location. just output it
        )

        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)

        # Check if the ENSEMBLE_JSON is uberhaubt in the output
        self.assertIn("ENSEMBLE_JSON", output_1)

        test_json = extract_ensemble_json_from_string(output_1)
        self.assertIn("number_counts", test_json)
        self.assertNotEqual(test_json["number_counts"], {})

    def test_minimal_ensemble_output_defer(self):
        with Capturing() as output:
            self._test_minimal_ensemble_output_defer()

    def _test_minimal_ensemble_output_defer(self):
        """
        test_case to check if the ensemble output is correctly output, by using defer command and freeing+outputting
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=1,  # no defer to memory location. just output it
        )

        output_1 = _binary_c_bindings.run_system(
            argstring=argstring_1, persistent_data_memaddr=persistent_data_memaddr
        )

        #
        self.assertNotIn("ENSEMBLE_JSON", output_1)

        # free memory and output the stuff.
        raw_json_output = (
            _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                persistent_data_memaddr
            )
        )
        ensemble_json_output = extract_ensemble_json_from_string(raw_json_output)

        self.assertIn("number_counts", ensemble_json_output)
        self.assertNotEqual(ensemble_json_output["number_counts"], {})

    def test_add_ensembles_direct(self):
        with Capturing() as output:
            self._test_add_ensembles_direct()

    def _test_add_ensembles_direct(self):
        """
        test_case to check if adding the ensemble outputs works. Many things should be caught by tests in the merge_dict test, but still good to test a bit here
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",  # no defer to memory location. just output it
        )
        argstring_2 = return_argstring(
            m1=10,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",  # no defer to memory location. just output it
        )

        #
        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        output_2 = _binary_c_bindings.run_system(argstring=argstring_2)

        #
        output_json_1 = extract_ensemble_json_from_string(output_1)
        output_json_2 = extract_ensemble_json_from_string(output_2)

        #
        merged_dict = merge_dicts(output_json_1, output_json_2)

        self.assertIn("number_counts", merged_dict)
        self.assertIn("stellar_type", merged_dict["number_counts"])

        for key in output_json_1["number_counts"]["stellar_type"]["0"]:
            self.assertIn(key, merged_dict["number_counts"]["stellar_type"]["0"])

        for key in output_json_2["number_counts"]["stellar_type"]["0"]:
            self.assertIn(key, merged_dict["number_counts"]["stellar_type"]["0"])

        # compare stuff:
        self.assertLess(
            np.abs(
                output_json_1["number_counts"]["stellar_type"]["0"]["CHeB"]
                + output_json_2["number_counts"]["stellar_type"]["0"]["CHeB"]
                - merged_dict["number_counts"]["stellar_type"]["0"]["CHeB"]
            ),
            1e-10,
        )
        self.assertLess(
            np.abs(
                output_json_1["number_counts"]["stellar_type"]["0"]["MS"]
                + output_json_2["number_counts"]["stellar_type"]["0"]["MS"]
                - merged_dict["number_counts"]["stellar_type"]["0"]["MS"]
            ),
            1e-10,
        )

    def test_compare_added_systems_with_double_deferred_systems(self):
        with Capturing() as output:
            self._test_compare_added_systems_with_double_deferred_systems()

    def _test_compare_added_systems_with_double_deferred_systems(self):
        """
        test to run 2 systems without deferring, and merging them manually. Then run 2 systems with defer and then output them.
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",  # no defer to memory location. just output it
        )
        argstring_2 = return_argstring(
            m1=10,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",  # no defer to memory location. just output it
        )

        #
        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        output_2 = _binary_c_bindings.run_system(argstring=argstring_2)

        #
        output_json_1 = extract_ensemble_json_from_string(output_1)
        output_json_2 = extract_ensemble_json_from_string(output_2)

        #
        merged_dict = merge_dicts(output_json_1, output_json_2)

        ###############################
        # Deferred setup
        persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

        argstring_1_deferred = return_argstring(
            m1=m1,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=1,  # no defer to memory location. just output it
        )
        argstring_2_deferred = return_argstring(
            m1=10,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=1,  # no defer to memory location. just output it
        )

        # run
        _ = _binary_c_bindings.run_system(
            argstring=argstring_1_deferred,
            persistent_data_memaddr=persistent_data_memaddr,
        )
        _ = _binary_c_bindings.run_system(
            argstring=argstring_2_deferred,
            persistent_data_memaddr=persistent_data_memaddr,
        )

        # output
        raw_json_output = (
            _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                persistent_data_memaddr
            )
        )
        ensemble_json_output = extract_ensemble_json_from_string(raw_json_output)

        # CHeck all keys are present
        for key in merged_dict["number_counts"]["stellar_type"]["0"]:
            self.assertIn(
                key, ensemble_json_output["number_counts"]["stellar_type"]["0"]
            )

        # Check if they are of the same value
        for key in merged_dict["number_counts"]["stellar_type"]["0"]:
            self.assertLess(
                np.abs(
                    merged_dict["number_counts"]["stellar_type"]["0"][key]
                    - ensemble_json_output["number_counts"]["stellar_type"]["0"][key]
                ),
                1e-10,
            )

    def test_combine_with_empty_json(self):
        with Capturing() as output:
            self._test_combine_with_empty_json()

    def _test_combine_with_empty_json(self):
        """
        Test for merging with an empty dict
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        argstring_1 = return_argstring(
            m1=m1,
            m2=m2,
            orbital_period=1000000000,
            ensemble_filter="STELLAR_TYPE_COUNTS",  # no defer to memory location. just output it
        )

        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)

        output_json_1 = extract_ensemble_json_from_string(output_1)

        assert_message = "combining output json with empty dict should give same result as initial json"

        self.assertEqual(merge_dicts(output_json_1, {}), output_json_1, assert_message)

    #############

    def test_full_ensemble_output(self):
        with Capturing() as output:
            self._test_full_ensemble_output()

    def _test_full_ensemble_output(self):
        """
        Function to just output the whole ensemble
        """
        print(self.id())

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        argstring_1 = return_argstring(
            m1=m1, m2=m2, orbital_period=1000000000, ensemble_filter=0
        )
        argstring_1 = return_argstring(defer_ensemble=0, ensemble_filters_off=0)

        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)

        #
        output_json_1 = extract_ensemble_json_from_string(output_1)

        keys = output_json_1.keys()

        # assert statements:
        self.assertIn("number_counts", keys)
        self.assertIn("HRD", keys)
        self.assertIn("HRD(t)", keys)
        self.assertIn("distributions", keys)
        self.assertIn("scalars", keys)


#######################################################################################################################################################
### ensemble tests
#######################################################################################################################################################

if __name__ == "__main__":
    unittest.main()
