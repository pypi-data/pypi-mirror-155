"""
Unittests for grid_options_defaults module

TODO: get_grid_options_defaults_dict
TODO: get_grid_options_descriptions
TODO: print_option_descriptions
TODO: default_cache_dir
"""
import os
import unittest

from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
)
from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_grid_options_defaults")


class test_grid_options_help(unittest.TestCase):
    """
    Unit tests for the grid_options_help function
    """

    def test_grid_options_help(self):
        with Capturing() as output:
            self._test_grid_options_help()

    def _test_grid_options_help(self):
        """
        Unit tests for the grid_options_help function
        """

        grid_options_defaults_pop = Population()

        input_1 = "aa"
        result_1 = grid_options_defaults_pop.grid_options_help(input_1)
        self.assertEqual(result_1, {}, msg="Dict should be empty")

        input_2 = "num_cores"
        result_2 = grid_options_defaults_pop.grid_options_help(input_2)
        self.assertIn(
            input_2,
            result_2,
            msg="{} should be in the keys of the returned dict".format(input_2),
        )
        self.assertNotEqual(
            result_2[input_2], "", msg="description should not be empty"
        )

        input_3 = "evolution_type"
        result_3 = grid_options_defaults_pop.grid_options_help(input_3)
        self.assertIn(
            input_3,
            result_3,
            msg="{} should be in the keys of the returned dict".format(input_3),
        )
        # self.assertEqual(result_3[input_3], "", msg="description should be empty")


class test_grid_options_description_checker(unittest.TestCase):
    """
    Unit tests for the grid_options_description_checker function
    """

    def test_grid_options_description_checker(self):
        with Capturing() as output:
            self._test_grid_options_description_checker()

    def _test_grid_options_description_checker(self):
        """
        Unit tests for the grid_options_description_checker function
        """

        grid_options_defaults_pop = Population()

        output_1 = grid_options_defaults_pop.grid_options_description_checker(
            print_info=True
        )

        self.assertTrue(isinstance(output_1, int))
        self.assertTrue(output_1 > 0)


class test_write_grid_options_to_rst_file(unittest.TestCase):
    """
    Unit tests for the write_grid_options_to_rst_file function
    """

    def test_write_grid_options_to_rst_file(self):
        with Capturing() as output:
            self._test_write_grid_options_to_rst_file()

    def _test_write_grid_options_to_rst_file(self):
        """
        Unit tests for the grid_options_description_checker function
        """

        grid_options_defaults_pop = Population()

        input_1 = os.path.join(TMP_DIR, "test_write_grid_options_to_rst_file_1.txt")
        self.assertRaises(
            ValueError,
            grid_options_defaults_pop.write_grid_options_to_rst_file,
            input_1,
        )

        input_2 = os.path.join(TMP_DIR, "test_write_grid_options_to_rst_file_2.rst")
        _ = grid_options_defaults_pop.write_grid_options_to_rst_file(input_2)

        self.assertTrue(os.path.isfile(input_2))


if __name__ == "__main__":
    unittest.main()
