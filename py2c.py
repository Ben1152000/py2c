import dis
import marshal
import sys
import inspect


class CodeTranslator:
    c_types = ['long', 'double', 'char*', 'void*']
    py2c_type_map = {int: 'long', float: 'double', str: 'char*'}

    def __init__(self, code):
        self.opcode_map = lambda name: getattr(self, name)
        self.instruction_index = 0

        self.stack_depths = []

        self.code = code
        self.instructions = list(dis.get_instructions(self.code))

        depth = 0
        for instruction in self.instructions:
            print(instruction)
            self.stack_depths.append(depth)
            depth += dis.stack_effect(instruction.opcode, instruction.arg)

        print(self.stack_depths)

    def LOAD_CONST(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def BINARY_ADD(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def LOAD_NAME(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def STORE_NAME(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def CALL_FUNCTION(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def RETURN_VALUE(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def POP_TOP(self):
        raise Exception(f'Unimplemented opcode {inspect.stack()[0][3]}')

    def translate(self):
        output = 'void main(){'
        # create a stack for each type
        for type_option in CodeTranslator.c_types:
            output += type_option
            for i in range(max(self.stack_depths)):
                output += f's{type_option[0]}{i},'
            output[-1] = ';'

        # create local variables
        # TODO figure out the actual types of local variables
        for name in self.code.co_names:
            output += f'long {type(name)} v,'
        output[-1] = ';'

        for instruction in self.instructions:
            output += self.opcode_map(instruction.opname)()
            self.instruction_index += 1

        output += '}'
        return output


def get_code(fname):
    f = open(fname, "rb")
    f.read(16)
    code = marshal.load(f)
    return code


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} pyc_file')
        exit(1)
    code = get_code(sys.argv[1])
    print(CodeTranslator(code).translate())
