"""
File containing the class object containing the functions to handle binary_c version info.

This class will be used to extend the population object

NOTE: could these functions not just be normal functions rather than class methods? I see hardly any use of the self
"""

# pylint: disable=E0203

import copy
import os

from typing import Union

from binarycpython import _binary_c_bindings
from binarycpython.utils.functions import isfloat


class version_info:
    """
    Class object containing the functions to handle binary_c version info.

    This class will be used to extend the population object
    """

    def __init__(self, **kwargs):
        """
        Init function for the version_info class
        """

        return

    ########################################################
    # version_info functions
    ########################################################
    def return_binary_c_version_info(self, parsed: bool = True) -> Union[str, dict]:
        """
        Function that returns the version information of binary_c. This function calls the function
        _binary_c_bindings.return_version_info()

        Args:
            parsed: Boolean flag whether to parse the version_info output of binary_c. default = False

        Returns:
            Either the raw string of binary_c or a parsed version of this in the form of a nested
            dictionary
        """

        found_prev = False
        if "BINARY_C_MACRO_HEADER" in os.environ:
            # the env var is already present. lets save that and put that back later
            found_prev = True
            prev_value = os.environ["BINARY_C_MACRO_HEADER"]

        #
        os.environ["BINARY_C_MACRO_HEADER"] = "macroxyz"

        # Get version_info
        raw_version_info = _binary_c_bindings.return_version_info().strip()

        # delete value
        del os.environ["BINARY_C_MACRO_HEADER"]

        # put stuff back if we found a previous one
        if found_prev:
            os.environ["BINARY_C_MACRO_HEADER"] = prev_value

        # parse if wanted
        if parsed:
            parsed_version_info = self.parse_binary_c_version_info(raw_version_info)
            return parsed_version_info

        return raw_version_info

    def parse_binary_c_version_info(self, version_info_string: str) -> dict:
        """
        Function that parses the binary_c version info. Long function with a lot of branches

        Args:
            version_info_string: raw output of version_info call to binary_c

        Returns:
            Parsed version of the version info, which is a dictionary containing the keys: 'isotopes' for isotope info, 'argpairs' for argument pair info (TODO: explain), 'ensembles' for ensemble settings/info, 'macros' for macros, 'elements' for atomic element info, 'DTlimit' for (TODO: explain), 'nucleosynthesis_sources' for nucleosynthesis sources, and 'miscellaneous' for all those that were not caught by the previous groups. 'git_branch', 'git_build', 'revision' and 'email' are also keys, but its clear what those contain.
        """

        version_info_dict = {}

        # Clean data and put in correct shape
        splitted = version_info_string.strip().splitlines()
        cleaned = {el.strip() for el in splitted if not el == ""}

        ##########################
        # Network:
        # Split off all the networks and parse the info.

        networks = {el for el in cleaned if el.startswith("Network ")}
        cleaned = cleaned - networks

        networks_dict = {}
        for el in networks:
            network_dict = {}
            split_info = el.split("Network ")[-1].strip().split("==")

            network_number = int(split_info[0])
            network_dict["network_number"] = network_number

            network_info_split = split_info[1].split(" is ")

            shortname = network_info_split[0].strip()
            network_dict["shortname"] = shortname

            if not network_info_split[1].strip().startswith(":"):
                network_split_info_extra = network_info_split[1].strip().split(":")

                longname = network_split_info_extra[0].strip()
                network_dict["longname"] = longname

                implementation = (
                    network_split_info_extra[1].strip().replace("implemented in", "")
                )
                if implementation:
                    network_dict["implemented_in"] = [
                        i.strip("()") for i in implementation.strip().split()
                    ]

            networks_dict[network_number] = copy.deepcopy(network_dict)
        version_info_dict["networks"] = networks_dict if networks_dict else None

        ##########################
        # Isotopes:
        # Split off
        isotopes = {el for el in cleaned if el.startswith("Isotope ")}
        cleaned -= isotopes

        isotope_dict = {}
        for el in isotopes:
            split_info = el.split("Isotope ")[-1].strip().split(" is ")

            isotope_info = split_info[-1]
            name = isotope_info.split(" ")[0].strip()

            # Get details
            mass_g = float(
                isotope_info.split(",")[0].split("(")[1].split("=")[-1][:-2].strip()
            )
            mass_amu = float(
                isotope_info.split(",")[0].split("(")[-1].split("=")[-1].strip()
            )
            mass_mev = float(
                isotope_info.split(",")[-3].split("=")[-1].replace(")", "").strip()
            )
            A = int(isotope_info.split(",")[-1].strip().split("=")[-1].replace(")", ""))
            Z = int(isotope_info.split(",")[-2].strip().split("=")[-1])

            #
            isotope_dict[int(split_info[0])] = {
                "name": name,
                "Z": Z,
                "A": A,
                "mass_mev": mass_mev,
                "mass_g": mass_g,
                "mass_amu": mass_amu,
            }
        version_info_dict["isotopes"] = isotope_dict if isotope_dict else None

        ##########################
        # Arg pairs:
        # Split off
        argpairs = {el for el in cleaned if el.startswith("ArgPair")}
        cleaned -= argpairs

        argpair_dict = {}
        for el in sorted(argpairs):
            split_info = el.split("ArgPair ")[-1].split(" ")

            if not argpair_dict.get(split_info[0], None):
                argpair_dict[split_info[0]] = {split_info[1]: split_info[2]}
            else:
                argpair_dict[split_info[0]][split_info[1]] = split_info[2]

        version_info_dict["argpairs"] = argpair_dict if argpair_dict else None

        ##########################
        # ensembles:
        # Split off
        ensembles = {el for el in cleaned if el.startswith("Ensemble")}
        cleaned -= ensembles

        ensemble_dict = {}
        ensemble_filter_dict = {}
        for el in ensembles:
            split_info = el.split("Ensemble ")[-1].split(" is ")

            if len(split_info) > 1:
                if not split_info[0].startswith("filter"):
                    ensemble_dict[int(split_info[0])] = split_info[-1]
                else:
                    filter_no = int(split_info[0].replace("filter ", ""))
                    ensemble_filter_dict[filter_no] = split_info[-1]

        version_info_dict["ensembles"] = ensemble_dict if ensemble_dict else None
        version_info_dict["ensemble_filters"] = (
            ensemble_filter_dict if ensemble_filter_dict else None
        )

        ##########################
        # macros:
        # Split off
        macros = {el for el in cleaned if el.startswith("macroxyz")}
        cleaned -= macros

        param_type_dict = {
            "STRING": str,
            "FLOAT": float,
            "MACRO": str,
            "INT": int,
            "LONG_INT": int,
            "UINT": int,
        }

        macros_dict = {}
        for el in macros:
            split_info = el.split("macroxyz ")[-1].split(" : ")
            param_type = split_info[0]

            new_split = "".join(split_info[1:]).split(" is ")
            param_name = new_split[0].strip()
            param_value = " is ".join(new_split[1:])
            param_value = param_value.strip()

            # print("macro ",param_name,"=",param_value," float?",isfloat(param_value)," int?",isint(param_value))

            # If we're trying to set the value to "on", check that
            # it doesn't already exist. If it does, do nothing, as the
            # extra information is better than just "on"
            if param_name in macros_dict:
                # print("already exists (is ",macros_dict[param_name]," float? ",isfloat(macros_dict[param_name]),", int? ",isint(macros_dict[param_name]),") : check that we can improve it")
                if macros_dict[param_name] == "on":
                    # update with better value
                    store = True
                elif (
                    isfloat(macros_dict[param_name]) is False
                    and isfloat(param_value) is True
                ):
                    # store the number we now have to replace the non-number we had
                    store = True
                else:
                    # don't override existing number
                    store = False

                # if store:
                #    print("Found improved macro value of param",param_name,", was ",macros_dict[param_name],", is",param_value)
                # else:
                #    print("Cannot improve: use old value")
            else:
                store = True

            if store:
                # Sometimes the macros have extra information behind it.
                # Needs an update in outputting by binary_c (RGI: what does this mean David???)
                try:
                    macros_dict[param_name] = param_type_dict[param_type](param_value)
                except ValueError:
                    macros_dict[param_name] = str(param_value)

        version_info_dict["macros"] = macros_dict if macros_dict else None

        ##########################
        # Elements:
        # Split off:
        elements = {el for el in cleaned if el.startswith("Element")}
        cleaned -= elements

        # Fill dict:
        elements_dict = {}
        for el in elements:
            split_info = el.split("Element ")[-1].split(" : ")
            name_info = split_info[0].split(" is ")

            # get isotope info
            isotopes = {}
            if not split_info[-1][0] == "0":
                isotope_string = split_info[-1].split(" = ")[-1]
                isotopes = {
                    int(split_isotope.split("=")[0]): split_isotope.split("=")[1]
                    for split_isotope in isotope_string.split(" ")
                }

            elements_dict[int(name_info[0])] = {
                "name": name_info[-1],
                "atomic_number": int(name_info[0]),
                "amt_isotopes": len(isotopes),
                "isotopes": isotopes,
            }
        version_info_dict["elements"] = elements_dict if elements_dict else None

        ##########################
        # dt_limits:
        # split off
        dt_limits = {el for el in cleaned if el.startswith("DTlimit")}
        cleaned -= dt_limits

        # Fill dict
        dt_limits_dict = {}
        for el in dt_limits:
            split_info = el.split("DTlimit ")[-1].split(" : ")
            dt_limits_dict[split_info[1].strip()] = {
                "index": int(split_info[0]),
                "value": float(split_info[-1]),
            }

        version_info_dict["dt_limits"] = dt_limits_dict if dt_limits_dict else None

        ##############################
        # Units

        units = {el for el in cleaned if el.startswith("Unit ")}
        cleaned -= units
        units_dict = {}
        for el in units:
            split_info = el.split("Unit ")[-1].split(",")
            s = split_info[0].split(" is ")

            if len(s) == 2:
                long, short = [i.strip().strip('"') for i in s]
            elif len(s) == 1:
                long, short = None, s[0]
            else:
                print("Warning: Failed to split unit string {}".format(el))

            to_cgs = (split_info[1].split())[3].strip().strip('"')
            code_units = split_info[2].split()
            code_unit_type_num = int(code_units[3].strip().strip('"'))
            code_unit_type = code_units[4].strip().strip('"')
            code_unit_cgs_value = code_units[9].strip().strip('"').strip(")")
            units_dict[long] = {
                "long": long,
                "short": short,
                "to_cgs": to_cgs,
                "code_unit_type_num": code_unit_type_num,
                "code_unit_type": code_unit_type,
                "code_unit_cgs_value": code_unit_cgs_value,
            }

        # Add the list of units
        units = {el for el in cleaned if el.startswith("Units: ")}
        cleaned -= units
        for el in units:
            el = el[7:]  # removes "Units: "
            units_dict["units list"] = el.strip("Units:")

        version_info_dict["units"] = units_dict

        ##########################
        # Nucleosynthesis sources:
        # Split off
        nucsyn_sources = {el for el in cleaned if el.startswith("Nucleosynthesis")}
        cleaned -= nucsyn_sources

        # Fill dict
        nucsyn_sources_dict = {}
        for el in nucsyn_sources:
            split_info = el.split("Nucleosynthesis source")[-1].strip().split(" is ")
            nucsyn_sources_dict[int(split_info[0])] = split_info[-1]

        version_info_dict["nucleosynthesis_sources"] = (
            nucsyn_sources_dict if nucsyn_sources_dict else None
        )

        ##########################
        # miscellaneous:
        # All those that I didn't catch with the above filters. Could try to get some more out though.

        misc_dict = {}

        # Filter out git revision
        git_revision = [el for el in cleaned if el.startswith("git revision")]
        misc_dict["git_revision"] = (
            git_revision[0].split("git revision ")[-1].replace('"', "")
        )
        cleaned -= set(git_revision)

        # filter out git url
        git_url = [el for el in cleaned if el.startswith("git URL")]
        misc_dict["git_url"] = git_url[0].split("git URL ")[-1].replace('"', "")
        cleaned -= set(git_url)

        # filter out version
        version = [el for el in cleaned if el.startswith("Version")]
        misc_dict["version"] = str(version[0].split("Version ")[-1])
        cleaned -= set(version)

        git_branch = [el for el in cleaned if el.startswith("git branch")]
        misc_dict["git_branch"] = (
            git_branch[0].split("git branch ")[-1].replace('"', "")
        )
        cleaned -= set(git_branch)

        build = [el for el in cleaned if el.startswith("Build")]
        misc_dict["build"] = build[0].split("Build: ")[-1].replace('"', "")
        cleaned -= set(build)

        email = [el for el in cleaned if el.startswith("Email")]
        misc_dict["email"] = email[0].split("Email ")[-1].split(",")
        cleaned -= set(email)

        other_items = {el for el in cleaned if " is " in el}
        cleaned -= other_items

        for el in other_items:
            split = el.split(" is ")
            key = split[0].strip()
            val = " is ".join(split[1:]).strip()
            if key in misc_dict:
                misc_dict[key + " (alt)"] = val
            else:
                misc_dict[key] = val

        misc_dict["uncaught"] = list(cleaned)

        version_info_dict["miscellaneous"] = misc_dict if misc_dict else None
        return version_info_dict

    def minimum_stellar_mass(self):
        """
        Function to return the minimum stellar mass (in Msun) from binary_c.
        """
        if not self._minimum_stellar_mass:
            self._minimum_stellar_mass = self.return_binary_c_version_info(parsed=True)[
                "macros"
            ]["BINARY_C_MINIMUM_STELLAR_MASS"]
        return self._minimum_stellar_mass
