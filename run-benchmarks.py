#!/usr/bin/env python3.9

import time
import os
from py2c.compile import compile_to_bytecode
from py2c.translator import CodeTranslator

C_COMPILER = 'gcc'
PYTHON_INTERPRETER = 'python3.9'
PYPY_INTERPRETER = 'pypy37'
isCythonInstalled = False
hasIdiomaticVersion = True

NUM_TRIES = 2  # 10

BENCHMARKS = [
    'benchmarks/fibonacci',
    'benchmarks/perfect',
    'benchmarks/prime_factor',
    'benchmarks/primes',
    'benchmarks/pythagorean',
    'benchmarks/summation',
    'benchmarks/collatz',
]


def check_installed(command):
    from shutil import which
    if which(command) == None:
        print(f'Warning: {command} does not appear to be installed.')
        return False
    return True

def time_execution(command, iterations):
    # TODO: use better timer metric
    s = 0
    for i in range(iterations):
        start = time.time()
        os.system(command)
        start = time.time() - start
        print(f'\t{i}:\t{start:.2f} seconds')
        s += start
    return s / iterations


# compile all files in test
if __name__ == '__main__':

    check_installed(C_COMPILER)
    check_installed(PYTHON_INTERPRETER)
    check_installed(PYPY_INTERPRETER)

    for path in BENCHMARKS:
        print(f'Executing {path}...')
        bytecode = compile_to_bytecode(f'{path}.py')
        translation_time = time.time()
        c_source = CodeTranslator(bytecode).translate()
        translation_time = time.time() - translation_time
        print(f'  Translation time: {translation_time * 1000:.2f} ms')
        
        with open(f'{path}.c', 'w') as writefile:
            writefile.write(c_source)

        os.system(f'{C_COMPILER} {path}.c -o {path}')
        compilation_time = time.time()
        os.system(f'{C_COMPILER} -O3 {path}.c -o {path}-O3')
        compilation_time = time.time() - compilation_time
        print(f'  Compilation time: {compilation_time * 1000:.2f} ms')

        print(f'  Python ({NUM_TRIES} trials):')
        python_runtime = time_execution(f'{PYTHON_INTERPRETER} {path}.py > /dev/null 2>&1', NUM_TRIES)
        print(f'\tavg:\t{python_runtime:.2f} seconds', '(100%)')

        print(f'  Unoptimized C ({NUM_TRIES} trials):')
        unoptimized_runtime = time_execution(f'./{path} > /dev/null 2>&1', NUM_TRIES)
        print(
            f'\tavg:\t{unoptimized_runtime:.2f} seconds',
            f'({100 * unoptimized_runtime / python_runtime:.2f}%, {python_runtime / unoptimized_runtime:.2f}x)'
        )

        print(f'  Optimized C ({NUM_TRIES} trials):')
        optimized_runtime = time_execution(f'./{path}-O3 > /dev/null 2>&1', NUM_TRIES)
        print(
            f'\tavg:\t{optimized_runtime:.2f} seconds',
            f'({100 * optimized_runtime / python_runtime:.2f}%, {python_runtime / optimized_runtime:.2f}x)'
        )

        print(f'  PyPy (JIT) ({NUM_TRIES} trials):')
        pypy_runtime = time_execution(f'{PYPY_INTERPRETER} {path}.py > /dev/null 2>&1', NUM_TRIES)
        print(
            f'\tavg:\t{pypy_runtime:.2f} seconds',
            f'({100 * pypy_runtime / python_runtime:.2f}%, {python_runtime / pypy_runtime:.2f}x)'
        )

        if isCythonInstalled:
            os.system(f'./cython_compiler.sh -o {path}-cython {path}.py -l')
            print(f'  Cython ({NUM_TRIES} trials):')
            cython_runtime = time_execution(f'./{path}-cython > /dev/null 2>&1', NUM_TRIES)
            print(
                f'\tavg:\t{cython_runtime:.2f} seconds',
                f'({100 * cython_runtime / python_runtime:.2f}%, {python_runtime / cython_runtime:.2f}x)'
            )

        if hasIdiomaticVersion:
            print(f'  Idiomatic C ({NUM_TRIES} trials):')
            idiomatic_runtime = time_execution(f'./{path}-i > /dev/null 2>&1', NUM_TRIES)
            print(
                f'\tavg:\t{idiomatic_runtime:.2f} seconds',
                f'({100 * idiomatic_runtime / python_runtime:.2f}%, {python_runtime / idiomatic_runtime:.2f}x)'
            )
