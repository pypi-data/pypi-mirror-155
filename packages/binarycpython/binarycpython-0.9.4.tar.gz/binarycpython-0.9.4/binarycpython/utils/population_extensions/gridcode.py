"""
Module containing the gridcode generation functions for the binarycpython package.

This class object is an extension to the population grid object
"""

# pylint: disable=E1101

import datetime
import importlib
import json
import os
from typing import Union, Any


_count = 0  # used for file symlinking (for testing only)
_numba = False  # activate experimental numba code?


class gridcode:
    """
    Extension to the population grid object that contains functionality to handle the metadata that will be put in the ensemble
    """

    def __init__(self, **kwargs):
        """
        Init function for the gridcode class
        """

        return

    ###################################################
    # Grid code functions
    #
    # Function below are used to run populations with
    # a variable grid
    ###################################################
    def _gridcode_filename(self):
        """
        Returns a filename for the gridcode.
        """
        if self.HPC_job():
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_grid_{population_id}.{jobid}.py".format(
                    population_id=self.grid_options["_population_id"],
                    jobid=self.jobID(),
                ),
            )
        else:
            filename = os.path.join(
                self.grid_options["tmp_dir"],
                "binary_c_grid_{population_id}.py".format(
                    population_id=self.grid_options["_population_id"]
                ),
            )
        return filename

    def _add_code(self, *args, indent=0):
        """
        Function to add code to the grid code string

        add code to the code_string

        indent (=0) is added once at the beginning
        mindent (=0) is added for every line

        don't use both!
        """

        indent_block = self._indent_block(indent)
        for thing in args:
            self.code_string += indent_block + thing

    def _indent_block(self, n=0):
        """
        return an indent block, with n extra blocks in it
        """
        return (self.indent_depth + n) * self.indent_string

    def _increment_indent_depth(self, delta):
        """
        increment the indent indent_depth by delta
        """
        self.indent_depth += delta

    def _generate_grid_code(self, dry_run=False):
        """
        Function that generates the code from which the population will be made.

        dry_run: when True, it will return the starcount at the end so that we know
        what the total number of systems is.

        The phasevol values are handled by generating a second array

        Results in a generated file that contains a system_generator function.

        # TODO: make sure running systems with multiplicity 3+ is also possible.
        # TODO: there is a lot of things going on in this function. Make sure to describe clearly what happens here.
        """
        self.verbose_print("Generating grid code", self.grid_options["verbosity"], 1)

        total_grid_variables = len(self.grid_options["_grid_variables"])

        self._add_code(
            # Import packages
            "import math\n",
            "import numpy as np\n",
            "from collections import OrderedDict\n",
            "from binarycpython.utils.useful_funcs import *\n",
            "import numba" if _numba else "",
            "\n\n",
            # Make the function
            "def grid_code(self, print_results=True):\n",
        )

        # Increase indent_depth
        self._increment_indent_depth(+1)

        self._add_code(
            # Write some info in the function
            "# Grid code generated on {}\n".format(datetime.datetime.now().isoformat()),
            "# This function generates the systems that will be evolved with binary_c\n\n"
            # Set some values in the generated code:
            "# Set initial values\n",
            "_total_starcount = 0\n",
            "starcounts = [0 for i in range({})]\n".format(total_grid_variables + 1),
            "probabilities = {}\n",
            "probabilities_list = [0 for i in range({})]\n".format(
                total_grid_variables + 1
            ),
            "probabilities_sum = [0 for i in range({})]\n".format(
                total_grid_variables + 1
            ),
            "parameter_dict = {}\n",
            "phasevol = 1\n",
        )

        # Set up the system parameters
        self._add_code(
            "M_1 = None\n",
            "M_2 = None\n",
            "M_3 = None\n",
            "M_4 = None\n",
            "orbital_period = None\n",
            "orbital_period_triple = None\n",
            "orbital_period_quadruple = None\n",
            "eccentricity = None\n",
            "eccentricity2 = None\n",
            "eccentricity3 = None\n",
            "\n",
            # Prepare the probability
            "# set probability lists\n",
        )

        for grid_variable_el in sorted(
            self.grid_options["_grid_variables"].items(),
            key=lambda x: x[1]["grid_variable_number"],
        ):
            # Make probabilities dict
            grid_variable = grid_variable_el[1]
            self._add_code('probabilities["{}"] = 0\n'.format(grid_variable["name"]))

        #################################################################################
        # Start of code generation
        #################################################################################
        self._add_code("\n")

        # turn vb to True to have debugging output
        vb = False

        # Generate code
        for loopnr, grid_variable_el in enumerate(
            sorted(
                self.grid_options["_grid_variables"].items(),
                key=lambda x: x[1]["grid_variable_number"],
            )
        ):
            self.verbose_print(
                "Constructing/adding: {}".format(grid_variable_el[0]),
                self.grid_options["verbosity"],
                2,
            )
            grid_variable = grid_variable_el[1]

            ####################
            # top code
            if grid_variable["topcode"]:
                self._add_code(grid_variable["topcode"])

            #########################
            # Set up the for loop
            # Add comment for for loop
            self._add_code(
                "# for loop for variable {name} gridtype {gridtype}".format(
                    name=grid_variable["name"],
                    gridtype=grid_variable["gridtype"],
                )
                + "\n",
                "sampled_values_{} = {}".format(
                    grid_variable["name"], grid_variable["samplerfunc"]
                )
                + "\n",
            )

            if vb:
                self._add_code(
                    "print('samples','{name}',':',sampled_values_{name})\n".format(
                        name=grid_variable["name"],
                    )
                )

            if vb:
                self._add_code(
                    "print('sample {name} from',sampled_values_{name})".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )

            # calculate number of values and starting location
            #
            # if we're sampling a continuous variable, we
            # have one fewer grid point than the length of the
            # sampled_values list
            if grid_variable["gridtype"] in [
                "centred",
                "centre",
                "center",
                "edge",
                "left edge",
                "left",
                "right",
                "right edge",
            ]:
                offset = -1
            elif grid_variable["gridtype"] == "discrete":
                # discrete variables sample all the points
                offset = 0

            start = 0

            # for loop over the variable
            if vb:
                self._add_code(
                    'print("var {name} values ",sampled_values_{name}," len ",len(sampled_values_{name})+{offset}," gridtype {gridtype} offset {offset}\\n")\n'.format(
                        name=grid_variable["name"],
                        offset=offset,
                        gridtype=grid_variable["gridtype"],
                    )
                )

            stop = "len(sampled_values_{name})+{offset}".format(
                name=grid_variable["name"], offset=offset
            )

            if _numba and grid_variable["dry_parallel"]:
                # Parallel outer loop
                self._add_code("@numba.jit(parallel=True)\n")
                self._add_code("def __parallel_func(phasevol,_total_starcount):\n")
                self._increment_indent_depth(+1)
                self._add_code(
                    "for {name}_sample_number in numba.prange({stop}):\n".format(
                        name=grid_variable["name"],
                        stop=stop,
                    )
                )
                self._increment_indent_depth(+1)
                if start > 0:
                    self._add_code(
                        "if {name}_sample_number < {start}:\n".format(
                            name=grid_variable["name"],
                            start=start,
                        )
                    )
                    self._add_code("continue\n", indent=1)
            else:
                self._add_code(
                    "for {name}_sample_number in range({start},{stop}):\n".format(
                        name=grid_variable["name"],
                        start=start,
                        stop=stop,
                    )
                )
                self._increment_indent_depth(+1)

            # {}_this_index is this grid point's index
            # {}_prev_index and {}_next_index are the previous and next grid points,
            # (which can be None if there is no previous or next, or if
            #  previous and next should not be used: this is deliberate)
            #

            if grid_variable["gridtype"] == "discrete":
                # discrete grids only care about this,
                # both prev and next should be None to
                # force errors where they are used
                self._add_code(
                    "{name}_this_index = {name}_sample_number ".format(
                        name=grid_variable["name"],
                    ),
                )
                self._add_code(
                    "\n",
                    "{name}_prev_index = None if {name}_this_index == 0 else ({name}_this_index - 1) ".format(
                        name=grid_variable["name"],
                    ),
                    "\n",
                )
                self._add_code(
                    "\n",
                    "{name}_next_index = None if {name}_this_index >= (len(sampled_values_{name})+{offset} - 1) else ({name}_this_index + 1)".format(
                        name=grid_variable["name"], offset=offset
                    ),
                    "\n",
                )

            elif grid_variable["gridtype"] in [
                "centred",
                "centre",
                "center",
                "edge",
                "left",
                "left edge",
            ]:

                # left and centred grids
                self._add_code(
                    "if {}_sample_number == 0:\n".format(grid_variable["name"])
                )
                self._add_code(
                    "{}_this_index = 0;\n".format(grid_variable["name"]), indent=1
                )
                self._add_code("else:\n")
                self._add_code(
                    "{name}_this_index = {name}_sample_number ".format(
                        name=grid_variable["name"]
                    ),
                    indent=1,
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_prev_index = ({name}_this_index - 1) if {name}_this_index > 0 else None ".format(
                        name=grid_variable["name"]
                    )
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_next_index = {name}_this_index + 1".format(
                        name=grid_variable["name"]
                    )
                )
                self._add_code("\n")

            elif grid_variable["gridtype"] in ["right", "right edge"]:

                # right edged grid
                self._add_code(
                    "if {name}_sample_number == 0:\n".format(name=grid_variable["name"])
                )
                self._add_code(
                    "{name}_this_index = 1;\n".format(name=grid_variable["name"]),
                    indent=1,
                )
                self._add_code("else:\n")
                self._add_code(
                    "{name}_this_index = {name}_sample_number + 1 ".format(
                        name=grid_variable["name"],
                    ),
                    indent=1,
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_prev_index = {name}_this_index - 1".format(
                        name=grid_variable["name"]
                    )
                )
                self._add_code("\n")
                self._add_code(
                    "{name}_next_index = ({name}_this_index + 1) if {name}_this_index < len(sampled_values_{name}) else None".format(
                        name=grid_variable["name"]
                    )
                )
                self._add_code("\n")

            # calculate phase volume
            if grid_variable["dphasevol"] == -1:
                # no phase volume required so set it to 1.0
                self._add_code(
                    "dphasevol_{name} = 1.0 # 666\n".format(name=grid_variable["name"])
                )

            elif grid_variable["gridtype"] in ["right", "right edge"]:
                # right edges always have this and prev defined
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_this_index] - sampled_values_{name}[{name}_prev_index])".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )
            elif grid_variable["gridtype"] == "discrete":
                # discrete might have next defined, use it if we can,
                # otherwise use prev
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_next_index] - sampled_values_{name}[{name}_this_index]) if {name}_next_index else (sampled_values_{name}[{name}_this_index] - sampled_values_{name}[{name}_prev_index])".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )
            else:
                # left and centred always have this and next defined
                self._add_code(
                    "dphasevol_{name} = (sampled_values_{name}[{name}_next_index] - sampled_values_{name}[{name}_this_index])".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )

            ##############
            # Add phasevol check:
            self._add_code(
                "if dphasevol_{name} <= 0:\n".format(name=grid_variable["name"])
            )

            #   n that case we need another local variable which will prevent it from being run but will track those parameters
            # Add phasevol check action:
            self._add_code(
                'print("Grid generator: dphasevol_{name} <= 0! (this=",{name}_this_index,"=",sampled_values_{name}[{name}_this_index],", next=",{name}_next_index,"=",sampled_values_{name}[{name}_next_index],") Skipping current sample.")'.format(
                    name=grid_variable["name"]
                )
                + "\n",
                "continue\n",
                indent=1,
            )

            if vb:
                self._add_code(
                    "print('sample {name} from ',sampled_values_{name},' at this=',{name}_this_index,', next=',{name}_next_index)".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )

            # select sampled point location based on gridtype (left, centre or right)
            if grid_variable["gridtype"] in [
                "edge",
                "left",
                "left edge",
                "right",
                "right edge",
                "discrete",
            ]:
                self._add_code(
                    "{name} = sampled_values_{name}[{name}_this_index]".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )
            elif grid_variable["gridtype"] in ["centred", "centre", "center"]:
                self._add_code(
                    "{name} = 0.5 * (sampled_values_{name}[{name}_next_index] + sampled_values_{name}[{name}_this_index])".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )
            else:
                msg = "Unknown gridtype value {type}.".format(
                    type=grid_variable["gridtype"]
                )
                raise ValueError(msg)

            if vb:
                self._add_code(
                    "print('hence {name} = ',{name})\n".format(
                        name=grid_variable["name"]
                    )
                )

            #################################################################################
            # Check condition and generate for loop

            # If the grid variable has a condition, write the check and the action
            if grid_variable["condition"]:
                self._add_code(
                    # Add comment
                    "# Condition for {name}\n".format(name=grid_variable["name"]),
                    # Add condition check
                    "if not {condition}:\n".format(
                        condition=grid_variable["condition"]
                    ),
                    indent=0,
                )

                # Add condition failed action:
                if self.grid_options["verbosity"] >= 4:
                    self._add_code(
                        'print("Grid generator: Condition for {name} not met!")'.format(
                            name=grid_variable["name"]
                        )
                        + "\n",
                        "continue" + "\n",
                        indent=1,
                    )
                else:
                    self._add_code(
                        "continue" + "\n",
                        indent=1,
                    )
                    # Add some whitespace
                self._add_code("\n")

            # Add some whitespace
            self._add_code("\n")

            #########################
            # Set up pre-code and value in some cases
            # Add pre-code
            if grid_variable["precode"]:
                self._add_code(
                    "{precode}".format(
                        precode=grid_variable["precode"].replace(
                            "\n", "\n" + self._indent_block(0)
                        )
                    )
                    + "\n"
                )

            # Set phasevol
            self._add_code(
                "phasevol *= dphasevol_{name}\n".format(
                    name=grid_variable["name"],
                )
            )

            #######################
            # Probabilities
            # Calculate probability
            self._add_code(
                "\n",
                "# Set probabilities\n",
                "dprob_{name} = dphasevol_{name} * ({probdist})".format(
                    name=grid_variable["name"],
                    probdist=grid_variable["probdist"],
                )
                + "\n",
                # Save probability sum
                "probabilities_sum[{n}] += dprob_{name}".format(
                    n=grid_variable["grid_variable_number"], name=grid_variable["name"]
                )
                + "\n",
            )

            if grid_variable["grid_variable_number"] == 0:
                self._add_code(
                    "probabilities_list[0] = dprob_{name}".format(
                        name=grid_variable["name"]
                    )
                    + "\n"
                )
            else:
                self._add_code(
                    "probabilities_list[{this}] = probabilities_list[{prev}] * dprob_{name}".format(
                        this=grid_variable["grid_variable_number"],
                        prev=grid_variable["grid_variable_number"] - 1,
                        name=grid_variable["name"],
                    )
                    + "\n"
                )

            ##############
            # postcode
            if grid_variable["postcode"]:
                self._add_code(
                    "{postcode}".format(
                        postcode=grid_variable["postcode"].replace(
                            "\n", "\n" + self._indent_block(0)
                        )
                    )
                    + "\n"
                )

            #######################
            # Increment starcount for this parameter
            self._add_code(
                "\n",
                "# Increment starcount for {name}\n".format(name=grid_variable["name"]),
                "starcounts[{n}] += 1".format(
                    n=grid_variable["grid_variable_number"],
                )
                + "\n",
                # Add value to dict
                'parameter_dict["{name}"] = {name}'.format(
                    name=grid_variable["parameter_name"]
                )
                + "\n",
                "\n",
            )

            self._increment_indent_depth(-1)

            # The final parts of the code, where things are returned, are within the deepest loop,
            # but in some cases code from a higher loop needs to go under it again
            # SO I think its better to put an if statement here that checks
            # whether this is the last loop.
            if loopnr == len(self.grid_options["_grid_variables"]) - 1:
                self._write_gridcode_system_call(
                    grid_variable,
                    dry_run,
                    grid_variable["branchpoint"],
                    grid_variable["branchcode"],
                )

            # increment indent_depth
            self._increment_indent_depth(+1)

            ####################
            # bottom code
            if grid_variable["bottomcode"]:
                self._add_code(grid_variable["bottomcode"])

        self._increment_indent_depth(-1)
        self._add_code("\n")

        # Write parts to write below the part that yield the results.
        # this has to go in a reverse order:
        # Here comes the stuff that is put after the deepest nested part that calls returns stuff.
        # Here we will have a
        reverse_sorted_grid_variables = sorted(
            self.grid_options["_grid_variables"].items(),
            key=lambda x: x[1]["grid_variable_number"],
            reverse=True,
        )
        for loopnr, grid_variable_el in enumerate(reverse_sorted_grid_variables):
            grid_variable = grid_variable_el[1]

            self._increment_indent_depth(+1)
            self._add_code(
                "#" * 40 + "\n",
                "# Code below is for finalising the handling of this iteration of the parameter {name}\n".format(
                    name=grid_variable["name"]
                ),
            )

            # Set phasevol
            # TODO: fix. this isn't supposed to be the value that we give it here. discuss
            self._add_code(
                "phasevol /= dphasevol_{name}\n\n".format(name=grid_variable["name"])
            )

            self._increment_indent_depth(-2)

            if _numba and grid_variable["dry_parallel"]:
                self._add_code("__parallel_func(phasevol,_total_starcount)\n")
                self._increment_indent_depth(-1)

            # Check the branchpoint part here. The branchpoint makes sure that we can construct
            # a grid with several multiplicities and still can make the system calls for each
            # multiplicity without reconstructing the grid each time
            if grid_variable["branchpoint"] > 0:

                self._increment_indent_depth(+1)

                self._add_code(
                    # Add comment
                    "# Condition for branchpoint at {}".format(
                        reverse_sorted_grid_variables[loopnr + 1][1]["name"]
                    )
                    + "\n",
                    # # Add condition check
                    #     "if not {}:".format(grid_variable["condition"])
                    #     + "\n"
                    # Add branchpoint
                    "if multiplicity=={}:".format(grid_variable["branchpoint"]) + "\n",
                )

                self._write_gridcode_system_call(
                    reverse_sorted_grid_variables[loopnr + 1][1],
                    dry_run,
                    grid_variable["branchpoint"],
                    grid_variable["branchcode"],
                )
                self._increment_indent_depth(-1)
                self._add_code("\n")

        ###############################
        # Finalise print statements
        #
        self._increment_indent_depth(+1)
        self._add_code("\n", "#" * 40 + "\n", "if print_results:\n")
        self._add_code(
            "print('Grid has handled {starcount} stars with a total probability of {probtot:g}'.format(starcount=_total_starcount,probtot=self.grid_options['_probtot']))\n",
            indent=1,
        )

        ################
        # Finalise return statement for dry run.
        #
        if dry_run:
            self._add_code("return _total_starcount\n")

        self._increment_indent_depth(-1)
        #################################################################################
        # Stop of code generation. Here the code is saved and written

        # Save the grid code to the grid_options
        self.verbose_print(
            "Save grid code to grid_options", self.grid_options["verbosity"], 1
        )

        self.grid_options["code_string"] = self.code_string

        # Write to file
        gridcode_filename = self._gridcode_filename()

        self.grid_options["gridcode_filename"] = gridcode_filename

        self.verbose_print(
            "{blue}Write grid code to {file} [dry_run = {dry}]{reset}".format(
                blue=self.ANSI_colours["blue"],
                file=gridcode_filename,
                dry=dry_run,
                reset=self.ANSI_colours["reset"],
            ),
            self.grid_options["verbosity"],
            1,
        )

        with self.open(gridcode_filename, "w", encoding="utf-8") as file:
            file.write(self.code_string)

        # perhaps create symlink
        if not self.HPC_job() and self.grid_options["symlink_latest_gridcode"]:
            global _count
            symlink = os.path.join(
                self.grid_options["tmp_dir"], "binary_c_grid-latest" + str(_count)
            )
            _count += 1
            try:
                os.unlink(symlink)
            except:
                pass

            try:
                os.symlink(gridcode_filename, symlink)
                self.verbose_print(
                    "{blue}Symlinked grid code to {symlink} {reset}".format(
                        blue=self.ANSI_colours["blue"],
                        symlink=symlink,
                        reset=self.ANSI_colours["reset"],
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
            except OSError:
                print("symlink failed")

    def _write_gridcode_system_call(
        self, grid_variable, dry_run, branchpoint, branchcode
    ):
        """
        Function to write the block of code (as string) that handles the setting the final probability, taking into account the weight and repeat settings, incrementing the total starcount and total probability.

        Then if the run is a dry run we implement the dry_run_hook or pass depending on the settings. If it is not a dry run we yield the system dict
        """

        self._increment_indent_depth(+1)
        self._add_code("#" * 40 + "\n")

        if branchcode:
            self._add_code(
                "# Branch code\nif {branchcode}:\n".format(branchcode=branchcode)
            )

        if branchpoint:
            self._add_code(
                "# Code below will get evaluated for every system at this level of multiplicity (last one of that being {name})\n".format(
                    name=grid_variable["name"]
                )
            )
        else:
            self._add_code(
                "# Code below will get evaluated for every generated system\n"
            )

        # Factor in the custom weight input
        self._add_code(
            "\n",
            "# Weigh the probability by a custom weighting factor\n",
            'probability = self.grid_options["weight"] * probabilities_list[{n}]'.format(
                n=grid_variable["grid_variable_number"]
            )
            + "\n",
            # Take into account the multiplicity fraction:
            "\n",
            "# Factor the multiplicity fraction into the probability\n",
            "probability *= self._calculate_multiplicity_fraction(parameter_dict)"
            + "\n",
            # Divide by number of repeats
            "\n",
            "# Divide the probability by the number of repeats\n",
            'probability /= self.grid_options["repeat"]' + "\n",
            # Now we yield the system self.grid_options["repeat"] times.
            "\n",
            "# Loop over the repeats\n",
            'for _ in range(self.grid_options["repeat"]):' + "\n",
        )
        self._add_code(
            "_total_starcount += 1\n",
            # set probability and phasevol values into the system dict
            'parameter_dict["{p}"] = {p}'.format(p="probability") + "\n",
            'parameter_dict["{v}"] = {v}'.format(v="phasevol") + "\n",
            # Increment total probability
            "self._increment_probtot(probability)\n",
            indent=1,
        )

        if not dry_run:
            # Handle what is returned, or what is not.
            self._add_code("yield(parameter_dict)\n", indent=1)

        # If its a dry run, dont do anything with it
        else:
            # run the hook function, only if given
            if self.grid_options["dry_run_hook"]:
                self._add_code(
                    "self.grid_options['dry_run_hook'](self, parameter_dict)\n",
                    indent=1,
                )
            else:
                # or pass
                self._add_code("pass\n", indent=1)

        self._add_code("#" * 40 + "\n")

        self._increment_indent_depth(-1)

        return self.code_string

    def _load_grid_function(self):
        """
        Function that loads the grid code from file
        """

        # Code to load the
        self.verbose_print(
            message="Load grid code function from {file}".format(
                file=self.grid_options["gridcode_filename"]
            ),
            verbosity=self.grid_options["verbosity"],
            minimal_verbosity=1,
        )

        spec = importlib.util.spec_from_file_location(
            "binary_c_python_grid",
            os.path.join(self.grid_options["gridcode_filename"]),
        )
        grid_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grid_file)
        generator = grid_file.grid_code

        self.grid_options["_system_generator"] = generator

        self.verbose_print("Grid code loaded", self.grid_options["verbosity"], 1)

    def _last_grid_variable(self):
        """
        Function that returns the last grid variable (i.e. the one with the highest grid_variable_number)

        TODO: this function does not require this structure and can be simplified
        """

        number = len(self.grid_options["_grid_variables"])
        for grid_variable in self.grid_options["_grid_variables"]:
            if (
                self.grid_options["_grid_variables"][grid_variable][
                    "grid_variable_number"
                ]
                == number - 1
            ):
                return grid_variable

    def update_grid_variable(self, name: str, **kwargs) -> None:
        """
        Function to update the values of a grid variable.

        Args:
            name:
                name of the grid variable to be changed.
            **kwargs:
                key-value pairs to override the existing grid variable data. See add_grid_variable for these names.
        """

        if name in self.grid_options["_grid_variables"]:
            grid_variable = self.grid_options["_grid_variables"][name]

            # Set the value and print
            for key, value in kwargs.items():
                grid_variable[key] = value
                self.verbose_print(
                    "Updated grid variable: {}".format(
                        json.dumps(grid_variable, indent=4, ensure_ascii=False)
                    ),
                    self.grid_options["verbosity"],
                    1,
                )
        else:
            msg = "Unknown grid variable {} - please create it with the add_grid_variable() method.".format(
                name
            )
            raise KeyError(msg)

    def delete_grid_variable(
        self,
        name: str,
    ) -> None:
        """
        Function to delete a grid variable with the given name.

        Args:
            name:
                name of the grid variable to be deleted.
        """

        if name in self.grid_options["_grid_variables"]:
            del self.grid_options["_grid_variables"][name]
            self.verbose_print(
                "Deleted grid variable: {}".format(name),
                self.grid_options["verbosity"],
                1,
            )
        else:
            msg = "Failed to remove grid variable {}: please check it exists.".format(
                name
            )
            raise ValueError(msg)

    def rename_grid_variable(self, oldname: str, newname: str) -> None:
        """
        Function to rename a grid variable.

        note: this does NOT alter the order
        of the self.grid_options["_grid_variables"] dictionary.

        The order in which the grid variables are loaded into the grid is based on their
        `grid_variable_number` property

        Args:
            oldname:
                old name of the grid variable
            newname:
                new name of the grid variable
        """

        if oldname in self.grid_options["_grid_variables"]:
            self.grid_options["_grid_variables"][newname] = self.grid_options[
                "_grid_variables"
            ].pop(oldname)
            self.grid_options["_grid_variables"][newname]["name"] = newname
            self.verbose_print(
                "Rename grid variable: {} to {}".format(oldname, newname),
                self.grid_options["verbosity"],
                1,
            )
        else:
            msg = "Failed to rename grid variable {} to {}.".format(oldname, newname)
            raise ValueError(msg)

    def add_grid_variable(
        self,
        name: str,
        parameter_name: str,
        longname: str,
        valuerange: Union[list, str],
        samplerfunc: str,
        probdist: str,
        dphasevol: Union[str, int] = -1,
        gridtype: str = "centred",
        branchpoint: int = 0,
        branchcode: Union[str, None] = None,
        precode: Union[str, None] = None,
        postcode: Union[str, None] = None,
        topcode: Union[str, None] = None,
        bottomcode: Union[str, None] = None,
        condition: Union[str, None] = None,
        index: Union[int, None] = None,
        dry_parallel: Union[bool, None] = False,
    ) -> None:
        """
        Function to add grid variables to the grid_options.

        The execution of the grid generation will be through a nested for loop.
        Each of the grid variables will get create a deeper for loop.

        The real function that generates the numbers will get written to a new file in the TMP_DIR,
        and then loaded imported and evaluated.
        beware that if you insert some destructive piece of code, it will be executed anyway.
        Use at own risk.

        Args:
            name:
                name of parameter used in the grid Python code.
                This is evaluated as a parameter and you can use it throughout
                the rest of the function

                Examples::

                    name = 'lnM_1'

            parameter_name:
                name of the parameter in binary_c

                This name must correspond to a Python variable of the same name,
                which is automatic if parameter_name == name.

                Note: if parameter_name != name, you must set a
                      variable in "precode" or "postcode" to define a Python variable
                      called parameter_name

            longname:
                Long name of parameter

                Examples::

                    longname = 'Primary mass'

            range:
                Range of values to take. Does not get used really, the samplerfunc is used to
                get the values from

                Examples::

                    range = [math.log(m_min), math.log(m_max)]

            samplerfunc:
                Function returning a list or numpy array of samples spaced appropriately.
                You can either use a real function, or a string representation of a function call.

                Examples::

                    samplerfunc = "self.const_linear(math.log(m_min), math.log(m_max), {})".format(resolution['M_1'])

            precode:
                Extra room for some code. This code will be evaluated within the loop of the
                sampling function (i.e. a value for lnM_1 is chosen already)

                Examples::

                    precode = 'M_1=math.exp(lnM_1);'

            postcode:
                Code executed after the probability is calculated.

            probdist:
                Function determining the probability that gets assigned to the sampled parameter

                Examples::

                    probdist = 'self.Kroupa2001(M_1)*M_1'

            dphasevol:
                part of the parameter space that the total probability is calculated with. Put to -1
                if you want to ignore any dphasevol calculations and set the value to 1

                Examples::

                    dphasevol = 'dlnM_1'

            condition:
                condition that has to be met in order for the grid generation to continue

                Examples::

                    condition = "self.grid_options['binary']==1"

            gridtype:
                Method on how the value range is sampled. Can be either 'edge' (steps starting at
                the lower edge of the value range) or 'centred'
                (steps starting at ``lower edge + 0.5 * stepsize``).

            dry_parallel:
                If True, try to parallelize this variable in dry runs.

            topcode:
                Code added at the very top of the block.

            bottomcode:
                Code added at the very bottom of the block.
        """

        # check parameters
        # if False and dphasevol != -1.0 and gridtype == "discrete":
        if dphasevol != -1.0 and gridtype == "discrete":
            print(
                "Error making grid: you have set the phasevol to be not -1 and gridtype to discrete, but a discrete grid has no phasevol calculation. You should only set the gridtype to discrete and not set the phasevol in this case."
            )

            self.exit(code=1)

        # Add grid_variable
        grid_variable = {
            "name": name,
            "parameter_name": parameter_name,
            "longname": longname,
            "valuerange": valuerange,
            "samplerfunc": samplerfunc,
            "precode": precode,
            "postcode": postcode,
            "probdist": probdist,
            "dphasevol": dphasevol,
            "condition": condition,
            "gridtype": gridtype,
            "branchpoint": branchpoint,
            "branchcode": branchcode,
            "topcode": topcode,
            "bottomcode": bottomcode,
            "grid_variable_number": len(self.grid_options["_grid_variables"]),
            "dry_parallel": dry_parallel,
        }

        # Check for gridtype input
        allowed_gridtypes = [
            "edge",
            "right",
            "right edge",
            "left",
            "left edge",
            "centred",
            "centre",
            "center",
            "discrete",
        ]

        if gridtype not in allowed_gridtypes:
            msg = "Unknown gridtype {gridtype}. Please choose one of: ".format(
                gridtype=gridtype
            ) + ",".join(allowed_gridtypes)
            raise ValueError(msg)

        # Load it into the grid_options
        self.grid_options["_grid_variables"][grid_variable["name"]] = grid_variable

        self.verbose_print(
            "Added grid variable: {}".format(
                json.dumps(grid_variable, indent=4, ensure_ascii=False)
            ),
            self.grid_options["verbosity"],
            2,
        )
