#!/usr/bin/env python3.9

import sys, py_compile, marshal
from translator import CodeTranslator

def compile_to_bytecode(filepath):
    pyc_file = py_compile.compile(filepath)
    readfile = open(pyc_file, 'rb')
    readfile.read(16)  # get through header bits
    bytecode = marshal.load(readfile)
    return bytecode

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} pyc_file [out_file]')
        exit(1)
    
    # Use filename.c if output file is not provided
    if len(sys.argv) < 3:
        sys.argv.append('.'.join(sys.argv[1].split('.')[:-1]) + '.c')
    
    bytecode = compile_to_bytecode(sys.argv[1])
    c_source = CodeTranslator(bytecode).translate()

    with open(sys.argv[2], 'w') as writefile:
        writefile.write(c_source)
