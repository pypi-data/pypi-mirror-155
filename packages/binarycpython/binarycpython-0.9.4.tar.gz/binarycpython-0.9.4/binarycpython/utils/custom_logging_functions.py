"""
Module containing functions for the custom logging functionality.
The functions here make it possible for the user to define binaryc output logs on runtime
"""

import os
import uuid
import ctypes
import socket
import textwrap
import subprocess

from typing import Tuple, Optional

from binarycpython.utils.functions import temp_dir, remove_file, verbose_print


def autogen_C_logging_code(logging_dict: dict, verbosity: int = 0) -> Optional[str]:
    """
    Function that auto-generates PRINTF statements for binaryc.
    Input is a dictionary where the key is the header of that logging line
    and items which are lists of parameters that will be put in that logging line

    The list elements are all appended to 'stardata->' in the auto-generated code.

    Example:
        Input dictionary should look like this::

            {'MY_STELLAR_DATA':
                [
                    'model.time',
                    'star[0].mass',
                    'model.probability',
                    'model.dt'
                ]
            }

    Args:
        logging_dict: Dictionary containing lists of parameters that binary_c has to output. The keys are used by binary_c as start of the sentence.
        verbose: Level of verbosity. Defaults to zero if not set explicitly.

    Returns:
        string containing C printf statement built to output the parameters given as input.
    """

    # Check if the input is of the correct form
    if not isinstance(logging_dict, dict):
        print("Error: please use a dictionary as input")
        return None

    code = ""

    # Loop over dict keys
    for key in logging_dict:
        verbose_print(
            "Generating Print statement for custom logging code with {} as a header".format(
                key
            ),
            verbosity,
            1,
        )
        logging_dict_entry = logging_dict[key]

        # Check if item is of correct type:
        if isinstance(logging_dict_entry, list):

            # Construct print statement
            code += 'Printf("{}'.format(key)
            code += " {}".format("%g " * len(logging_dict_entry))
            code = code.strip()
            code += '\\n"'

            # Add format keys
            for param in logging_dict_entry:
                code += ",((double)stardata->{})".format(param)
            code += ");\n"

        else:
            print(
                "Error: please use a list for the list of parameters that you want to have logged"
            )
            return None
    code = code.strip()

    return code


####################################################################################
def binary_c_log_code(code: str, verbosity: int = 0) -> str:
    """
    Function to construct the code to construct the custom logging function

    Example:
        Code to log and terminate evolution when the primary star becomes a NS::

            if(stardata->star[0].stellar_type>=NS)
            {
                if (stardata->model.time < stardata->model.max_evolution_time)
                {
                    Printf("EXAMPLE_LOG_CO %30.12e %g %g %g %g %d %d\\n",
                        //
                        stardata->model.time, // 1

                        stardata->star[0].mass, //2
                        stardata->previous_stardata->star[0].mass, //3

                        stardata->star[0].radius, //4
                        stardata->previous_stardata->star[0].radius, //5

                        stardata->star[0].stellar_type, //6
                        stardata->previous_stardata->star[0].stellar_type //7
                  );
                };
                /* Kill the simulation to save time */
                stardata->model.max_evolution_time = stardata->model.time - stardata->model.dtm;
            };

    Args:
        code: Exact c-statement to output information in binary_c. Can be wrapped in logical statements.
        verbosity: Level of verbosity. Defaults to zero if not set explicitly.

    Returns:
        string containing the custom logging code. This includes all the includes and other definitions. This code will be used as the shared library
    """

    verbose_print(
        "Creating the code for the shared library for the custom logging",
        verbosity,
        1,
    )
    if not "Printf" in code:
        print(
            "Error: There has to be at least a printf statement in the provided code. Aborting"
        )
        return None

    # Create code
    custom_logging_function_string = """\
#pragma push_macro(\"Max\")
#pragma push_macro(\"Min\")
#undef Max
#undef Min
#include "binary_c.h"

// add visibility __attribute__ ((visibility ("default"))) to it 
void binary_c_API_function custom_output_function(struct stardata_t * stardata);
void binary_c_API_function custom_output_function(struct stardata_t * stardata)
{{
    // struct stardata_t * stardata = (struct stardata_t *)x;
    {};
}}

#undef Max 
#undef Min
#pragma pop_macro(\"Min\")
#pragma pop_macro(\"Max\")\
    """.format(
        code
    )

    # print(repr(textwrap.dedent(custom_logging_function_string)))
    return textwrap.dedent(custom_logging_function_string)


def binary_c_write_log_code(code: str, filename: str, verbosity: int = 0) -> None:
    """
    Function to write the generated logging code to a file

    Args:
        code: string containing the custom logging code to write to a file.
        filename: target filename.
        verbosity: Level of verbosity. Defaults to zero if not set explicitly.
    """

    # TODO: change this. I don't like the cwd
    cwd = os.getcwd()
    filePath = os.path.join(cwd, filename)

    # Remove if it exists
    remove_file(filePath, verbosity)
    verbose_print(
        "Writing the custom logging code to {}".format(filePath),
        verbosity,
        1,
    )

    # Write again
    with open(filePath, "w") as file:
        file.write(code)


def from_binary_c_config(config_file: str, flag: str) -> str:
    """
    Function to run the ``binaryc_config`` command with flags

    Args:
        config_file: ``binary_c-config`` filepath. TODO: change the name of this
        flag: flag used in the ``binary_c-config`` call.

    Returns:
        returns the result of ``<binary_c-config> <flag>``
    """

    res = subprocess.check_output(
        "{config_file} {flag}".format(config_file=config_file, flag=flag),
        shell=True,
        stderr=subprocess.STDOUT,
    )

    # convert and chop off newline
    res = res.decode("utf-8").rstrip()

    return res


def return_compilation_dict(verbosity: int = 0) -> dict:
    """
    Function to build the compile command for the shared library

    Inspired by binary_c_inline_config command in Perl

    TODO: this function still has some cleaning up to do w.r.t. default values for the compile command
    # https://developers.redhat.com/blog/2018/03/21/compiler-and-linker-flags-gcc/

    Args:
        verbosity: Level of verbosity. Defaults to zero if not set explicitly.

    Returns:
        string containing the command to build the shared library
    """

    verbose_print(
        "Calling the binary_c config code to get the info to build the shared library",
        verbosity,
        1,
    )

    # use binary_c-config to get necessary flags
    BINARY_C_DIR = os.getenv("BINARY_C")
    if BINARY_C_DIR:
        BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")
        BINARY_C_SRC_DIR = os.path.join(BINARY_C_DIR, "src")
    else:
        raise NameError("Envvar BINARY_C doesnt exist")

    #
    cc = from_binary_c_config(BINARY_C_CONFIG, "cc")

    # Check for binary_c
    BINARY_C_EXE = os.path.join(BINARY_C_DIR, "binary_c")
    if not os.path.isfile(BINARY_C_EXE):
        print("We require  binary_c executable; have you built binary_c?")
        raise NameError("BINARY_C executable doesnt exist")

    #
    libbinary_c = "-lbinary_c"
    binclibs = from_binary_c_config(BINARY_C_CONFIG, "libs")
    libdirs = "{} -L{}".format(
        from_binary_c_config(BINARY_C_CONFIG, "libdirs"), BINARY_C_SRC_DIR
    )
    bincflags = from_binary_c_config(BINARY_C_CONFIG, "cflags")
    bincincdirs = from_binary_c_config(BINARY_C_CONFIG, "incdirs")

    # combine
    # binclibs = " {} {} {}".format(libdirs, libbinary_c, binclibs)
    binclibs = " {} {} {}".format(libdirs, binclibs, libbinary_c)

    # setup defaults:
    defaults = {
        "cc": "gcc",  # default compiler
        "ccflags": bincflags,
        "ld": "ld",  # 'ld': $Config{ld}, # default linker
        "debug": 0,
        "inc": "{} -I{}".format(bincincdirs, BINARY_C_SRC_DIR),
        # inc => ' '.($Config{inc}//' ').' '.$bincincdirs." -I$srcdir ",
        #   include the defaults plus # GSL and binary_c
        # 'libname': libname, # libname is usually just binary_c corresponding to libbinary_c.so
        "libs": binclibs,
    }

    # set values with defaults. TODO: make other input possile.
    ld = defaults["ld"]
    # debug = defaults["debug"]
    inc = defaults[
        "inc"
    ]  # = ($ENV{BINARY_GRID2_INC} // $defaults{inc}).' '.($ENV{BINARY_GRID2_EXTRAINC} // '');
    libs = defaults[
        "libs"
    ]  # = ($ENV{BINARY_GRID2_LIBS} // $defaults{libs}).' '.($ENV{BINARY_GRID2_EXTRALIBS}//'');
    ccflags = defaults["ccflags"]  #  = $ENV{BINARY_GRID2_CCFLAGS}
    # // ($defaults{ccflags}) . ($ENV{BINARY_GRID2_EXTRACCFLAGS} // '');

    # you must define _SEARCH_H to prevent it being loaded twice
    ccflags += " -shared -D_SEARCH_H"

    # remove the visibility=hidden for this compilation
    ccflags = ccflags.replace("-fvisibility=hidden", "")

    # ensure library paths to the front of the libs:
    libs_content = libs.split(" ")
    library_paths = [el for el in libs_content if el.startswith("-L")]
    non_library_paths = [
        el for el in libs_content if (not el.startswith("-L") and not el == "")
    ]
    libs = "{} {}".format(" ".join(library_paths), " ".join(non_library_paths))

    #
    verbose_print(
        "Got options to compile:\n\tcc = {cc}\n\tccflags = {ccflags}\n\tld = {ld}\n\tlibs = {libs}\n\tinc = {inc}\n\n".format(
            cc=cc, ccflags=ccflags, ld=ld, libs=libs, inc=inc
        ),
        verbosity,
        1,
    )

    return {"cc": cc, "ld": ld, "ccflags": ccflags, "libs": libs, "inc": inc}


def compile_shared_lib(
    code: str, sourcefile_name: str, outfile_name: str, verbosity: int = 0
) -> None:
    """
    Function to write the custom logging code to a file and then compile it.

    TODO: consider returning a status

    Args:
        code: string containing the custom logging code
        sourcefile_name: name of the file that will contain the code
        outfile_name: name of the file that will be the shared library
        verbosity: Level of verbosity. Defaults to zero if not set explicitly.
    """

    # Write code to file
    binary_c_write_log_code(code, sourcefile_name, verbosity)

    # Remove the library if present:
    remove_file(outfile_name, verbosity)

    # create compilation command
    compilation_dict = return_compilation_dict(verbosity)

    # Construct full command
    command = (
        "{cc} -fPIC {ccflags} {libs} -o {outfile_name} {sourcefile_name} {inc}".format(
            cc=compilation_dict["cc"],
            ccflags=compilation_dict["ccflags"],
            libs=compilation_dict["libs"],
            outfile_name=outfile_name,
            sourcefile_name=sourcefile_name,
            inc=compilation_dict["inc"],
        )
    )

    # remove extra white spaces:
    command = " ".join(command.split())

    # Execute compilation and create the library
    verbose_print(
        "Building shared library for custom logging with (binary_c.h) on {}\n".format(
            socket.gethostname()
        ),
        verbosity,
        1,
    )
    verbose_print(
        "Executing following command to compile the shared library:\n{command}".format(
            command=command
        ),
        verbosity,
        1,
    )

    #
    res = subprocess.check_output("{command}".format(command=command), shell=True)
    if res:
        verbose_print(
            "Output of compilation command:\n{}".format(res),
            verbosity,
            1,
        )


def create_and_load_logging_function(
    custom_logging_code: str, verbosity: int = 0, custom_tmp_dir=None
) -> Tuple[int, str]:
    """
    Function to automatically compile the shared library with the given
    custom logging code and load it with ctypes.

    This function is more or less the main function of this module and unless you know what you're doing with the other functions
    I recommend using this in function in combination with a function that generates the exact code (like :meth:`~binarycpython.utils.custom_logging_code.binary_c_log_code`)

    Args:
        custom_logging_code: string containing the custom logging code
        verbosity: Level of verbosity. Defaults to zero if not set explicitly.

    Returns:
        memory address of the custom logging function in a capsule.
    """
    #

    if not custom_tmp_dir:
        tmp_dir = temp_dir()
    else:
        tmp_dir = custom_tmp_dir

    custom_logging_dir = os.path.join(tmp_dir, "custom_logging")

    # Create the sub dir for the custom_logging code
    os.makedirs(custom_logging_dir, exist_ok=True)

    #
    library_name = os.path.join(
        custom_logging_dir, "libcustom_logging_{}.so".format(uuid.uuid4().hex)
    )

    compile_shared_lib(
        custom_logging_code,
        sourcefile_name=os.path.join(custom_logging_dir, "custom_logging.c"),
        outfile_name=library_name,
        verbosity=verbosity,
    )

    verbose_print(
        "loading shared library for custom logging",
        verbosity,
        1,
    )

    # Loading library
    _ = ctypes.CDLL("libgslcblas.so", mode=ctypes.RTLD_GLOBAL)
    _ = ctypes.CDLL("libgsl.so", mode=ctypes.RTLD_GLOBAL)
    _ = ctypes.CDLL("libbinary_c.so", mode=ctypes.RTLD_GLOBAL)

    libcustom_logging = ctypes.CDLL(
        library_name,
        mode=ctypes.RTLD_GLOBAL,
    )  # loads the shared library

    # Get memory adress of function. mimicking a pointer
    func_memaddr = ctypes.cast(
        libcustom_logging.custom_output_function, ctypes.c_void_p
    ).value

    if not isinstance(func_memaddr, int):
        print(
            "Something went wrong. The memory adress returned by the ctypes.cast is not an integer. It has the value {}".format(
                func_memaddr
            )
        )
        raise ValueError

    verbose_print(
        "loaded shared library for custom logging. \
        custom_output_function is loaded in memory at {}".format(
            func_memaddr
        ),
        verbosity,
        1,
    )

    return func_memaddr, library_name
