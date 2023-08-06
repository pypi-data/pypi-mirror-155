"""
Module containing the unittests for the distribution functions. 

TODO: powerlaw_constant_nocache
TODO: powerlaw_constant
TODO: calculate_constants_three_part_powerlaw
TODO: gaussian_normalizing_const
TODO: gaussian_func
TODO: sana12
TODO: interpolate_in_mass_izzard2012
TODO: cosmic_SFH_madau_dickinson2014
TODO: poisson
TODO: _poisson

TODO: get_max_multiplicity
TODO: merge_multiplicities
TODO: Moe_di_Stefano_2017_multiplicity_fractions
TODO: build_q_table
TODO: powerlaw_extrapolation_q
TODO: linear_extrapolation_q
TODO: get_integration_constant_q
TODO: fill_data
TODO: calc_e_integral
TODO: calc_P_integral
TODO: calc_total_probdens
TODO: Moe_di_Stefano_2017_pdf
"""

import unittest
import numpy as np

from binarycpython.utils.useful_funcs import calc_sep_from_period
from binarycpython.utils.functions import Capturing, temp_dir

from binarycpython.utils.grid import Population

TMP_DIR = temp_dir("tests", "test_distributions")

MASS_LIST = [0.1, 0.2, 1, 10, 15, 50]
LOGPER_LIST = [-2, -0.5, 1.6, 2.5, 5.3, 10]
Q_LIST = [0.01, 0.2, 0.4, 0.652, 0.823, 1]
PER_LIST = [10 ** logper for logper in LOGPER_LIST]
TOLERANCE = 1e-5


class test_flat(unittest.TestCase):
    """
    Class for unit test of flat
    """

    def test_flat(self):
        with Capturing() as output:
            self._test_flat()

    def _test_flat(self):
        """
        Unittest for the function flat
        """

        distribution_functions_pop = Population()

        output_1 = distribution_functions_pop.flat()

        self.assertTrue(isinstance(output_1, float))
        self.assertEqual(output_1, 1.0)


class test_number(unittest.TestCase):
    """
    Class for unit test of number
    """

    def test_number(self):
        with Capturing() as output:
            self._test_number()

    def _test_number(self):
        """
        Unittest for function number
        """

        distribution_functions_pop = Population()

        input_1 = 1.0
        output_1 = distribution_functions_pop.number(input_1)

        self.assertEqual(input_1, output_1)


class test_const_distribution(unittest.TestCase):
    """
    Class for unit test of number
    """

    def test_const_distribution(self):
        with Capturing() as output:
            self._test_const_distribution()

    def _test_const_distribution(self):
        """
        Unittest for function const
        """

        distribution_functions_pop = Population()

        output_1 = distribution_functions_pop.const_distribution(
            min_bound=0, max_bound=2
        )
        self.assertEqual(
            output_1, 0.5, msg="Value should be 0.5, but is {}".format(output_1)
        )

        output_2 = distribution_functions_pop.const_distribution(
            min_bound=0, max_bound=2, val=3
        )
        self.assertEqual(
            output_2, 0, msg="Value should be 0, but is {}".format(output_2)
        )


class test_powerlaw(unittest.TestCase):
    """
    Class for unit test of powerlaw
    """

    def test_powerlaw(self):
        with Capturing() as output:
            self._test_powerlaw()

    def _test_powerlaw(self):
        """
        unittest for the powerlaw test
        """

        distribution_functions_pop = Population()

        perl_results = [
            0,
            0,
            1.30327367546194,
            0.00653184128064016,
            0.00257054805572128,
            0.000161214690242696,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(
                distribution_functions_pop.powerlaw(1, 100, -2.3, mass)
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass, per: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(np.abs(python_results[i] - perl_results[i]), TOLERANCE)

        # extra test for k = -1
        self.assertRaises(
            ValueError, distribution_functions_pop.powerlaw, 1, 100, -1, 10
        )


class test_three_part_power_law(unittest.TestCase):
    """
    Class for unit test of three_part_power_law
    """

    def test_three_part_power_law(self):
        with Capturing() as output:
            self._test_three_part_power_law()

    def _test_three_part_power_law(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            10.0001044752901,
            2.03065220596677,
            0.0501192469795434,
            0.000251191267451594,
            9.88540897458207e-05,
            6.19974072148769e-06,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(
                distribution_functions_pop.three_part_powerlaw(
                    mass, 0.08, 0.1, 1, 300, -1.3, -2.3, -2.3
                )
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass, per: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )

        # Extra test:
        # M < M0
        self.assertTrue(
            distribution_functions_pop.three_part_powerlaw(
                0.05, 0.08, 0.1, 1, 300, -1.3, -2.3, -2.3
            )
            == 0,
            msg="Probability should be zero as M < M0",
        )


class test_Kroupa2001(unittest.TestCase):
    """
    Class for unit test of Kroupa2001
    """

    def test_Kroupa2001(self):
        with Capturing() as output:
            self._test_Kroupa2001()

    def _test_Kroupa2001(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0,  # perl value is actually 5.71196495365248
            2.31977861075353,
            0.143138195684851,
            0.000717390363216896,
            0.000282322598503135,
            1.77061658757533e-05,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(distribution_functions_pop.Kroupa2001(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )

        # Extra tests:
        self.assertEqual(
            distribution_functions_pop.Kroupa2001(10, newopts={"mmax": 300}),
            distribution_functions_pop.three_part_powerlaw(
                10, 0.1, 0.5, 1, 300, -1.3, -2.3, -2.3
            ),
        )


class test_ktg93(unittest.TestCase):
    """
    Class for unit test of ktg93
    """

    def test_ktg93(self):
        with Capturing() as output:
            self._test_ktg93()

    def _test_ktg93(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0,  # perl value is actually 5.79767807698379 but that is not correct
            2.35458895566605,
            0.155713799148675,
            0.000310689875361984,
            0.000103963454405194,
            4.02817276824841e-06,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(distribution_functions_pop.ktg93(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )

        # extra test:
        self.assertEqual(
            distribution_functions_pop.ktg93(10, newopts={"mmax": 300}),
            distribution_functions_pop.three_part_powerlaw(
                10, 0.1, 0.5, 1, 300, -1.3, -2.2, -2.7
            ),
        )


class test_imf_tinsley1980(unittest.TestCase):
    """
    Class for unit test of imf_tinsley1980
    """

    def test_imf_tinsley1980(self):
        with Capturing() as output:
            self._test_imf_tinsley1980()

    def _test_imf_tinsley1980(self):
        """
        Unittest for function imf_tinsley1980
        """

        distribution_functions_pop = Population()

        m = 1.2
        self.assertEqual(
            distribution_functions_pop.imf_tinsley1980(m),
            distribution_functions_pop.three_part_powerlaw(
                m, 0.1, 2.0, 10.0, 80.0, -2.0, -2.3, -3.3
            ),
        )


class test_imf_scalo1986(unittest.TestCase):
    """
    Class for unit test of imf_scalo1986
    """

    def test_imf_scalo1986(self):
        with Capturing() as output:
            self._test_imf_scalo1986()

    def _test_imf_scalo1986(self):
        """
        Unittest for function imf_scalo1986
        """

        distribution_functions_pop = Population()

        m = 1.2
        self.assertEqual(
            distribution_functions_pop.imf_scalo1986(m),
            distribution_functions_pop.three_part_powerlaw(
                m, 0.1, 1.0, 2.0, 80.0, -2.35, -2.35, -2.70
            ),
        )


class test_imf_scalo1998(unittest.TestCase):
    """
    Class for unit test of imf_scalo1998
    """

    def test_imf_scalo1998(self):
        with Capturing() as output:
            self._test_imf_scalo1998()

    def _test_imf_scalo1998(self):
        """
        Unittest for function imf_scalo1986
        """

        distribution_functions_pop = Population()

        m = 1.2
        self.assertEqual(
            distribution_functions_pop.imf_scalo1998(m),
            distribution_functions_pop.three_part_powerlaw(
                m, 0.1, 1.0, 10.0, 80.0, -1.2, -2.7, -2.3
            ),
        )


class test_imf_chabrier2003(unittest.TestCase):
    """
    Class for unit test of imf_chabrier2003
    """

    def test_imf_chabrier2003(self):
        with Capturing() as output:
            self._test_imf_chabrier2003()

    def _test_imf_chabrier2003(self):
        """
        Unittest for function imf_chabrier2003
        """

        distribution_functions_pop = Population()

        input_1 = 0
        self.assertRaises(
            ValueError, distribution_functions_pop.imf_chabrier2003, input_1
        )

        masses = [0.1, 0.2, 0.5, 1, 2, 10, 15, 50]
        perl_results = [
            5.64403964849588,
            2.40501495673496,
            0.581457346702825,
            0.159998782068074,
            0.0324898485372181,
            0.000801893469684309,
            0.000315578044662863,
            1.97918170035704e-05,
        ]
        python_results = [
            distribution_functions_pop.imf_chabrier2003(m) for m in masses
        ]

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass: {}".format(
                perl_results[i], python_results[i], str(masses[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


class test_duquennoy1991(unittest.TestCase):
    """
    Class for unit test of duquennoy1991
    """

    def test_duquennoy1991(self):
        with Capturing() as output:
            self._test_duquennoy1991()

    def _test_duquennoy1991(self):
        """
        Unittest for function duquennoy1991
        """

        distribution_functions_pop = Population()

        self.assertEqual(
            distribution_functions_pop.duquennoy1991(4.2),
            distribution_functions_pop.gaussian(4.2, 4.8, 2.3, -2, 12),
        )


class test_gaussian(unittest.TestCase):
    """
    Class for unit test of gaussian
    """

    def test_gaussian(self):
        with Capturing() as output:
            self._test_gaussian()

    def _test_gaussian(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0.00218800520299544,
            0.0121641269671571,
            0.0657353455837751,
            0.104951743573429,
            0.16899534495487,
            0.0134332780385336,
        ]
        python_results = []
        input_lists = []

        for logper in LOGPER_LIST:
            input_lists.append(logper)
            python_results.append(
                distribution_functions_pop.gaussian(logper, 4.8, 2.3, -2.0, 12.0)
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for logper: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )

        # Extra test:
        self.assertTrue(
            distribution_functions_pop.gaussian(15, 4.8, 2.3, -2.0, 12.0) == 0,
            msg="Probability should be 0 because the input period is out of bounds",
        )


class test_Arenou2010_binary_fraction(unittest.TestCase):
    """
    Class for unit test of Arenou2010_binary_fraction
    """

    def test_Arenou2010_binary_fraction(self):
        with Capturing() as output:
            self._test_Arenou2010_binary_fraction()

    def _test_Arenou2010_binary_fraction(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0.123079723518677,
            0.178895136157746,
            0.541178340047153,
            0.838798485820276,
            0.838799998443204,
            0.8388,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(
                distribution_functions_pop.Arenou2010_binary_fraction(mass)
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


class test_raghavan2010_binary_fraction(unittest.TestCase):
    """
    Class for unit test of raghavan2010_binary_fraction
    """

    def test_raghavan2010_binary_fraction(self):
        with Capturing() as output:
            self._test_raghavan2010_binary_fraction()

    def _test_raghavan2010_binary_fraction(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [0.304872297931597, 0.334079955706623, 0.41024, 1, 1, 1]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            input_lists.append(mass)
            python_results.append(
                distribution_functions_pop.raghavan2010_binary_fraction(mass)
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


class test_Izzard2012_period_distribution(unittest.TestCase):
    """
    Class for unit test of Izzard2012_period_distribution
    """

    def test_Izzard2012_period_distribution(self):
        with Capturing() as output:
            self._test_Izzard2012_period_distribution()

    def _test_Izzard2012_period_distribution(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            7.61631504133159e-09,
            0.168028727846997,
            0.130936282216512,
            0.0559170865520968,
            0.0100358604460285,
            0,
            2.08432736869149e-21,
            0.18713622563288,
            0.143151383185002,
            0.0676299576972089,
            0.0192427864870784,
            0,
            1.1130335685003e-24,
            0.194272603987661,
            0.14771508552257,
            0.0713078479280884,
            0.0221093965810181,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            for per in PER_LIST:
                input_lists.append([mass, per])

                python_results.append(
                    distribution_functions_pop.Izzard2012_period_distribution(per, mass)
                )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass, per: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


class test_flatsections(unittest.TestCase):
    """
    Class for unit test of flatsections
    """

    def test_flatsections(self):
        with Capturing() as output:
            self._test_flatsections()

    def _test_flatsections(self):
        """
        unittest for flatsections
        """

        distribution_functions_pop = Population()

        perl_results = [
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
        ]
        python_results = []
        input_lists = []

        for q in Q_LIST:
            input_lists.append(q)
            python_results.append(
                distribution_functions_pop.flatsections(
                    q, [{"min": 0.01, "max": 1.0, "height": 1.0}]
                )
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for q: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


class test_sana12(unittest.TestCase):
    """
    Class for unit test of sana12
    """

    def test_sana12(self):
        with Capturing() as output:
            self._test_sana12()

    def _test_sana12(self):
        """
        unittest for three_part_power_law
        """

        distribution_functions_pop = Population()

        perl_results = [
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
        ]
        python_results = []
        input_lists = []

        for mass in MASS_LIST:
            for q in Q_LIST:
                for per in PER_LIST:
                    mass_2 = mass * q

                    sep = calc_sep_from_period(mass, mass_2, per)
                    sep_min = calc_sep_from_period(mass, mass_2, 10 ** 0.15)
                    sep_max = calc_sep_from_period(mass, mass_2, 10 ** 5.5)

                    input_lists.append([mass, mass_2, per])

                    python_results.append(
                        distribution_functions_pop.sana12(
                            mass, mass_2, sep, per, sep_min, sep_max, 0.15, 5.5, -0.55
                        )
                    )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            msg = "Error: Value perl: {} Value python: {} for mass, mass2, per: {}".format(
                perl_results[i], python_results[i], str(input_lists[i])
            )
            self.assertLess(
                np.abs(python_results[i] - perl_results[i]), TOLERANCE, msg=msg
            )


if __name__ == "__main__":
    unittest.main()
