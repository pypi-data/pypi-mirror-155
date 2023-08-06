"""
Collection of useful functions.

Part of this is copied/inspired by Rob's binary_stars module

Functions:
    - calc_period_from_sep(m1, m2, sep) calculate the period given the separation.
    - calc_sep_from_period(m1, m2, per) does the inverse.
    - rzams(m, z) gives you the ZAMS radius of a star
    - ZAMS_collision(m1, m2, e, sep, z) returns 1 if stars collide on the ZAMS
    - roche_lobe(q): returns roche lobe radius in units of separation
    - ragb(m): radius at first thermal pulse
    - minimum_period_for_RLOF(M1, M2, metallicity, store_memaddr=-1): function to calculate the minimum period that leads to RLOF on ZAMS
    - minimum_separation_for_RLOF(M1, M2, metallicity, store_memaddr=-1): function to calculate the minimum period that leads to RLOF on ZAMS
    - maximum_mass_ratio_for_RLOF(M1, orbital_period, store_memaddr=None): Function to calculate the maximum mass ratio that leads to RLOF on ZAMS

Tasks:
    - TODO: check whether these functions are correct
"""

import math
import re
from typing import Union

from binarycpython import _binary_c_bindings
from binarycpython.utils.functions import create_arg_string

AURSUN = 2.150445198804013386961742071435e02
YEARDY = 3.651995478818308811241877265275e02


def minimum_period_for_RLOF(M1, M2, metallicity, store_memaddr=-1):
    """
    Wrapper function for _binary_c_bindings.return_minimum_orbit_for_RLOF

    Handles the output and returns the minimum orbital period at which RLOF just does not occur at ZAMS

    Args:
        M1: Primary mass in solar mass
        M2: Secondary mass in solar mass
        metallicity: metallicity
        store_memaddr (optional): store memory address
    Returns:
        minimum orbital_period that just does not cause a RLOF at ZAMS

    """

    bse_dict = {
        "M_1": M1,
        "M_2": M2,
        "metallicity": metallicity,
        "minimum_orbital_period_for_instant_RLOF": 1,
        "minimum_separation_for_instant_RLOF": 1,
    }

    argstring = "binary_c " + create_arg_string(bse_dict)

    output = _binary_c_bindings.return_minimum_orbit_for_RLOF(argstring, store_memaddr)

    minimum_period = float(re.search("MINIMUM PERIOD (.*)", output).group(1))

    return minimum_period


# print(minimum_period_for_RLOF(10, 5, 0.02))
# print(minimum_period_for_RLOF(10, 2, 0.02))


def minimum_separation_for_RLOF(M1, M2, metallicity, store_memaddr=-1):
    """
    Wrapper function for _binary_c_bindings.return_minimum_orbit_for_RLOF

    Handles the output and returns the minimum separation at which RLOF just does not occur at ZAMS

    Args:
        M1: Primary mass in solar mass
        M2: Secondary mass in solar mass
        metallicity: metallicity
        store_memaddr (optional): store memory adress
    Returns:
        minimum separation that just does not cause a RLOF at ZAMS

    """

    bse_dict = {
        "M_1": M1,
        "M_2": M2,
        "metallicity": metallicity,
        "minimum_orbital_period_for_instant_RLOF": 1,
        "minimum_separation_for_instant_RLOF": 1,
    }

    argstring = "binary_c " + create_arg_string(bse_dict)

    output = _binary_c_bindings.return_minimum_orbit_for_RLOF(argstring, store_memaddr)

    minimum_separation = float(re.search("MINIMUM SEPARATION (.*)", output).group(1))

    return minimum_separation


# print(minimum_separation_for_RLOF(0.08, 0.08, 0.00002))
# print(minimum_separation_for_RLOF(10, 2, 0.02))


def maximum_mass_ratio_for_RLOF(
    M1, orbital_period, metallicity=0.02, store_memaddr=None
):
    """
    Wrapper function for _binary_c_bindings.return_maximum_mass_ratio_for_RLOF

    Handles the output and returns the maximum mass ratio at which RLOF just does not occur at ZAMS

    Args:
        M1: Primary mass in solar mass
        orbital_period: orbital period in days
        metallicity: metallicity
        store_memaddr (optional): store memory adress
    Returns:
        maximum mass ratio that just does not cause a RLOF at ZAMS
    """

    # Convert to orbital period in years
    orbital_period = orbital_period / 3.651995478818308811241877265275e02

    bse_dict = {
        "M_1": M1,
        "M_2": 0.01,
        "separation": 0,
        "orbital_period": orbital_period,
        "metallicity": metallicity,
        "maximum_mass_ratio_for_instant_RLOF": 1,
    }

    argstring = "binary_c " + create_arg_string(bse_dict)
    output = _binary_c_bindings.return_maximum_mass_ratio_for_RLOF(
        argstring, store_memaddr
    )
    stripped = output.strip()

    if stripped == "NO MAXIMUM MASS RATIO < 1":
        maximum_mass_ratio = 1
    else:
        maximum_mass_ratio = float(stripped.split()[-1])
    return maximum_mass_ratio


# print(maximum_mass_ratio_for_RLOF(4, 0.1, 0.002))
# print(maximum_mass_ratio_for_RLOF(4, 1, 0.002))


def calc_period_from_sep(
    M1: Union[int, float], M2: Union[int, float], sep: Union[int, float]
) -> Union[int, float]:
    """
    calculate period from separation

    Args:
        M1: Primary mass in solar mass
        M2: Secondary mass in solar mass
        sep: Separation in solar radii

    Returns:
        period in days
    """

    return YEARDY * (sep / AURSUN) * math.sqrt(sep / (AURSUN * (M1 + M2)))


def calc_sep_from_period(
    M1: Union[int, float], M2: Union[int, float], period: Union[int, float]
) -> Union[int, float]:
    """
    Calculate separation from period.

    Args:
        M1: Primary mass in solar mass
        M2: Secondary mass in solar mass
        period: Period of binary in days

    Returns:
        Separation in solar radii
    """

    return AURSUN * (period * period * (M1 + M2) / (YEARDY * YEARDY)) ** (1.0 / 3.0)


def roche_lobe(q: Union[int, float]) -> Union[int, float]:
    """
    A function to evaluate R_L/a(q), Eggleton 1983.

    # TODO: check the definition of the mass ratio
    # TODO: check whether the logs are correct

    Args:
        q: mass ratio of the binary (secondary/primary). If you input: q = mass_accretor/mass_donor, you will get the rochelobe radius of the accretor. And vice versa for the donor.

    Returns:
        Roche lobe radius in units of the separation
    """

    p = q ** (1.0 / 3.0)
    return 0.49 * p * p / (0.6 * p * p + math.log(1.0 + p))


def ragb(m: Union[int, float]) -> Union[int, float]:
    """
    Function to calculate radius of a star in units of solar radii at first thermal pulse as a function of mass (Z=0.02 only, but also good for Z=0.0001)

    TODO: ask rob about this function. Do we still need this? Can we make something better? (i.e. upon installation of the code run a grid of systems and get the data from there?)

    Args:
        m: mass of star in units of solar mass
        z: metallicity of star

    Returns:
        radius at first thermal pulse in units of solar radii
    """

    return m * 40.0 + 20.0


def zams_collision(
    m1: Union[int, float],
    m2: Union[int, float],
    sep: Union[int, float],
    e: Union[int, float],
    z: Union[int, float],
) -> Union[int, float]:
    """
    given m1,m2, separation and eccentricity (and metallicity)
    determine if two stars collide on the ZAMS

    Args:
        m1: Primary mass in solar mass
        m2: Secondary mass in solar mass
        sep: separation in solar radii
        e: eccentricity
        z: metallicity

    Returns:
        integer boolean whether the binary stars will collide at pericenter
    """

    # calculate periastron distance
    peri_distance = (1.0 - e) * sep

    # calculate star radii
    r1 = rzams(m1, z)
    r2 = rzams(m2, z)

    if r1 + r2 > peri_distance:
        return 1
    return 0


def rzams(m, z):
    """
    Function to determine the radius of a ZAMS star as a function of m and z:

    Based on the fits of Tout et al., 1996, MNRAS, 281, 257

    Args:
        m: mass of star in solar mass
        z: metallicity

    Returns:
        radius of star at ZAMS, in solar radii
    """

    lzs = math.log10(z / 0.02)

    #
    # A function to evaluate Rzams
    # ( from Tout et al., 1996, MNRAS, 281, 257 ).
    #

    p = {}
    xz = (
        666,
        0.39704170,
        -0.32913574,
        0.34776688,
        0.37470851,
        0.09011915,
        8.52762600,
        -24.41225973,
        56.43597107,
        37.06152575,
        5.45624060,
        0.00025546,
        -0.00123461,
        -0.00023246,
        0.00045519,
        0.00016176,
        5.43288900,
        -8.62157806,
        13.44202049,
        14.51584135,
        3.39793084,
        5.56357900,
        -10.32345224,
        19.44322980,
        18.97361347,
        4.16903097,
        0.78866060,
        -2.90870942,
        6.54713531,
        4.05606657,
        0.53287322,
        0.00586685,
        -0.01704237,
        0.03872348,
        0.02570041,
        0.00383376,
        1.71535900,
        0.62246212,
        -0.92557761,
        -1.16996966,
        -0.30631491,
        6.59778800,
        -0.42450044,
        -12.13339427,
        -10.73509484,
        -2.51487077,
        10.08855000,
        -7.11727086,
        -31.67119479,
        -24.24848322,
        -5.33608972,
        1.01249500,
        0.32699690,
        -0.00923418,
        -0.03876858,
        -0.00412750,
        0.07490166,
        0.02410413,
        0.07233664,
        0.03040467,
        0.00197741,
        0.01077422,
        3.08223400,
        0.94472050,
        -2.15200882,
        -2.49219496,
        -0.63848738,
        17.84778000,
        -7.45345690,
        -48.96066856,
        -40.05386135,
        -9.09331816,
        0.00022582,
        -0.00186899,
        0.00388783,
        0.00142402,
        -0.00007671,
    )

    p["8"] = xz[36] + lzs * (xz[37] + lzs * (xz[38] + lzs * (xz[39] + lzs * xz[40])))
    p["9"] = xz[41] + lzs * (xz[42] + lzs * (xz[43] + lzs * (xz[44] + lzs * xz[45])))
    p["10"] = xz[46] + lzs * (xz[47] + lzs * (xz[48] + lzs * (xz[49] + lzs * xz[50])))
    p["11"] = xz[51] + lzs * (xz[52] + lzs * (xz[53] + lzs * (xz[54] + lzs * xz[55])))
    p["12"] = xz[56] + lzs * (xz[57] + lzs * (xz[58] + lzs * (xz[59] + lzs * xz[60])))
    p["13"] = xz[61]
    p["14"] = xz[62] + lzs * (xz[63] + lzs * (xz[64] + lzs * (xz[65] + lzs * xz[66])))
    p["15"] = xz[67] + lzs * (xz[68] + lzs * (xz[69] + lzs * (xz[70] + lzs * xz[71])))
    p["16"] = xz[72] + lzs * (xz[73] + lzs * (xz[74] + lzs * (xz[75] + lzs * xz[76])))

    m195 = m ** 19.5
    rad = (
        p["8"] * (m ** 2.5)
        + p["9"] * (m ** 6.5)
        + p["10"] * (m ** 11)
        + p["11"] * (m ** 19)
        + p["12"] * m195
    ) / (
        p["13"]
        + p["14"] * (m * m)
        + p["15"] * (m ** 8.5)
        + (m ** 18.5)
        + p["16"] * m195
    )
    return rad
