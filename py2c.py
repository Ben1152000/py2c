#!/usr/bin/env python3.9

if __name__ == '__main__':

    import sys, py_compile, marshal
    from py2c.translator import CodeTranslator
    from py2c.compile import compile_to_bytecode

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
