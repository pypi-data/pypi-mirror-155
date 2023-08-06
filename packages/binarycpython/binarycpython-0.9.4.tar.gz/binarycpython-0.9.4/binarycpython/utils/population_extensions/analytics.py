"""
The class extension for the population object that contains analytics functionality
"""

# pylint: disable=E1101

import time


class analytics:
    """
    Extension for the Population class containing the functions for analytics
    """

    def __init__(self, **kwargs):
        """
        Init function for the analytics class
        """

        return

    #######################
    # time used functions
    #######################

    def make_analytics_dict(self):
        """
        Function to create the analytics dictionary
        """

        print("Do analytics")

        analytics_dict = {}

        if self.grid_options["do_analytics"]:
            # Put all interesting stuff in a variable and output that afterwards, as analytics of the run.
            analytics_dict = {
                "population_id": self.grid_options["_population_id"],
                "evolution_type": self.grid_options["evolution_type"],
                "failed_count": self.grid_options["_failed_count"],
                "failed_prob": self.grid_options["_failed_prob"],
                "failed_systems_error_codes": self.grid_options[
                    "_failed_systems_error_codes"
                ].copy(),
                "errors_exceeded": self.grid_options["_errors_exceeded"],
                "errors_found": self.grid_options["_errors_found"],
                "total_probability": self.grid_options["_probtot"],
                "total_count": self.grid_options["_count"],
                "start_timestamp": self.grid_options["_start_time_evolution"],
                "end_timestamp": self.grid_options["_end_time_evolution"],
                "time_elapsed": self.time_elapsed(),
                "total_mass_run": self.grid_options["_total_mass_run"],
                "total_probability_weighted_mass_run": self.grid_options[
                    "_total_probability_weighted_mass_run"
                ],
                "zero_prob_stars_skipped": self.grid_options[
                    "_zero_prob_stars_skipped"
                ],
            }

        if "metadata" in self.grid_ensemble_results:
            # Add analytics dict to the metadata too:
            self.grid_ensemble_results["metadata"].update(analytics_dict)
            print("Added analytics to metadata")
            self.add_system_metadata()
        else:
            # use existing analytics dict
            analytics_dict = self.grid_ensemble_results.get("metadata", {})

        return analytics_dict

    def set_time(self, when):
        """
        Function to set the timestamp at when, where when is 'start' or 'end'.

        If when == end, we also calculate the time elapsed.
        """
        self.grid_options["_" + when + "_time_evolution"] = time.time()
        if when == "end":
            self.grid_options["_time_elapsed"] = self.time_elapsed(force=True)

    def time_elapsed(self, force=False):
        """
        Function to return how long a population object has been running.

        We return the cached value if it's available, and calculate
        the time elapsed if otherwise or if force is True
        """
        for x in ["_start_time_evolution", "_end_time_evolution"]:
            if not self.grid_options[x]:
                self.grid_options[x] = time.time()
                # print("{} missing : {}".format(x, self.grid_options[x]))

        if force or "_time_elapsed" not in self.grid_options:
            self.grid_options["_time_elapsed"] = (
                self.grid_options["_end_time_evolution"]
                - self.grid_options["_start_time_evolution"]
            )
            # print(
            #     "set time elapsed = {} - {} = {}".format(
            #         self.grid_options["_end_time_evolution"],
            #         self.grid_options["_start_time_evolution"],
            #         self.grid_options["_time_elapsed"],
            #     )
            # )

        return self.grid_options["_time_elapsed"]

    def CPU_time(self):
        """
        Function to return how much CPU time we've used
        """
        dt = self.grid_options["_time_elapsed"]

        ncpus = self.grid_options.get("num_processes", 1)

        # print("CPU time : dt={} n={} -> {}".format(dt, ncpus, dt * ncpus))

        return dt * ncpus
