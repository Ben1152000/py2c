# π2c – A Python-Bytecode to C compiler

## Project Overview:

Toba is a set of tools that increase the speed of Java programs by converting Java Bytecode to C and compiling it ahead-of-time to generate a native executable. We want to apply the same basic idea to Python, and convert .pyc files to C code. This bytecode-to-source compiler (called π2c) has the aim of improving runtime efficiency of python code. We also plan on comparing the performance of π2c to other existing python runtimes, e.g., the python interpreter, cython, etc. across a broad set of benchmarks.

## Instructions for use:

To convert a python3 file to c source code, run

    ./py2c.py python_file [out_file]

For example, running

    ./py2c.py test/fibonacci.py test/fibonacci.c

will compile the fibonacci program into a .pyc bytecode file, and convert it to a c program. Then, running

    gcc -O3 test/fibonacci.c -o test/fibonacci

will compile and optimize the c program, creating an executable binary in the desired location.

Note: In order for py2c to work, all functions and variables need to be statically typed. Type annotations (introduced in v3.5) are required for functions. Supported types include `int`, `float`, and `bool`.

### Examples:

A set of example programs can be found in the `test/` directory, and a set of benchmarks can be found in the `benchmarks/` directory. Note that the examples `test/complicated.py` and `test/dynamic_typing.py` do not work, since they highlight features that have not been implemented in py2c.

These examples can be run manually using the instructions in the section above.

### Benchmarks:

The `run-benchmarks.py` program exists to automatically test the runtime of the py2c translation against various other runtime systems. Currently, it tests the program when run with py2c (with and without optimizations), CPython (python interpreter), PyPy (python JIT compiler), cython (c/python interface), and idiomatic (manual) c translation. The runtimes and relative speedups are printed for each program and runtime.

To run all of the benchmarks at once, run

    python3 run-benchmarks.py

Before you run the above command, it may be necessary to install the following programs:
- Cython (`pip3 install cython`)
- PyPy (version >= 3.5)

*Important: At the top of the `run-benchmarks.py` file, change the user-defined constants to contain the proper values for your environment. If cython is installed, set the value of `isCythonInstalled` to `True`*

## References

### Useful Links:

- Python Bytecode Format: https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html#:~:text=pyc%20file%20is%20a%20binary,A%20marshalled%20code%20object.

- Python library: https://docs.python.org/3.9/library/dis.html#python-bytecode-instructions

- Java to C compiler: https://www.researchgate.net/publication/2433450_Toba_java_for_applications_a_way_ahead_of_time_WAT_compiler/citations

- Cool diagram of pyc files: https://formats.kaitai.io/python_pyc_27/python_pyc_27.svg

- Ideas for benchmarks: https://capra.cs.cornell.edu/bril/tools/bench.html
