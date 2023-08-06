"""
Module containing the metadata functions for the binarycpython package.

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import json
import platform

from binarycpython.utils.dicts import (
    multiply_values_dict,
)
from binarycpython.utils.ensemble import (
    binaryc_json_serializer,
)
from binarycpython.utils.functions import (
    now,
)


class metadata:
    """
    Extension to the population grid object that contains functionality to handle the metadata that will be put in the ensemble
    """

    def __init__(self, **kwargs):
        """
        Init function for the metadata class
        """

        return

    def add_system_metadata(self):
        """
        Add system's metadata to the grid_ensemble_results, and add some system information to metadata.
        """

        # add metadata if it doesn't exist
        if not "metadata" in self.grid_ensemble_results:
            self.grid_ensemble_results["metadata"] = {}

        # add date
        self.grid_ensemble_results["metadata"]["date"] = now()

        # add platform and build information
        self.grid_ensemble_results["metadata"]["platform"] = platform.platform()
        self.grid_ensemble_results["metadata"]["platform_uname"] = list(
            platform.uname()
        )
        self.grid_ensemble_results["metadata"]["platform_machine"] = platform.machine()
        self.grid_ensemble_results["metadata"]["platform_node"] = platform.node()
        self.grid_ensemble_results["metadata"]["platform_release"] = platform.release()
        self.grid_ensemble_results["metadata"]["platform_version"] = platform.version()
        self.grid_ensemble_results["metadata"][
            "platform_processor"
        ] = platform.processor()
        self.grid_ensemble_results["metadata"]["platform_python_build"] = " ".join(
            platform.python_build()
        )
        self.grid_ensemble_results["metadata"][
            "platform_python_version"
        ] = platform.python_version()

        # Get hostname
        self.grid_ensemble_results["metadata"]["hostname"] = platform.uname()[1]

        # Calculate time elapsed
        self.grid_ensemble_results["metadata"]["duration"] = self.time_elapsed()

        # Calculate cpu time
        self.grid_ensemble_results["metadata"]["CPU_time"] = self.CPU_time()

    def add_ensemble_metadata(self, combined_output_dict):
        """
        Function to add metadata to the grid_ensemble_results and grid_options
        """

        self.grid_ensemble_results["metadata"] = {}

        self.grid_ensemble_results["metadata"]["population_id"] = self.grid_options[
            "_population_id"
        ]
        self.grid_ensemble_results["metadata"][
            "total_probability_weighted_mass"
        ] = combined_output_dict["_total_probability_weighted_mass_run"]
        self.grid_ensemble_results["metadata"][
            "factored_in_probability_weighted_mass"
        ] = False
        if self.grid_options["ensemble_factor_in_probability_weighted_mass"]:
            multiply_values_dict(
                self.grid_ensemble_results["ensemble"],
                1.0
                / self.grid_ensemble_results["metadata"][
                    "total_probability_weighted_mass"
                ],
            )
            self.grid_ensemble_results["metadata"][
                "factored_in_probability_weighted_mass"
            ] = True
        self.grid_ensemble_results["metadata"]["_killed"] = self.grid_options["_killed"]

        # Add settings of the populations
        all_info = self.return_all_info(
            include_population_settings=True,
            include_binary_c_defaults=True,
            include_binary_c_version_info=True,
            include_binary_c_help_all=True,
        )
        self.grid_ensemble_results["metadata"]["settings"] = json.loads(
            json.dumps(all_info, default=binaryc_json_serializer, ensure_ascii=False)
        )

        ##############################
        # Update grid options
        for x in self._metadata_keylist():
            self.grid_options[x] = combined_output_dict[x]
        self.grid_options["_failed_systems_error_codes"] = list(
            set(combined_output_dict["_failed_systems_error_codes"])
        )

    def _metadata_keylist(self):
        """
        Function that returns the list of metadata keys

        TODO: Consider just setting this list as a property of the object in the init
        """
        return [
            "_failed_count",
            "_failed_prob",
            "_errors_exceeded",
            "_errors_found",
            "_probtot",
            "_count",
            "_total_mass_run",
            "_total_probability_weighted_mass_run",
            "_zero_prob_stars_skipped",
            "_killed",
        ]
