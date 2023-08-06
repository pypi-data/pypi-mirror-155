# Python module for binary_c
Docstring coverage: 
![docstring coverage](./badges/docstring_coverage.svg)
Test coverage: 
![test coverage](./badges/test_coverage.svg)

Powered by:
![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)

We present our package [binary-c-python](https://ri0005.pages.surrey.ac.uk/binary_c-python/), a population synthesis code which is aimed to provide a convenient and easy-to-use interface to the [binary_c](http://personal.ph.surrey.ac.uk/~ri0005/doc/binary_c/binary_c.html) framework, allowing the user to rapidly evolve single stellar systems and populations of star systems. Based on a early work by Jeff Andrews. Updated and extended for Python3 by David Hendriks, Robert Izzard.

binary_c-python is developed for students and scientists in the field of stellar astrophysics, who want to study the evolution of individual or populations of single and binary star systems (see the example use-case notebooks in the [online documentation](https://ri0005.pages.surrey.ac.uk/binary_c-python/example_notebooks.html).

The current release is version [version](VERSION), and is designed and tested to work with binary_c version 2.2.1 (for older or newer versions we can't guarantee correct behaviour). 

## Installation
To install binary_c-python we need to make sure we meet the requirements of installation, and 

### Python requirements
To run this code you need to at least have installations of:

- Python 3.7 or higher (3.6 is EOL, and we are using 3.9 for development)
- binary_c version 2.2.0 or higher

The packages that are required for this code to run are listed in the requirements.txt, which automatically gets read out by setup.py

### Environment variables
Before compilation you need to have certain environment variables:

Required:

- `BINARY_C` should point to the root directory of your binary_c installation
- `LD_LIBRARY_PATH` should include $BINARY_C/src and whatever directories are required to run binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `LIBRARY_PATH` should include whatever directories are required to build binary_c (e.g. locations of libgsl, libmemoize, librinterpolate, etc.)
- `GSL_DIR` should point to the root location where you installed GSL to. This root dir should contain `bin/`, `lib/` etc

### Build instructions
First, make sure you have built binary_c (See `$BINARY_C/doc/binary_c2.pdf` section: installation for all the installation instructions for `binary_c`)) and that it functions correctly.

### Installation via PIP:
To install this package via pip:

```
pip install binarycpython
```

This will install the latest stable installation that is available on Pip. The version on the master branch should be the same version as the latest stable version on Pip

### Installation from source:
We can also install the package from source, which is useful for development versions and when you want to modify the code. It is recommended that you install this into a virtual environment. From within the `commands/` directory, run 

```
./install.sh
```

This will install the package, along with all the dependencies, into the current active (virtual) python environment.

#### After installation from source
After installing the code via source it is useful to run the test suite before doing any programming with it. The test suite is stored in `binarycpython/tests` and running `python main.py` in there will run all the tests. 

### Use of code without installation
Because installing `binary_c-python` requires a working installation of `binary_c`, installing via pip or from source without this working installation of `binary_c` won't work. To still make use of some of the functions provided by `binary_c-python`, you can add the path to the code-base to your `PYTHONPATH`:
- Download `binary_c-python`, via e.g. `git clone https://gitlab.com/binary_c/binary_c-python.git` 
- Add the path to the downloaded repo to your `$PYTHONPATH`, via e.g. `export PYTHONPATH="~/binary_c-python:$PYTHONPATH"`

## Usage
### Examples
See the examples/ directory for example scripts and notebooks. The documentation contains example pages as well. 

### Usage notes
Make sure that with every change/recompilation you make in `binary_c`, you also rebuild this package. Whenever you change the sourcecode of this package, you need to reinstall it into your virtualenvironment as well

### Documentation
Look in the docs/ directory. Within the build/html/ there is the html version of the documentation. The documentation is also hosted on http://personal.ph.surrey.ac.uk/~ri0005/doc/binary_c/binary_c.html but only for the most recent stable release.

## Development:
If you want to contribute to the code, then it is recommended that you install the packages in `development_requirements.txt`:

```
pip install -r development_requirements.txt
```

Please do not hesitate to contact us to discuss any developments. 

### Generating documentation
To build the documentation manually, run

```
./generate_docs.sh
```

from within the `commands/` directory

### Generating docstring and test coverage report 
To generate the unit test and docstring coverage report, run

```
./generate_reports.sh
```

from within the `commands/` directory

### Running unit tests
There are two versions of the general unit tests. The first includes only the actual code of the project, and is located at `binarycpython/test/main.py`. The second includes the tutorial notebooks, and is located at `binarycpython/test/main_with_notebooks.py`. To run just the notebook tests run `python binarycpython/tests/test_notebooks.py`

## FAQ/Issues:
Here we provide a non-exhaustive list of some issues we encountered and solutions for these: 

Building issues with binary_c itself: 
- see the documentation of binary_c (in doc/). 
- If you have MESA installed, make sure that the `$MESASDK_ROOT/bin/mesasdk_init.sh` is not sourced. It comes with its own version of some programs, and those can interfere with installing.  

When Pip install fails:
- Run the installation with `-v` and/or `--log <logfile>` to get some more info
- If gcc throws errors like `gcc: error: unrecognized command line option ‘-ftz’; did you mean ‘-flto’?`, this might be due to that the python on that system was built with a different compiler. It then passes the python3.6-config --cflags to the binarycpython installation, which, if done with gcc, will not work. Try a different python3.6. I suggest using `pyenv` to manage python versions. If installing a version of python with pyenv is not possible, then try to use a python version that is avaible to the machine that is built with the same compiler as binary_c was built with. 
- if pip installation results in `No files/directories in /tmp/pip-1ckzg0p9-build/pip-egg-info (from PKG-INFO)`, try running it verbose (`-v`) to see what is actually going wrong. 
- If pip terminates with the error FileNotFoundError: [Errno 2] No such file or directory: '<...>/binary_c-config' Then make sure that the path to your main $BINARY_C directory is set correctly.

Other:
- When running jupyter notebooks, make sure you are running the jupyter installation from the same virtual environment. 
- When the output of binary_c seems to be different than expected, you might need to rebuild this python package. Everytime binary_c is compiled, this package needs to be rebuilt too.
