"""
Module containing the functions to handle the Moe&Distrefano data

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import os
import gc
import copy
import json

import py_rinterpolate

from binarycpython.utils.functions import (
    verbose_print,
)
from binarycpython.utils.dicts import update_dicts, normalize_dict
from binarycpython.utils.population_extensions.distribution_functions import (
    Moecache,
    LOG_LN_CONVERTER,
)
from binarycpython.utils.population_extensions.grid_options_defaults import (
    _MOE2017_VERBOSITY_LEVEL,
)
from binarycpython.utils import moe_di_stefano_2017_data


class Moe_di_Stefano_2017:
    """
    Extension to the population grid object that contains functionality to handle handle the Moe & distefano distributions
    """

    def __init__(self, **kwargs):
        """
        Init function for the Moe_di_Stefano_2017 class
        """

        return

    def set_moe_di_stefano_settings(self, options=None):
        """
        Function to set user input configurations for the Moe & di Stefano methods

        If nothing is passed then we just use the default options
        """

        if not options:
            options = {}

        # Take the option dictionary that was given and override.
        options = update_dicts(self.grid_options["Moe2017_options"], options)
        self.grid_options["Moe2017_options"] = copy.deepcopy(options)

        # Write options to a file
        os.makedirs(
            os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
            exist_ok=True,
        )
        with open(
            os.path.join(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                "moeopts.dat",
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(
                    self.grid_options["Moe2017_options"], indent=4, ensure_ascii=False
                )
            )
            f.close()

    def _load_moe_di_stefano_data(self):
        """
        Function to load the moe & di stefano data
        """

        # Only if the grid is loaded and Moecache contains information
        if not self.grid_options["_loaded_Moe2017_data"]:  # and not Moecache:

            if self.grid_options["_Moe2017_JSON_data"]:
                # Use the existing (perhaps modified) JSON data
                json_data = self.grid_options["_Moe2017_JSON_data"]

            else:
                # Load the JSON data from a file
                json_data = self.get_moe_di_stefano_dataset(
                    self.grid_options["Moe2017_options"],
                    verbosity=self.grid_options["verbosity"],
                )

            # entry of log10M1 is a list containing 1 dict.
            # We can take the dict out of the list
            if isinstance(json_data["log10M1"], list):
                json_data["log10M1"] = json_data["log10M1"][0]

            # save this data in case we want to modify it later
            self.grid_options["_Moe2017_JSON_data"] = json_data

            # Get all the masses
            logmasses = sorted(json_data["log10M1"].keys())
            if not logmasses:
                msg = "The table does not contain masses."
                verbose_print(
                    "\tMoe_di_Stefano_2017: {}".format(msg),
                    self.grid_options["verbosity"],
                    0,
                )
                raise ValueError(msg)

            # Write to file
            os.makedirs(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                exist_ok=True,
            )
            with open(
                os.path.join(
                    os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                    "moe.log",
                ),
                "w",
                encoding="utf-8",
            ) as logfile:
                logfile.write("log₁₀Masses(M☉) {}\n".format(logmasses))

            # Get all the periods and see if they are all consistently present
            logperiods = []
            for logmass in logmasses:
                if not logperiods:
                    logperiods = sorted(json_data["log10M1"][logmass]["logP"].keys())
                    dlog10P = float(logperiods[1]) - float(logperiods[0])

                current_logperiods = sorted(json_data["log10M1"][logmass]["logP"])
                if logperiods != current_logperiods:
                    msg = (
                        "Period values are not consistent throughout the dataset logperiods = "
                        + " ".join(str(x) for x in logperiods)
                        + "\nCurrent periods = "
                        + " ".join(str(x) for x in current_logperiods)
                    )
                    verbose_print(
                        "\tMoe_di_Stefano_2017: {}".format(msg),
                        self.grid_options["verbosity"],
                        0,
                    )
                    raise ValueError(msg)

                ############################################################
                # log10period binwidth : of course this assumes a fixed
                # binwidth, so we check for this too.
                for i in range(len(current_logperiods) - 1):
                    if not dlog10P == (
                        float(current_logperiods[i + 1]) - float(current_logperiods[i])
                    ):
                        msg = "Period spacing is not consistent throughout the dataset"
                        verbose_print(
                            "\tMoe_di_Stefano_2017: {}".format(msg),
                            self.grid_options["verbosity"],
                            0,
                        )
                        raise ValueError(msg)

            # save the logperiods list in the cache:
            # this is used in the renormalization integration
            Moecache["logperiods"] = logperiods

            # Write to file
            os.makedirs(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                exist_ok=True,
            )
            with open(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano", "moe.log"),
                "a",
                encoding="utf-8",
            ) as logfile:
                logfile.write("log₁₀Periods(days) {}\n".format(logperiods))

            # Fill the global dict
            for logmass in logmasses:
                # Create the multiplicity table
                if not Moecache.get("multiplicity_table", None):
                    Moecache["multiplicity_table"] = []

                # multiplicity as a function of primary mass
                Moecache["multiplicity_table"].append(
                    [
                        float(logmass),
                        json_data["log10M1"][logmass]["f_multi"],
                        json_data["log10M1"][logmass]["single star fraction"],
                        json_data["log10M1"][logmass]["binary star fraction"],
                        json_data["log10M1"][logmass]["triple/quad star fraction"],
                    ]
                )

                ############################################################
                # a small log10period which we can shift just outside the
                # table to force integration out there to zero
                epslog10P = 1e-8 * dlog10P

                ############################################################
                # loop over either binary or triple-outer periods
                first = 1

                # Go over the periods
                for logperiod in logperiods:
                    ############################################################
                    # distributions of binary and triple star fractions
                    # as a function of mass, period.
                    #
                    # Note: these should be per unit log10P, hence we
                    # divide by dlog10P

                    if first:
                        first = 0

                        # Create the multiplicity table
                        if not Moecache.get("period_distributions", None):
                            Moecache["period_distributions"] = []

                        ############################################################
                        # lower bound the period distributions to zero probability
                        Moecache["period_distributions"].append(
                            [
                                float(logmass),
                                float(logperiod) - 0.5 * dlog10P - epslog10P,
                                0.0,
                                0.0,
                            ]
                        )
                        Moecache["period_distributions"].append(
                            [
                                float(logmass),
                                float(logperiod) - 0.5 * dlog10P,
                                json_data["log10M1"][logmass]["logP"][logperiod][
                                    "normed_bin_frac_p_dist"
                                ]
                                / dlog10P,
                                json_data["log10M1"][logmass]["logP"][logperiod][
                                    "normed_tripquad_frac_p_dist"
                                ]
                                / dlog10P,
                            ]
                        )

                    Moecache["period_distributions"].append(
                        [
                            float(logmass),
                            float(logperiod),
                            json_data["log10M1"][logmass]["logP"][logperiod][
                                "normed_bin_frac_p_dist"
                            ]
                            / dlog10P,
                            json_data["log10M1"][logmass]["logP"][logperiod][
                                "normed_tripquad_frac_p_dist"
                            ]
                            / dlog10P,
                        ]
                    )

                    ############################################################
                    # distributions as a function of mass, period, q
                    #
                    # First, get a list of the qs given by Moe
                    #
                    qs = sorted(json_data["log10M1"][logmass]["logP"][logperiod]["q"])

                    # Fill the data and 'normalise'
                    qdata = self.fill_data(
                        qs, json_data["log10M1"][logmass]["logP"][logperiod]["q"]
                    )

                    # Create the multiplicity table
                    if not Moecache.get("q_distributions", None):
                        Moecache["q_distributions"] = []

                    for q in qs:
                        Moecache["q_distributions"].append(
                            [float(logmass), float(logperiod), float(q), qdata[q]]
                        )

                    ############################################################
                    # eccentricity distributions as a function of mass, period, ecc
                    eccs = sorted(json_data["log10M1"][logmass]["logP"][logperiod]["e"])

                    # Fill the data and 'normalise'
                    ecc_data = self.fill_data(
                        eccs, json_data["log10M1"][logmass]["logP"][logperiod]["e"]
                    )

                    # Create the multiplicity table
                    if not Moecache.get("ecc_distributions", None):
                        Moecache["ecc_distributions"] = []

                    for ecc in eccs:
                        Moecache["ecc_distributions"].append(
                            [
                                float(logmass),
                                float(logperiod),
                                float(ecc),
                                ecc_data[ecc],
                            ]
                        )

                ############################################################
                # upper bound the period distributions to zero probability
                Moecache["period_distributions"].append(
                    [
                        float(logmass),
                        float(logperiods[-1])
                        + 0.5 * dlog10P,  # TODO: why this shift? to center it?
                        json_data["log10M1"][logmass]["logP"][logperiods[-1]][
                            "normed_bin_frac_p_dist"
                        ]
                        / dlog10P,
                        json_data["log10M1"][logmass]["logP"][logperiods[-1]][
                            "normed_tripquad_frac_p_dist"
                        ]
                        / dlog10P,
                    ]
                )
                Moecache["period_distributions"].append(
                    [
                        float(logmass),
                        float(logperiods[-1]) + 0.5 * dlog10P + epslog10P,
                        0.0,
                        0.0,
                    ]
                )

            verbose_print(
                "\tMoe_di_Stefano_2017: Length period_distributions table: {}".format(
                    len(Moecache["period_distributions"])
                ),
                self.grid_options["verbosity"],
                _MOE2017_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length multiplicity table: {}".format(
                    len(Moecache["multiplicity_table"])
                ),
                self.grid_options["verbosity"],
                _MOE2017_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length q table: {}".format(
                    len(Moecache["q_distributions"])
                ),
                self.grid_options["verbosity"],
                _MOE2017_VERBOSITY_LEVEL,
            )
            verbose_print(
                "\tMoe_di_Stefano_2017: Length ecc table: {}".format(
                    len(Moecache["ecc_distributions"])
                ),
                self.grid_options["verbosity"],
                _MOE2017_VERBOSITY_LEVEL,
            )

            # Write to log file
            os.makedirs(
                os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                exist_ok=True,
            )
            with open(
                os.path.join(
                    os.path.join(self.grid_options["tmp_dir"], "moe_distefano"),
                    "moecache.json",
                ),
                "w",
                encoding="utf-8",
            ) as cache_filehandle:
                cache_filehandle.write(
                    json.dumps(Moecache, indent=4, ensure_ascii=False)
                )

            # Signal that the data has been loaded
            self.grid_options["_loaded_Moe2017_data"] = True

    def _set_moe_di_stefano_distributions(self):
        """
        Function to set the Moe & di Stefano distribution
        """

        ############################################################
        # first, the multiplicity, this is 1,2,3,4, ...
        # for singles, binaries, triples, quadruples, ...

        max_multiplicity = self.get_max_multiplicity(
            self.grid_options["Moe2017_options"]["multiplicity_modulator"]
        )
        verbose_print(
            "\tMoe_di_Stefano_2017: Max multiplicity = {}".format(max_multiplicity),
            self.grid_options["verbosity"],
            _MOE2017_VERBOSITY_LEVEL,
        )
        ######
        # Setting up the grid variables

        # Multiplicity
        self.add_grid_variable(
            name="multiplicity",
            parameter_name="multiplicity",
            longname="multiplicity",
            valuerange=[1, max_multiplicity],
            samplerfunc="self.const_int(1, {n}, {n})".format(n=max_multiplicity),
            precode='self.grid_options["multiplicity"] = multiplicity; self.bse_options["multiplicity"] = multiplicity; options={}'.format(
                self.grid_options["Moe2017_options"]
            ),
            condition="({}[int(multiplicity)-1] > 0)".format(
                str(self.grid_options["Moe2017_options"]["multiplicity_modulator"])
            ),
            gridtype="discrete",
            probdist=1,
        )

        ############################################################
        # always require M1, for all systems
        #
        # log-spaced m1 with given resolution
        self.add_grid_variable(
            name="lnM_1",
            parameter_name="M_1",
            longname="Primary mass",
            samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"]["M"][0]
            or "self.const_linear(np.log({}), np.log({}), {})".format(
                self.grid_options["Moe2017_options"]["ranges"]["M"][0],
                self.grid_options["Moe2017_options"]["ranges"]["M"][1],
                self.grid_options["Moe2017_options"]["resolutions"]["M"][0],
            ),
            valuerange=[
                "np.log({})".format(
                    self.grid_options["Moe2017_options"]["ranges"]["M"][0]
                ),
                "np.log({})".format(
                    self.grid_options["Moe2017_options"]["ranges"]["M"][1]
                ),
            ],
            gridtype="centred",
            dphasevol="dlnM_1",
            precode='M_1 = np.exp(lnM_1); options["M_1"]=M_1',
            probdist="self.Moe_di_Stefano_2017_pdf({{{}, {}, {}}}, verbosity=self.grid_options['verbosity'])['total_probdens'] if multiplicity == 1 else 1".format(
                str(dict(self.grid_options["Moe2017_options"]))[1:-1],
                "'multiplicity': multiplicity",
                "'M_1': M_1",
            ),
        )

        # Go to higher multiplicities
        if max_multiplicity >= 2:
            # binaries: period
            self.add_grid_variable(
                name="log10per",
                parameter_name="orbital_period",
                longname="log10(Orbital_Period)",
                probdist=1.0,
                condition='(self.grid_options["multiplicity"] >= 2)',
                branchpoint=1
                if max_multiplicity > 1
                else 0,  # Signal here to put a branchpoint if we have a max multiplicity higher than 1.
                gridtype="centred",
                dphasevol="({} * dlog10per)".format(LOG_LN_CONVERTER),
                valuerange=[
                    self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                    self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                ],
                samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"][
                    "logP"
                ][0]
                or "self.const_linear({}, {}, {})".format(
                    self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                    self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                    self.grid_options["Moe2017_options"]["resolutions"]["logP"][0],
                ),
                precode="""orbital_period = 10.0**log10per
qmin={}/M_1
qmax=maximum_mass_ratio_for_RLOF(M_1, orbital_period)
""".format(
                    self.grid_options["Moe2017_options"]["Mmin"]
                ),
            )  # TODO: change the maximum_mass_ratio_for_RLOF

            # binaries: mass ratio
            self.add_grid_variable(
                name="q",
                parameter_name="M_2",
                longname="Mass ratio",
                valuerange=[
                    self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                    if self.grid_options["Moe2017_options"]
                    .get("ranges", {})
                    .get("q", None)
                    else "options['Mmin']/M_1",
                    self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                    if self.grid_options["Moe2017_options"]
                    .get("ranges", {})
                    .get("q", None)
                    else "qmax",
                ],
                probdist=1,
                gridtype="centred",
                dphasevol="dq",
                precode="""
M_2 = q * M_1
sep = calc_sep_from_period(M_1, M_2, orbital_period)
    """,
                samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"]["M"][1]
                or "self.const_linear({}, {}, {})".format(
                    self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                    if self.grid_options["Moe2017_options"]
                    .get("ranges", {})
                    .get("q", [None, None])[0]
                    else "{}/M_1".format(self.grid_options["Moe2017_options"]["Mmin"]),
                    self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                    if self.grid_options["Moe2017_options"]
                    .get("ranges", {})
                    .get("q", [None, None])[1]
                    else "qmax",
                    self.grid_options["Moe2017_options"]["resolutions"]["M"][1],
                ),
            )

            # (optional) binaries: eccentricity
            if self.grid_options["Moe2017_options"]["resolutions"]["ecc"][0] > 0:
                self.add_grid_variable(
                    name="ecc",
                    parameter_name="eccentricity",
                    longname="Eccentricity",
                    probdist=1,
                    gridtype="centred",
                    dphasevol="decc",
                    precode="eccentricity=ecc",
                    valuerange=[
                        self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                            0
                        ],  # Just fail if not defined.
                        self.grid_options["Moe2017_options"]["ranges"]["ecc"][1],
                    ],
                    samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"][
                        "ecc"
                    ][0]
                    or "self.const_linear({}, {}, {})".format(
                        self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                            0
                        ],  # Just fail if not defined.
                        self.grid_options["Moe2017_options"]["ranges"]["ecc"][1],
                        self.grid_options["Moe2017_options"]["resolutions"]["ecc"][0],
                    ),
                )

            # Now for triples and quadruples
            if max_multiplicity >= 3:
                # Triple: period
                self.add_grid_variable(
                    name="log10per2",
                    parameter_name="orbital_period_triple",
                    longname="log10(Orbital_Period2)",
                    probdist=1.0,
                    condition='(self.grid_options["multiplicity"] >= 3)',
                    branchpoint=2
                    if max_multiplicity > 2
                    else 0,  # Signal here to put a branchpoint if we have a max multiplicity higher than 1.
                    gridtype="centred",
                    dphasevol="({} * dlog10per2)".format(LOG_LN_CONVERTER),
                    valuerange=[
                        self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                        self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                    ],
                    samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"][
                        "logP"
                    ][1]
                    or "self.const_linear({}, {}, {})".format(
                        self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                        self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                        self.grid_options["Moe2017_options"]["resolutions"]["logP"][1],
                    ),
                    precode="""orbital_period_triple = 10.0**log10per2
q2min={}/(M_1+M_2)
q2max=maximum_mass_ratio_for_RLOF(M_1+M_2, orbital_period_triple)
    """.format(
                        self.grid_options["Moe2017_options"]["Mmin"]
                    ),
                )

                # Triples: mass ratio
                # Note, the mass ratio is M_outer/M_inner
                self.add_grid_variable(
                    name="q2",
                    parameter_name="M_3",
                    longname="Mass ratio outer/inner",
                    valuerange=[
                        self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                        if self.grid_options["Moe2017_options"]
                        .get("ranges", {})
                        .get("q", None)
                        else "options['Mmin']/(M_1+M_2)",
                        self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                        if self.grid_options["Moe2017_options"]
                        .get("ranges", {})
                        .get("q", None)
                        else "q2max",
                    ],
                    probdist=1,
                    gridtype="centred",
                    dphasevol="dq2",
                    precode="""
M_3 = q2 * (M_1 + M_2)
sep2 = calc_sep_from_period((M_1+M_2), M_3, orbital_period_triple)
eccentricity2=0
""",
                    samplerfunc=self.grid_options["Moe2017_options"]["samplerfuncs"][
                        "M"
                    ][2]
                    or "self.const_linear({}, {}, {})".format(
                        self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                        if self.grid_options["Moe2017_options"]
                        .get("ranges", {})
                        .get("q", None)
                        else "options['Mmin']/(M_1+M_2)",
                        self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                        if self.grid_options["Moe2017_options"]
                        .get("ranges", {})
                        .get("q", None)
                        else "q2max",
                        self.grid_options["Moe2017_options"]["resolutions"]["M"][2],
                    ),
                )

                # (optional) triples: eccentricity
                if self.grid_options["Moe2017_options"]["resolutions"]["ecc"][1] > 0:
                    self.add_grid_variable(
                        name="ecc2",
                        parameter_name="eccentricity2",
                        longname="Eccentricity of the triple",
                        probdist=1,
                        gridtype="centred",
                        dphasevol="decc2",
                        precode="eccentricity2=ecc2",
                        valuerange=[
                            self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                0
                            ],  # Just fail if not defined.
                            self.grid_options["Moe2017_options"]["ranges"]["ecc"][1],
                        ],
                        samplerfunc=self.grid_options["Moe2017_options"][
                            "samplerfuncs"
                        ]["ecc"][1]
                        or "self.const_linear({}, {}, {})".format(
                            self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                0
                            ],  # Just fail if not defined.
                            self.grid_options["Moe2017_options"]["ranges"]["ecc"][1],
                            self.grid_options["Moe2017_options"]["resolutions"]["ecc"][
                                1
                            ],
                        ),
                    )

                if max_multiplicity == 4:
                    # Quadruple: period
                    self.add_grid_variable(
                        name="log10per3",
                        parameter_name="orbital_period_quadruple",
                        longname="log10(Orbital_Period3)",
                        probdist=1.0,
                        condition='(self.grid_options["multiplicity"] >= 4)',
                        branchpoint=3
                        if max_multiplicity > 3
                        else 0,  # Signal here to put a branchpoint if we have a max multiplicity higher than 1.
                        gridtype="centred",
                        dphasevol="({} * dlog10per3)".format(LOG_LN_CONVERTER),
                        valuerange=[
                            self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                            self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                        ],
                        samplerfunc=self.grid_options["Moe2017_options"][
                            "samplerfuncs"
                        ]["logP"][2]
                        or "self.const_linear({}, {}, {})".format(
                            self.grid_options["Moe2017_options"]["ranges"]["logP"][0],
                            self.grid_options["Moe2017_options"]["ranges"]["logP"][1],
                            self.grid_options["Moe2017_options"]["resolutions"]["logP"][
                                2
                            ],
                        ),
                        precode="""orbital_period_quadruple = 10.0**log10per3
q3min={}/(M_3)
q3max=maximum_mass_ratio_for_RLOF(M_3, orbital_period_quadruple)
    """.format(
                            self.grid_options["Moe2017_options"]["Mmin"]
                        ),
                    )

                    # Quadruple: mass ratio : M_outer / M_inner
                    self.add_grid_variable(
                        name="q3",
                        parameter_name="M_4",
                        longname="Mass ratio outer low/outer high",
                        valuerange=[
                            self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                            if self.grid_options["Moe2017_options"]
                            .get("ranges", {})
                            .get("q", None)
                            else "options['Mmin']/(M_3)",
                            self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                            if self.grid_options["Moe2017_options"]
                            .get("ranges", {})
                            .get("q", None)
                            else "q3max",
                        ],
                        probdist=1,
                        gridtype="centred",
                        dphasevol="dq3",
                        precode="""
M_4 = q3 * M_3
sep3 = calc_sep_from_period((M_3), M_4, orbital_period_quadruple)
eccentricity3=0
""",
                        samplerfunc=self.grid_options["Moe2017_options"][
                            "samplerfuncs"
                        ]["M"][3]
                        or "self.const_linear({}, {}, {})".format(
                            self.grid_options["Moe2017_options"]["ranges"]["q"][0]
                            if self.grid_options["Moe2017_options"]
                            .get("ranges", {})
                            .get("q", None)
                            else "options['Mmin']/(M_3)",
                            self.grid_options["Moe2017_options"]["ranges"]["q"][1]
                            if self.grid_options["Moe2017_options"]
                            .get("ranges", {})
                            .get("q", None)
                            else "q3max",
                            self.grid_options["Moe2017_options"]["resolutions"]["M"][2],
                        ),
                    )

                    # (optional) triples: eccentricity
                    if (
                        self.grid_options["Moe2017_options"]["resolutions"]["ecc"][2]
                        > 0
                    ):
                        self.add_grid_variable(
                            name="ecc3",
                            parameter_name="eccentricity3",
                            longname="Eccentricity of the triple+quadruple/outer binary",
                            probdist=1,
                            gridtype="centred",
                            dphasevol="decc3",
                            precode="eccentricity3=ecc3",
                            valuerange=[
                                self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                    0
                                ],  # Just fail if not defined.
                                self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                    1
                                ],
                            ],
                            samplerfunc=self.grid_options["Moe2017_options"][
                                "samplerfuncs"
                            ]["ecc"][2]
                            or "self.const_linear({}, {}, {})".format(
                                self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                    0
                                ],  # Just fail if not defined.
                                self.grid_options["Moe2017_options"]["ranges"]["ecc"][
                                    1
                                ],
                                self.grid_options["Moe2017_options"]["resolutions"][
                                    "ecc"
                                ][2],
                            ),
                        )

        # Now we are at the last part.
        # Here we should combine all the information that we calculate and update the options
        # dictionary. This will then be passed to the Moe_di_Stefano_2017_pdf to calculate
        # the real probability. The trick we use is to strip the options_dict as a string
        # and add some keys to it:

        updated_options = "{{{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}}}".format(
            str(dict(self.grid_options["Moe2017_options"]))[1:-1],
            '"multiplicity": multiplicity',
            '"M_1": M_1',
            '"M_2": M_2',
            '"M_3": M_3',
            '"M_4": M_4',
            '"P": orbital_period',
            '"P2": orbital_period_triple',
            '"P3": orbital_period_quadruple',
            '"ecc": eccentricity',
            '"ecc2": eccentricity2',
            '"ecc3": eccentricity3',
        )

        probdist_addition = "self.Moe_di_Stefano_2017_pdf({}, verbosity=self.grid_options['verbosity'])['total_probdens']".format(
            updated_options
        )

        # and finally the probability calculator
        self.grid_options["_grid_variables"][self._last_grid_variable()][
            "probdist"
        ] = probdist_addition

        verbose_print(
            "\tMoe_di_Stefano_2017: Added final call to the pdf function",
            self.grid_options["verbosity"],
            _MOE2017_VERBOSITY_LEVEL,
        )

        # Signal that the MOE2017 grid has been set
        self.grid_options["_set_Moe2017_grid"] = True

    ################################################################################################
    def Moe_di_Stefano_2017(self, options=None):
        """
        Function to handle setting the user input settings,
        set up the data and load that into interpolators and
        then set the distribution functions

        Takes a dictionary as its only argument
        """

        default_options = {
            "apply settings": True,
            "setup grid": True,
            "load data": True,
            "clean cache": False,
            "clean load flag": False,
            "clean all": False,
        }

        if not options:
            options = {}
        options = update_dicts(default_options, options)

        # clean cache?
        if options["clean all"] or options["clean cache"]:
            Moecache.clear()

        if options["clean all"] or options["clean load flag"]:
            self.grid_options["_loaded_Moe2017_data"] = False

        # Set the user input
        if options["apply settings"]:
            self.set_moe_di_stefano_settings(options=options)

        # Load the data
        if options["load data"]:
            self._load_moe_di_stefano_data()

        # construct the grid here
        if options["setup grid"]:
            self._set_moe_di_stefano_distributions()

    def _clean_interpolators(self):
        """
        Function to clean up the interpolators after a run

        We look in the Moecache global variable for items that are interpolators.
        Should be called by the general cleanup function AND the thread cleanup function
        """

        interpolator_keys = []
        for key, value in Moecache.items():
            if isinstance(value, py_rinterpolate.Rinterpolate):
                interpolator_keys.append(key)

        for key in interpolator_keys:
            Moecache[key].destroy()
            del Moecache[key]
        gc.collect()

    def _calculate_multiplicity_fraction(self, system_dict):
        """
        Function to calculate multiplicity fraction

        Makes use of the self.bse_options['multiplicity'] value. If its not set, it will raise an error

        grid_options['multiplicity_fraction_function'] will be checked for the choice

        TODO: add option to put a manual binary fraction in here (solve via negative numbers being the functions)
        """

        # Just return 1 if no option has been chosen
        if self.grid_options["multiplicity_fraction_function"] in [0, "None"]:
            verbose_print(
                "_calculate_multiplicity_fraction: Chosen not to use any multiplicity fraction.",
                self.grid_options["verbosity"],
                3,
            )

            return 1

        # Raise an error if the multiplicity is not set
        if not system_dict.get("multiplicity", None):
            msg = "Multiplicity value has not been set. When using a specific multiplicity fraction function please set the multiplicity"
            raise ValueError(msg)

        # Go over the chosen options
        if self.grid_options["multiplicity_fraction_function"] in [1, "Arenou2010"]:
            # Arenou 2010 will be used
            verbose_print(
                "_calculate_multiplicity_fraction: Using Arenou 2010 to calculate multiplicity fractions",
                self.grid_options["verbosity"],
                3,
            )

            binary_fraction = self.Arenou2010_binary_fraction(system_dict["M_1"])
            multiplicity_fraction_dict = {
                1: 1 - binary_fraction,
                2: binary_fraction,
                3: 0,
                4: 0,
            }

        elif self.grid_options["multiplicity_fraction_function"] in [2, "Raghavan2010"]:
            # Raghavan 2010 will be used
            verbose_print(
                "_calculate_multiplicity_fraction: Using Raghavan (2010) to calculate multiplicity fractions",
                self.grid_options["verbosity"],
                3,
            )

            binary_fraction = self.raghavan2010_binary_fraction(system_dict["M_1"])
            multiplicity_fraction_dict = {
                1: 1 - binary_fraction,
                2: binary_fraction,
                3: 0,
                4: 0,
            }

        elif self.grid_options["multiplicity_fraction_function"] in [3, "Moe2017"]:
            # We need to check several things now here:

            # First, are the options for the MOE2017 grid set? On start it is filled with the default settings
            if not self.grid_options["Moe2017_options"]:
                msg = "The MOE2017 options do not seem to be set properly. The value is {}".format(
                    self.grid_options["Moe2017_options"]
                )
                raise ValueError(msg)

            # Second: is the Moecache filled.
            if not Moecache:
                verbose_print(
                    "_calculate_multiplicity_fraction: Moecache is empty. It needs to be filled with the data for the interpolators. Loading the data now",
                    self.grid_options["verbosity"],
                    3,
                )

                # Load the data
                self._load_moe_di_stefano_data()

            # record the prev value
            prev_M1_value_ms = self.grid_options["Moe2017_options"].get("M_1", None)

            # Set value of M1 of the current system
            self.grid_options["Moe2017_options"]["M_1"] = system_dict["M_1"]

            # Calculate the multiplicity fraction
            multiplicity_fraction_list = (
                self.Moe_di_Stefano_2017_multiplicity_fractions(
                    self.grid_options["Moe2017_options"], self.grid_options["verbosity"]
                )
            )

            # Turn into dict
            multiplicity_fraction_dict = {
                el + 1: multiplicity_fraction_list[el]
                for el in range(len(multiplicity_fraction_list))
            }

            # Set the prev value back
            self.grid_options["Moe2017_options"]["M_1"] = prev_M1_value_ms

        # we don't know what to do next
        else:
            msg = "Chosen value for the multiplicity fraction function is not known."
            raise ValueError(msg)

        # To make sure we normalize the dictionary
        multiplicity_fraction_dict = normalize_dict(
            multiplicity_fraction_dict, verbosity=self.grid_options["verbosity"]
        )

        verbose_print(
            "Multiplicity: {} multiplicity_fraction: {}".format(
                system_dict["multiplicity"],
                multiplicity_fraction_dict[system_dict["multiplicity"]],
            ),
            self.grid_options["verbosity"],
            3,
        )

        return multiplicity_fraction_dict[system_dict["multiplicity"]]

    def get_moe_di_stefano_dataset(self, options, verbosity=0):
        """
            Function to get the default Moe and di Stefano dataset or accept a user input.

        Returns a dict containing the (JSON) data.
        """

        json_data = None

        if "JSON" in options:
            # use the JSON data passed in
            json_data = options["JSON"]

        elif "file" in options:
            # use the file passed in, if provided
            if not os.path.isfile(options["file"]):
                verbose_print(
                    "The provided 'file' Moe and de Stefano JSON file does not seem to exist at {}".format(
                        options["file"]
                    ),
                    verbosity,
                    1,
                )

                raise ValueError
            if not options["file"].endswith(".json"):
                verbose_print(
                    "Provided filename is not a json file",
                    verbosity,
                    1,
                )

            else:
                # Read input data and Clean up the data if there are white spaces around the keys
                with open(options["file"], "r", encoding="utf-8") as data_filehandle:
                    datafile_data = data_filehandle.read()
                    datafile_data = datafile_data.replace('" ', '"')
                    datafile_data = datafile_data.replace(' "', '"')
                    datafile_data = datafile_data.replace(' "', '"')
                    json_data = json.loads(datafile_data)

        if not json_data:
            # no JSON data or filename given, use the default 2017 dataset
            verbose_print(
                "Using the default Moe and de Stefano 2017 datafile",
                verbosity,
                1,
            )
            json_data = copy.deepcopy(moe_di_stefano_2017_data.moe_di_stefano_2017_data)

        return json_data

    def get_Moe_di_Stefano_2017_default_options(self):
        """
        Function that returns the default options for the Moe & diStefano grid options
        """

        return {
            # place holder for the JSON data to be used if a file
            # isn't specified
            "JSON": None,
            # resolution data
            "resolutions": {
                "M": [
                    20,  # M1
                    20,  # M2 (i.e. q)
                    0,  # M3 currently unused
                    0,  # M4 currently unused
                ],
                "logP": [
                    20,  # P2 (binary period)
                    0,  # P3 (triple period) currently unused
                    0,  # P4 (quadruple period) currently unused
                ],
                "ecc": [
                    10,  # e (binary eccentricity)
                    0,  # e2 (triple eccentricity) currently unused
                    0,  # e3 (quadruple eccentricity) currently unused
                ],
            },
            "samplerfuncs": {
                "M": [None, None, None, None],
                "logP": [None, None, None],
                "ecc": [None, None, None],
            },
            "ranges": {
                # stellar masses (Msun)
                "M": [
                    self.minimum_stellar_mass()
                    * 1.05,  # 0.08 is a tad bit above the minimum mass. Don't sample at 0.07, otherwise the first row of q values will have a phasevol of 0. Anything higher is fine.
                    80.0,  # (rather arbitrary) upper mass cutoff
                ],
                "q": [
                    None,  # artificial qmin : set to None to use default
                    None,  # artificial qmax : set to None to use default
                ],
                "logP": [0.0, 8.0],  # 0 = log10(1 day)  # 8 = log10(10^8 days)
                "ecc": [0.0, 0.99],
            },
            # minimum stellar mass
            "Mmin": self.minimum_stellar_mass(),  # We take the value that binary_c has set as the default
            # multiplicity model (as a function of log10M1)
            #
            # You can use 'Poisson' which uses the system multiplicity
            # given by Moe and maps this to single/binary/triple/quad
            # fractions.
            #
            # Alternatively, 'data' takes the fractions directly
            # from the data, but then triples and quadruples are
            # combined (and there are NO quadruples).
            "multiplicity_model": "Poisson",
            # multiplicity modulator:
            # [single, binary, triple, quadruple]
            #
            # e.g. [1,0,0,0] for single stars only
            #      [0,1,0,0] for binary stars only
            #
            # defaults to [1,1,0,0] i.e. all types
            #
            "multiplicity_modulator": [
                1,  # single
                1,  # binary
                0,  # triple
                0,  # quadruple
            ],
            # given a mix of multiplicities, you can either (noting that
            # here (S,B,T,Q) = appropriate modulator * model(S,B,T,Q) )
            #
            # 'norm'  : normalise so the whole population is 1.0
            #           after implementing the appropriate fractions
            #           S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
            #
            # 'raw'   : stick to what is predicted, i.e.
            #           S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
            #           without normalisation
            #           (in which case the total probability < 1.0 unless
            #            all you use single, binary, triple and quadruple)
            #
            # 'merge' : e.g. if you only have single and binary,
            #           add the triples and quadruples to the binaries, so
            #           binaries represent all multiple systems
            #           ...
            #           *** this is canonical binary population synthesis ***
            #
            #           Note: if multiplicity_modulator == [1,1,1,1] this
            #                 option does nothing (equivalent to 'raw').
            #
            #
            # note: if you only set one multiplicity_modulator
            # to 1, and all the others to 0, then normalising
            # will mean that you effectively have the same number
            # of stars as single, binary, triple or quad (whichever
            # is non-zero) i.e. the multiplicity fraction is ignored.
            # This is probably not useful except for
            # testing purposes or comparing to old grids.
            "normalize_multiplicities": "merge",
            # q extrapolation (below 0.15 and above 0.9) method. We can choose from ['flat', 'linear', 'plaw2', 'nolowq']
            "q_low_extrapolation_method": "linear",
            "q_high_extrapolation_method": "linear",
        }

    def get_Moe_di_Stefano_2017_default_options_description(self):
        """
        Function to return the descriptions for all the Moe & diStefano grid options
        """

        return {
            "resolutions": "",
            "ranges": "",
            "Mmin": "Minimum stellar mass",
            "multiplicity_model": """
        multiplicity model (as a function of log10M1)

        You can use 'Poisson' which uses the system multiplicity
        given by Moe and maps this to single/binary/triple/quad
        fractions.

        Alternatively, 'data' takes the fractions directly
        from the data, but then triples and quadruples are
        combined (and there are NO quadruples).
        """,
            "multiplicity_modulator": """
        [single, binary, triple, quadruple]

        e.g. [1,0,0,0] for single stars only
             [0,1,0,0] for binary stars only

        defaults to [1,1,0,0] i.e. singles and binaries
        """,
            "normalize_multiplicities": """
        'norm': normalise so the whole population is 1.0
                after implementing the appropriate fractions
                S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
                given a mix of multiplicities, you can either (noting that
                here (S,B,T,Q) = appropriate modulator * model(S,B,T,Q) )
                note: if you only set one multiplicity_modulator
                to 1, and all the others to 0, then normalising
                will mean that you effectively have the same number
                of stars as single, binary, triple or quad (whichever
                is non-zero) i.e. the multiplicity fraction is ignored.
                This is probably not useful except for
                testing purposes or comparing to old grids.

        'raw'   : stick to what is predicted, i.e.
                  S/(S+B+T+Q), B/(S+B+T+Q), T/(S+B+T+Q), Q/(S+B+T+Q)
                  without normalisation
                  (in which case the total probability < 1.0 unless
                  all you use single, binary, triple and quadruple)

        'merge' : e.g. if you only have single and binary,
                  add the triples and quadruples to the binaries, so
                  binaries represent all multiple systems
                  ...
                  *** this is canonical binary population synthesis ***

                  It only takes the maximum multiplicity into account,
                  i.e. it doesn't multiply the resulting array by the multiplicity modulator again.
                  This prevents the resulting array to always be 1 if only 1 multiplicity modulator element is nonzero

                  Note: if multiplicity_modulator == [1,1,1,1]. this option does nothing (equivalent to 'raw').
        """,
            "q_low_extrapolation_method": """
        q extrapolation (below 0.15) method
            none
            flat
            linear2
            plaw2
            nolowq
        """,
            "q_high_extrapolation_method": "Same as q_low_extrapolation_method",
        }
