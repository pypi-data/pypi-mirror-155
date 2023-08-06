"""
Unittests for gridcode module

TODO: _gridcode_filename
TODO: _add_code
TODO: _indent_block
TODO: _increment_indent_depth
TODO: _generate_grid_code
TODO: _write_gridcode_system_call
TODO: _load_grid_function
TODO: _last_grid_variable
TODO: update_grid_variable
TODO: delete_grid_variable
TODO: rename_grid_variable
"""

import unittest

from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
)

from binarycpython.utils.grid import Population


class test_add_grid_variable(unittest.TestCase):
    """
    Unittests for add_grid_variable function
    """

    def test_add_grid_variable(self):
        with Capturing() as output:
            self._test_add_grid_variable()

    def _test_add_grid_variable(self):
        """
        Unittests for the function add_grid_variable

        TODO: Should I test more here?
        """

        test_pop = Population()

        resolution = {"M_1": 10, "q": 10}

        test_pop.add_grid_variable(
            name="lnm1",
            longname="Primary mass",
            valuerange=[1, 100],
            samplerfunc="const(math.log(1), math.log(100), {})".format(
                resolution["M_1"]
            ),
            precode="M_1=math.exp(lnm1)",
            probdist="three_part_powerlaw(M_1, 0.1, 0.5, 1.0, 100, -1.3, -2.3, -2.3)*M_1",
            dphasevol="dlnm1",
            parameter_name="M_1",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        test_pop.add_grid_variable(
            name="q",
            longname="Mass ratio",
            valuerange=["0.1/M_1", 1],
            samplerfunc="const(0.1/M_1, 1, {})".format(resolution["q"]),
            probdist="flatsections(q, [{'min': 0.1/M_1, 'max': 1.0, 'height': 1}])",
            dphasevol="dq",
            precode="M_2 = q * M_1",
            parameter_name="M_2",
            condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        )

        self.assertIn("q", test_pop.grid_options["_grid_variables"])
        self.assertIn("lnm1", test_pop.grid_options["_grid_variables"])
        self.assertEqual(len(test_pop.grid_options["_grid_variables"]), 2)


if __name__ == "__main__":
    unittest.main()
