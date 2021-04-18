# π2c – A Python-Bytecode to C compiler

Toba is a set of tools that increase the speed of Java programs by converting Java Bytecode to C and compiling it ahead-of-time to generate a native executable. We want to apply the same basic idea to Python, and convert .pyc files to C code. This bytecode-to-source compiler (called π2c) has the aim of improving runtime efficiency of python code. We also plan on comparing the performance of π2c to other existing python runtimes, e.g., the python interpreter, cython, etc. across a broad set of benchmarks.

Useful links:
- Python Bytecode Format: https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html#:~:text=pyc%20file%20is%20a%20binary,A%20marshalled%20code%20object.
- Python library: https://docs.python.org/3.5/library/dis.html#python-bytecode-instructions
- Java to C compiler: https://www.researchgate.net/publication/2433450_Toba_java_for_applications_a_way_ahead_of_time_WAT_compiler/citations
