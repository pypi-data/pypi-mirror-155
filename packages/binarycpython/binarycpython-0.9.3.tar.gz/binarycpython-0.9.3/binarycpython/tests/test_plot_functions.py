"""
Unittests for plot_functions
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt

from binarycpython.utils.plot_functions import *
from binarycpython.utils.functions import Capturing


class test_color_by_index(unittest.TestCase):
    """
    Unittests for function color_by_index
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        First test
        """

        colors = ["red", "white", "blue"]

        color = color_by_index([1, 2, 3], 1, colors)
        self.assertTrue(color == "blue")


class test_plot_system(unittest.TestCase):
    """
    Unittests for function
    """

    def test_mass_evolution_plot(self):
        with Capturing() as output:
            self._test_mass_evolution_plot()

    def _test_mass_evolution_plot(self):
        """
        Test for setting plot_type = "mass_evolution"
        """

        plot_type = "mass_evolution"
        show_plot = False
        output_fig_1 = plot_system(
            plot_type,
            show_plot=show_plot,
            M_1=1,
            metallicity=0.002,
            M_2=0.1,
            separation=0,
            orbital_period=100000000000,
        )

        fig, ax = plt.subplots(nrows=1)
        self.assertTrue(type(output_fig_1) == fig.__class__)

        # with stellar types
        # plot_type = 'mass_evolution'
        # show_plot = False
        # show_stellar_types = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, show_stellar_types=show_stellar_types, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

        # fig, ax = plt.subplots(nrows=1)
        # self.assertTrue(type(output_fig_2)==fig.__class__)

        # # show plot
        # show_plot = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

    def test_orbit_evolution_plot(self):
        with Capturing() as output:
            self._test_orbit_evolution_plot()

    def _test_orbit_evolution_plot(self):
        """
        Test for setting plot_type = "orbit_evolution"
        """

        plot_type = "orbit_evolution"
        show_plot = False
        output_fig_1 = plot_system(
            plot_type,
            show_plot=show_plot,
            M_1=1,
            metallicity=0.002,
            M_2=0.1,
            separation=0,
            orbital_period=100000000000,
        )

        fig, ax = plt.subplots(nrows=1)
        self.assertTrue(type(output_fig_1) == fig.__class__)

        # with stellar types
        # plot_type = 'orbit_evolution'
        # show_plot = False
        # show_stellar_types = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, show_stellar_types=show_stellar_types, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

        # fig, ax = plt.subplots(nrows=1)
        # self.assertTrue(type(output_fig_2)==fig.__class__)

        # # show plot
        # show_plot = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

    def test_hr_diagram_plot(self):
        with Capturing() as output:
            self._test_hr_diagram_plot()

    def _test_hr_diagram_plot(self):
        """
        Test for setting plot_type = "hr_diagram"
        """

        plot_type = "hr_diagram"
        show_plot = False
        output_fig_1 = plot_system(
            plot_type,
            show_plot=show_plot,
            M_1=1,
            metallicity=0.002,
            M_2=0.1,
            separation=0,
            orbital_period=100000000000,
        )

        fig, ax = plt.subplots(nrows=1)
        self.assertTrue(type(output_fig_1) == fig.__class__)

        # with stellar types
        # plot_type = 'hr_diagram'
        # show_plot = False
        # show_stellar_types = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, show_stellar_types=show_stellar_types, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

        # fig, ax = plt.subplots(nrows=1)
        # self.assertTrue(type(output_fig_2)==fig.__class__)

        # # show plot
        # show_plot = True
        # output_fig_2 = plot_system(plot_type, show_plot=show_plot, M_1=1, metallicity=0.002, M_2=0.1, separation=0, orbital_period=100000000000)

    def test_unknown_plottype(self):
        with Capturing() as output:
            self._test_unknown_plottype()

    def _test_unknown_plottype(self):
        """
        Test for non-existant setting plot_type = "hr_diagram"
        """

        plot_type = "random"
        self.assertRaises(ValueError, plot_system, plot_type)


if __name__ == "__main__":
    unittest.main()
