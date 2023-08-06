"""
Unittests for useful_funcs module
"""

import unittest
import numpy as np

from binarycpython.utils.functions import (
    Capturing,
)

from binarycpython.utils.useful_funcs import (
    zams_collision,
    rzams,
    roche_lobe,
    ragb,
    calc_sep_from_period,
    calc_period_from_sep,
)


class test_calc_period_from_sep(unittest.TestCase):
    """
    Unittests for function calc_period_from_sep

    TODO: add tests comparing to .e.g astropy results
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        output_1 = calc_period_from_sep(1, 1, 1)
        self.assertEqual(output_1, 0.08188845248066838)


class test_calc_sep_from_period(unittest.TestCase):
    """
    Unittests for function calc_sep_from_period

    TODO: add tests comparing to .e.g astropy results
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        output_1 = calc_sep_from_period(1, 1, 1)
        self.assertEqual(output_1, 5.302958446503317)


class test_roche_lobe(unittest.TestCase):
    """
    Unittests for function roche_lobe
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        mass_donor = 2
        mass_accretor = 1

        output_1 = roche_lobe(mass_accretor / mass_donor)
        print(output_1)

        self.assertLess(np.abs(output_1 - 0.3207881203346875), 1e-10)


class test_ragb(unittest.TestCase):
    """
    Unittests for function ragb
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        m = 20
        output = ragb(m)

        self.assertEqual(output, 820)


class test_rzams(unittest.TestCase):
    """
    Unittests for function rzams
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        mass = 0.5
        metallicity = 0.02
        output_1 = rzams(mass, metallicity)

        self.assertLess(np.abs(output_1 - 0.458757762074762), 1e-7)

        mass = 12.5
        metallicity = 0.01241
        output_2 = rzams(mass, metallicity)

        self.assertLess(np.abs(output_2 - 4.20884329861741), 1e-7)

        mass = 149
        metallicity = 0.001241
        output_3 = rzams(mass, metallicity)

        self.assertLess(np.abs(output_3 - 12.8209978916491), 1e-7)


class test_zams_collission(unittest.TestCase):
    """
    Unittests for function zams_collission
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        mass1 = 1
        mass2 = 10
        sep = 10
        eccentricity = 0
        metallicity = 0.02

        output_collision_1 = zams_collision(
            mass1, mass2, sep, eccentricity, metallicity
        )
        self.assertTrue(output_collision_1 == 0)

        sep = 1
        output_collision_2 = zams_collision(
            mass1, mass2, sep, eccentricity, metallicity
        )
        self.assertTrue(output_collision_2 == 1)


if __name__ == "__main__":
    unittest.main()
