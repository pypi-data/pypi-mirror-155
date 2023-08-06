"""
Module that contains functionality to plot some properties of (binary) systems.

Different routines are defined here to plot orbits, masses, angular momenta etc.

Structure of file:
    custom logging strings
    parsing functions
    plotting functions
    master function: plot_system

All the loose components here can of course be used in other routines if you want.

There is no pre loaded matplotlib rc, you should do that yourself

These plotting routines are designed for binary systems, and admittedly they are here mostly for
inspirational purposes, since one would probably want to customise the plots.
Regardless, having some plotting routines in here seemed like a nice idea

Tasks
    TODO: This module is not finished yet.
    TODO: Make modules for single system
    TODO: Put all the plotting functions in here

"""

import math

import pandas as pd
import numpy as np
import astropy.constants as const

import matplotlib.pyplot as plt

from binarycpython.utils.functions import output_lines
from binarycpython.utils.run_system_wrapper import run_system
from binarycpython.utils.custom_logging_functions import binary_c_log_code

# Define the custom_logging_strings.
# These are kept to the minimum necessary for each plotting routine.

CUSTOM_LOGGING_STRING_MASSES = """
Printf("MASS_PLOTTING %30.12e %g %g %g %g %g %g\\n",
    //
    stardata->model.time, // 1
    
    // masses
    stardata->common.zero_age.mass[0], //
    stardata->common.zero_age.mass[1], //

    stardata->star[0].mass,
    stardata->star[1].mass,
    stardata->star[0].core_mass[ID_core(stardata->star[0].stellar_type)],
    stardata->star[1].core_mass[ID_core(stardata->star[1].stellar_type)]
);
"""

CUSTOM_LOGGING_STRING_ORBIT = """
Printf("ORBIT_PLOTTING %30.12e %g %g %g\\n",
    //
    stardata->model.time, // 1
    
    // orbit elements
    stardata->common.orbit.period, //2
    stardata->common.orbit.separation, //3
    stardata->common.orbit.eccentricity //4
    );
"""

CUSTOM_LOGGING_STRING_HR_DIAGRAM = """
Printf("HR_PLOTTING %30.12e %d %d %g %g %g %g %g %g\\n",
    //
    stardata->model.time, // 1
    
    // stellar types
    stardata->star[0].stellar_type, //2
    stardata->star[1].stellar_type, //3

    // luminosity and radii
    stardata->star[0].luminosity, // 4
    stardata->star[1].luminosity, // 5
    stardata->star[0].radius,     // 6
    stardata->star[1].radius,     // 7

    // masses
    stardata->common.zero_age.mass[0], // 8
    stardata->common.zero_age.mass[1]  // 9
    );
"""


def color_by_index(row, column, colors):
    """
    Function that returns a color based on row and column information. Used to color the stellar types
    """

    return colors[int(row[column])]


def plot_HR_diagram(
    df,
    show_stellar_types: bool = False,
    show_plot: bool = True,
    use_astropy_values: bool = True,
):
    """
    Function to plot the HR diagram evolution of the system. Assumes its a binary system.

    For a single star see plot_HR_diagram_single

    Plot shows Log luminosity on y axis,
    log temperature on x axis (reversed)

    requires:
        - time
        - stellar_type_1
        - stellar_type_2
        - radius_1
        - radius_2
        - luminosity_1
        - luminosity_2

    Plots:
        - luminosity_1 vs teff_1
        - luminosity_2 vs teff_2

    Tasks:
        - TODO: add HD limit
        - TODO: add lines of constant radius

    Args:
        df: pandas dataframe with the required columns
        show_stellar_types: whether to color code the tracks and show the stellar types
        show_plot: whether to actually show the plot. If false: returns the figure object
        use_astropy_values: Whether to use astropy values for for Rsun, Lsun and stefan boltzman constant.

    Returns
        returns a figure object if show_plot is false

    """

    # prefactor = (1/(4 * math.pi * omega_sb))**(1.0/4)
    # prefactor_approx = 1000 * (1130)**(1.0/4) * ((R_SUN**2)/L_SUN)**(1.0/4)

    if use_astropy_values:
        R_SUN = const.R_sun.cgs.value
        L_SUN = const.L_sun.cgs.value
        omega_sb = const.sigma_sb.cgs.value
        print(
            "Using astropy values: R_SUN= {} L_SUN = {} omega_sb = {}".format(
                R_SUN, L_SUN, omega_sb
            )
        )
    else:
        R_SUN = 6.956600000000000000000000000000e10
        L_SUN = 3.851500000000000274321803705319e33
        omega_sb = 5.670352798655924736991040813194e-05
        print(
            "Using binary_c values: R_SUN= {} L_SUN = {} omega_sb = {}".format(
                R_SUN, L_SUN, omega_sb
            )
        )

    prefactor = (1 / (4 * math.pi * omega_sb)) ** (1.0 / 4)

    if show_stellar_types:
        fig, _ = plt.subplots(ncols=1, nrows=1, figsize=(20, 20))
        # fig, colors = add_stellar_types_bar(df, fig, ax_index=-1, only_colorbar=True)
    else:
        fig, _ = plt.subplots(ncols=1, nrows=1, figsize=(20, 20))

    df = df.assign(
        teff_1=prefactor
        * ((df["luminosity_1"] * L_SUN) / ((df["radius_1"] * R_SUN) ** 2)) ** (1.0 / 4)
    )
    df = df.assign(
        teff_2=prefactor
        * ((df["luminosity_2"] * L_SUN) / ((df["radius_2"] * R_SUN) ** 2)) ** (1.0 / 4)
    )

    # # Add colors to dataframe
    # df = df.assign(colors_1=df.apply(color_by_index, axis=1, args=('stellar_type_1', colors)))
    # df = df.assign(colors_2=df.apply(color_by_index, axis=1, args=('stellar_type_2', colors)))

    # Star 1:
    fig.axes[0].scatter(
        df["teff_1"],
        df["luminosity_1"],
        label="Star 1 (M={})".format(df["pms_mass_1"].values.tolist()[0]),
        # color=df['colors_1']
    )

    # Star 2:
    fig.axes[0].scatter(
        df["teff_2"],
        df["luminosity_2"],
        label="Star 2 (M={})".format(df["pms_mass_2"].values.tolist()[0]),
        # color=df['colors_2']
    )

    margin_fraction_x = 0.1
    margin_fraction_y = 0.9

    # Fix axes
    min_y, max_y = (
        df[["luminosity_1", "luminosity_2"]].min().min(),
        df[["luminosity_1", "luminosity_2"]].max().max(),
    )
    min_x, max_x = (
        df[["teff_1", "teff_2"]].min().min(),
        df[["teff_1", "teff_2"]].max().max(),
    )
    fig.axes[0].set_xlim(
        min_x * (1 - margin_fraction_x), max_x * (1 + margin_fraction_x)
    )
    fig.axes[0].set_ylim(
        min_y * (1 - margin_fraction_y), max_y * (1 + margin_fraction_y)
    )
    fig.axes[0].set_yscale("log")
    fig.axes[0].set_xscale("log")
    fig.axes[0].invert_xaxis()

    # Other stuff
    fig.axes[0].set_title("HR diagram")
    fig.axes[0].legend(loc="best")
    fig.axes[0].set_ylabel(r"Luminosity [$L_{star}$/$L_{\odot}$]")
    fig.axes[0].set_xlabel(r"$T_{eff}$ (K)")

    # Show or return
    if show_plot:
        plt.show()
    return fig


def plot_orbit(df, show_stellar_types: bool = False, show_plot: bool = True):
    """
    Function to plot the orbital elements of the system

    Plots the following quantities:
        - Orbital period
        - Separation
        - eccentricity

    TODO: fix stellar_types plot

    Args:
        df: pandas dataframe with the required columns
        show_stellar_types: whether to color code the tracks and show the stellar types
        show_plot: whether to actually show the plot. If false: returns the figure object

    Returns
        returns a figure object if show_plot is false
    """

    if show_stellar_types:
        fig, _ = plt.subplots(ncols=1, nrows=4, figsize=(20, 10))
        fig.subplots_adjust(hspace=0)
    else:
        fig, _ = plt.subplots(ncols=1, nrows=3, figsize=(20, 10), sharex=True)
        fig.subplots_adjust(hspace=0)

    #
    fig.axes[0].plot(df["time"], df["orbital_period"], label="Orbital period")

    fig.axes[1].plot(df["time"], df["separation"], label="Separation orbit")

    fig.axes[2].plot(df["time"], df["eccentricity"], label="Eccentricity orbit")

    # Make up
    fig.axes[0].set_title("Orbital elements evolution")

    fig.axes[0].legend(loc="best")
    fig.axes[1].legend(loc="best")
    fig.axes[2].legend(loc="best")

    # fig.axes[0].set_ylim(0, 1.1*max_total_mass)
    fig.axes[0].set_ylabel(r"Orbital period")
    fig.axes[1].set_ylabel(r"Separation")
    fig.axes[2].set_ylabel(r"Eccentricity")
    fig.axes[0].set_yscale("log")
    fig.axes[1].set_yscale("log")

    fig.axes[2].set_xlabel(r"Time (Myr)")

    # Show or return
    if show_plot:
        plt.show()
    return fig


def plot_masses(df, show_stellar_types: bool = False, show_plot: bool = True):
    """
    Function to plot the masses of the system.

    Function requires the following keys:
        - time
        - pms_mass_1
        - pms_mass_2
        - mass_1
        - mass_2

    Plots the following quantities:
        - Total mass
        - Mass star 1
        - Mass star 2
        - Pms mass 1
        - pms mass 2
        - pms total mass
        - (maybe?) core and env masses

    TODO: fix stellar_types plot

    Args:
        df: pandas dataframe with the required columns
        show_stellar_types: whether to color code the tracks and show the stellar types
        show_plot: whether to actually show the plot. If false: returns the figure object

    Returns
        returns a figure object if show_plot is false
    """

    if show_stellar_types:
        fig, _ = plt.subplots(ncols=1, nrows=2, figsize=(20, 10))
        fig.subplots_adjust(hspace=0)
    else:
        fig, _ = plt.subplots(ncols=1, nrows=1, figsize=(20, 10))

    max_total_mass = (
        df["pms_mass_1"].values.tolist()[0] + df["pms_mass_2"].values.tolist()[0]
    )

    df["total_mass_temp"] = df["mass_1"] + df["mass_2"]
    df["pms_total_mass_temp"] = max_total_mass

    # total mass
    fig.axes[0].plot(df["time"], df["total_mass_temp"], label="Total mass")
    fig.axes[0].axhline(
        df["pms_total_mass_temp"].values.tolist()[0],
        label="Initial total mass",
        linestyle="--",
        alpha=0.5,
    )

    # Mass 1
    fig.axes[0].plot(df["time"], df["mass_1"], label="star 1", color="red")
    fig.axes[0].axhline(
        df["pms_mass_1"].values.tolist()[0],
        color="red",
        linestyle="--",
        linewidth=2,
        label="Initial mass 1",
        alpha=0.5,
    )
    fig.axes[0].plot(
        df["time"],
        df["core_mass_1"],
        color="red",
        linestyle="-.",
        linewidth=2,
        label="Core mass 1",
        alpha=0.5,
    )

    # mass 2
    fig.axes[0].plot(df["time"], df["mass_2"], color="orange", label="star 2")
    fig.axes[0].axhline(
        df["pms_mass_2"].values.tolist()[0],
        color="orange",
        linestyle="--",
        linewidth=2,
        label="Initial mass 2",
        alpha=0.5,
    )
    fig.axes[0].plot(
        df["time"],
        df["core_mass_2"],
        color="orange",
        linestyle="-.",
        linewidth=2,
        label="Core mass 2",
        alpha=0.5,
    )

    # Make up
    fig.axes[0].set_title("Stellar mass evolution")
    fig.axes[0].legend(loc="best")
    fig.axes[0].set_ylim(0, 1.1 * max_total_mass)
    fig.axes[0].set_ylabel(r"Mass [$M_{\odot}$]")
    fig.axes[0].set_xlabel(r"Time (Myr)")

    # Show or return
    if show_plot:
        plt.show()
    return fig


# Define the parse functions for the plotting routines
def dummy():
    """
    Placeholder function
    """

    return None


def parse_function_hr_diagram(output: str):
    """
    Parsing function for the HR plotting routine

    Args:
        output: raw binary_c output string

    Returns:
        pandas dataframe containing the columns for the HR diagram plotting routine
    """

    # extract info from the single evolution

    values_list = []

    parameters = [
        "time",
        "stellar_type_1",
        "stellar_type_2",
        "luminosity_1",
        "luminosity_2",
        "radius_1",
        "radius_2",
        "pms_mass_1",
        "pms_mass_2",
    ]

    # Go over the output.
    for line in output_lines(output):
        headerline = line.split()[0]

        # Check the header and act accordingly
        if headerline == "HR_PLOTTING":
            values = line.split()[1:]
            values_list.append(values)

    df = pd.DataFrame(values_list)
    df.columns = parameters

    df = df.astype(np.float64)
    df["stellar_type_1"] = df["stellar_type_1"].astype(np.int64)
    df["stellar_type_2"] = df["stellar_type_2"].astype(np.int64)

    return df


def parse_function_orbit(output: str):
    """
    Parsing function for the orbit plotting routine

    Args:
        output: raw binary_c output string

    Returns:
        pandas dataframe containing the columns for the orbit plotting routine
    """

    values_list = []

    parameters = [
        "time",
        "orbital_period",
        "separation",
        "eccentricity",
    ]

    # Go over the output.
    for line in output_lines(output):
        headerline = line.split()[0]

        # Check the header and act accordingly
        if headerline == "ORBIT_PLOTTING":
            values = line.split()[1:]
            values_list.append(values)

    df = pd.DataFrame(values_list)
    df.columns = parameters

    df = df.astype(np.float64)

    return df


def parse_function_masses(output: str):
    """
    Parsing function for the orbit plotting routine

    Args:
        output: raw binary_c output string

    Returns:
        pandas dataframe containing the columns for the masses plotting routine
    """

    values_list = []

    parameters = [
        "time",
        "pms_mass_1",
        "pms_mass_2",
        "mass_1",
        "mass_2",
        "core_mass_1",
        "core_mass_2",
    ]

    # Go over the output.
    for line in output_lines(output):
        headerline = line.split()[0]

        # Check the header and act accordingly
        if headerline == "MASS_PLOTTING":
            values = line.split()[1:]
            values_list.append(values)

    df = pd.DataFrame(values_list)
    df.columns = parameters

    df = df.astype(np.float64)

    return df


def plot_system(plot_type, **kwargs):
    """
    Function to plot the different quantities of a system.

    This goes (in general) via the following steps:
        - a preset custom logging for a specific plotting routine is loaded, depending on the choice of plot_type
        - This is used for the run_system call
        - The output of this run_system is loaded into a dataframe by
            parsing it with a corresponding parsing function
        - The dataframe is passed to the plotting routine
        - plot is shown or returned.

    There are several pre-set plots to choose from:
        - mass_evolution
        - orbit_evolution
        - hr_diagram

    All keywords are considered kwargs, except for plot_type

    Args:
        plot_type: string input should be one of ['mass_evolution', 'orbit_evolution', 'hr_diagram'].
            Input will be matched against this, and then go through a dictionary to pick the correct plotting function.
        show_plot: boolean whether to show the plot. If False it returns the figure object
            (makes so that you can customize it)
        show_stellar_types: whether to plot the stellar type evolution on a second pane.
            This is not included in all the plotting routines.
        Other input: other kwargs that are passed to run_system
            (inspect the docstring of run_system for more info)

    Returns:
        returns a object figure if show_plot = false
    """

    # set defaults and options
    show_plot = False
    show_stellar_types = False

    plot_types_dict = {
        "mass_evolution": {
            "plot_function": plot_masses,
            "custom_logging_string": CUSTOM_LOGGING_STRING_MASSES,
            "parse_function": parse_function_masses,
        },
        "orbit_evolution": {
            "plot_function": plot_orbit,
            "custom_logging_string": CUSTOM_LOGGING_STRING_ORBIT,
            "parse_function": parse_function_orbit,
        },
        "hr_diagram": {
            "plot_function": plot_HR_diagram,
            "custom_logging_string": CUSTOM_LOGGING_STRING_HR_DIAGRAM,
            "parse_function": parse_function_hr_diagram,
        },
    }
    plot_system_specific_keywords = ["plot_type", "show_plot", "show_stellar_types"]

    # First check on the plot_type input
    if not plot_type in plot_types_dict:
        print(
            "Warning, the provided plot type is not known. \
            Please choose one from the following:\n\t{}".format(
                plot_types_dict.keys()
            )
        )
        raise ValueError

    # First: check all the arguments. Chosen to not check all the keywords for run_system
    #   and binary_c specifically, but just to pick out the ones needed for this routine.
    #   run_system will handle the rest
    run_system_arg_dict = {}

    for key, value in kwargs.items():
        if key == "show_plot":
            show_plot = value
        elif key == "show_stellar_types":
            show_stellar_types = value

        # The rest will be passed to run_system
        else:
            run_system_arg_dict[key] = value

    # TODO: When a list of plot_types is passed, make it so that the strings are chained,
    #   and that the output of the binary_c call is handled by multiple parsers
    custom_logging_code = binary_c_log_code(
        plot_types_dict[plot_type]["custom_logging_string"]
    )
    run_system_arg_dict["custom_logging_code"] = custom_logging_code

    run_system_arg_dict["parse_function"] = plot_types_dict[plot_type]["parse_function"]

    # Run and get the output of the parse stellar_type_dict_shortfunction
    binary_c_output_df = run_system(**run_system_arg_dict)

    fig = plot_types_dict[plot_type]["plot_function"](
        binary_c_output_df, show_plot=show_plot, show_stellar_types=show_stellar_types
    )

    return fig
