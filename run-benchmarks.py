#!/usr/bin/env python3.9

import time, os
from py2c import compile_to_bytecode
from translator import CodeTranslator

C_COMPILER = 'gcc'

BENCHMARKS = [
    'benchmarks/collatz',
    'benchmarks/fibonacci',
    'benchmarks/perfect',
    'benchmarks/prime_factor',
    'benchmarks/primes',
    'benchmarks/pythagorean',
    'benchmarks/summation',
]

NUM_TRIES = 2# 10

def time_execution(command, iterations):
    # TODO: use better timer metric
    s = 0
    for i in range(iterations):
        start = time.time()
        os.system(command)
        s += time.time() - start
    return s / iterations

# compile all files in test
if __name__ == '__main__':

    for path in BENCHMARKS:
        print(f'Executing {path}...')
        bytecode = compile_to_bytecode(f'{path}.py')
        c_source = CodeTranslator(bytecode).translate()
        with open(f'{path}.c', 'w') as writefile:
            writefile.write(c_source)
        
        os.system(f'{C_COMPILER} {path}.c -o {path}')
        os.system(f'{C_COMPILER} -O3 {path}.c -o {path}-O3')

        python_runtime = time_execution(f'python3 {path}.py > /dev/null 2>&1', NUM_TRIES)
        unoptimized_runtime = time_execution(f'./{path} > /dev/null 2>&1', NUM_TRIES)
        optimized_runtime = time_execution(f'./{path}-O3 > /dev/null 2>&1', NUM_TRIES)
        pypy_runtime = time_execution(f'pypy37 {path}.py > /dev/null 2>&1', NUM_TRIES)

        print('Python:', f'{python_runtime:.2f} seconds', '(100%)')
        print('Unoptimized C:', f'{unoptimized_runtime:.2f} seconds', f'({100 * unoptimized_runtime / python_runtime:.2f}%, {python_runtime / unoptimized_runtime:.2f}x)')
        print('Optimized C:', f'{optimized_runtime:.2f} seconds', f'({100 * optimized_runtime / python_runtime:.2f}%, {python_runtime / optimized_runtime:.2f}x)')
        print('PyPy (JIT):', f'{pypy_runtime:.2f} seconds', f'({100 * pypy_runtime / python_runtime:.2f}%, {python_runtime / pypy_runtime:.2f}x)')