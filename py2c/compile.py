import py_compile, marshal

def compile_to_bytecode(filepath):
    pyc_file = py_compile.compile(filepath)
    readfile = open(pyc_file, 'rb')
    readfile.read(16)  # get through header bits
    bytecode = marshal.load(readfile)
    return bytecode
