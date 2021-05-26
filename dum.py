# Based on code written by Ned Batchelder:
# https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html

import dis
import marshal
import struct
import sys
import time
import types


def show_file(fname):
    f = open(fname, "rb")
    magic = f.read(4)
    f.read(4)
    moddate = f.read(4)
    f.read(4)
    modtime = time.asctime(time.localtime(struct.unpack('i', moddate)[0]))
    print(f"magic {magic.hex()}")
    print(f"moddate {moddate.hex()} ({modtime})")
    print(marshal.version)
    code = marshal.load(f)
    show_code(code)


def show_code(code, indent=''):
    print(f"{indent}code")
    indent += '   '
    print(f"{indent}argcount {code.co_argcount}")
    print(f"{indent}nlocals {code.co_nlocals}")
    print(f"{indent}stacksize {code.co_stacksize}")
    print(f"{indent}flags {code.co_flags}")
    show_hex("code", code.co_code, indent=indent)
    dis.disassemble(code)
    print(f"{indent}consts")
    for const in code.co_consts:
        if type(const) == types.CodeType:
            show_code(const, indent + '   ')
        else:
            print(f"   {indent}{const} ({type(const)})")
    print(f"{indent}names {code.co_names}")
    print(f"{indent}varnames {code.co_varnames}")
    print(f"{indent}freevars {code.co_freevars}")
    print(f"{indent}cellvars {code.co_cellvars}")
    print(f"{indent}filename {code.co_filename}")
    print(f"{indent}name {code.co_name}")
    print(f"{indent}firstlineno {code.co_firstlineno}")
    show_hex("lnotab", code.co_lnotab, indent=indent)


def show_hex(label, h, indent):
    h = h.hex()
    if len(h) < 60:
        print(f"{indent}{label} {h}")
    else:
        print(f"{indent}{label}")
        for i in range(0, len(h), 60):
            print(f"{indent}   {h[i:i+60]}")


show_file(sys.argv[1])
