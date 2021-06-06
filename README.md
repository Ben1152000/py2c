# π2c – A Python-Bytecode to C compiler

## Project Overview:

Toba is a set of tools that increase the speed of Java programs by converting Java Bytecode to C and compiling it ahead-of-time to generate a native executable. We want to apply the same basic idea to Python, and convert .pyc files to C code. This bytecode-to-source compiler (called π2c) has the aim of improving runtime efficiency of python code. We also plan on comparing the performance of π2c to other existing python runtimes, e.g., the python interpreter, cython, etc. across a broad set of benchmarks.

## Instructions for use:

To convert a python3.9 file to c source code, run

    ./py2c.py python_file [out_file]

For example, running

    ./py2c.py test/fibonacci.py test/fibonacci.c

will compile the fibonacci program into a .pyc bytecode file, and convert it to a c program. Then, running

    gcc -O3 test/fibonacci.c -o test/fibonacci

will compile and optimize the c program, creating an executable binary in the desired location.

## Examples:

A set of example programs can be found in the `test/` directory, and a set of benchmarks can be found in the `benchmarks/` directory. Note that the examples `test/complicated.py` and `test/dynamic_typing.py` do not work, since they highlight features that have not been implemented in py2c.

## Benchmarks:

The `run-benchmarks.py` program exists to automatically test the runtime of the py2c translation against various other runtime systems. Currently, it tests the program when run with py2c (with and without optimizations), CPython (python interpreter), PyPy (python JIT compiler), cython (c/python interface), and idiomatic (manual) c translation. The runtimes and relative speedups are printed for each program 


To run the benchmarks you may want to install Cython via `pip install Cython`
Please also install PyPy 3.5 or higher using your system's package manager.

## Useful links:
- Python Bytecode Format: https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html#:~:text=pyc%20file%20is%20a%20binary,A%20marshalled%20code%20object.
- Python library: https://docs.python.org/3.9/library/dis.html#python-bytecode-instructions
- Java to C compiler: https://www.researchgate.net/publication/2433450_Toba_java_for_applications_a_way_ahead_of_time_WAT_compiler/citations
- Cool diagram of pyc files: https://formats.kaitai.io/python_pyc_27/python_pyc_27.svg
Ideas for benchmarks:
- https://capra.cs.cornell.edu/bril/tools/bench.html
