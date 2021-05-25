#!/usr/bin/env python3.9

import time, os
from py2c import compile_to_bytecode
from translator import CodeTranslator

C_COMPILER = 'gcc'

BENCHMARKS = [
    'benchmarks/fibonacci',
]

def time_execution(command):
    # TODO: use better timer metric
    start = time.time()
    os.system(command)
    return time.time() - start

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


        python_runtime = time_execution(f'python3 {path}.py > /dev/null 2>&1')
        unoptimized_runtime = time_execution(f'./{path} > /dev/null 2>&1')
        optimized_runtime = time_execution(f'./{path}-O3 > /dev/null 2>&1')

        print('Python:', python_runtime, '(100%)')
        print('Unoptimized C:', unoptimized_runtime, f'({100 * unoptimized_runtime / python_runtime}%)')
        print('Optimized C:', optimized_runtime, f'({100 * optimized_runtime / python_runtime}%)')