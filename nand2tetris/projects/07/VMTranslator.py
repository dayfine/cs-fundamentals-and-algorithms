# VM_COMMAND_TYPES
C_ARITHMETIC = 'command/arithmetic'
C_PUSH = 'command/push'
C_POP = 'command/pop'
C_LABEL = 'command/label'
C_GOTO = 'command/goto'
C_IF= 'command/if'
C_FUNCTION = 'command/function'
C_RETURN = 'command/return'
C_CALL= 'command/call'

# ARITHMETIC_COMMANDS
ADD = 'add'
SUB = 'sub'
NEG = 'neg'
EQ = 'eq'
GT = 'gt'
LT = 'lt'
AND = 'and'
OR = 'or'
NOT = 'not'

# STACK
STACK_BASE_ADDR = 256

# MEMORY SEGMENTS
SEG_LOCAL = 'local'
SEG_ARGUMENT = 'argument'
SEG_THIS = 'this'
SEG_THAT = 'that'
SEG_CONSTANT = 'constant'
SEG_STATIC = 'static'
SEG_POINTER = 'pointer'
SEG_TEMP = 'temp'


class VMTranslator
    def __init__():
        self.outputs = []
        self.stack_address = STACK_BASE_ADDR

    def translate(self, filepath):
        self.load(filepath)
        self.second_pass()
        self.write(filepath)


    def load(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith('//'):
                    continue

                self.parse_line(l)

    def parse_line(self, line):
        tokens = line.split(' ')

        if len(tokens) == 1:
            parse_operator_command(tokens[0])
        elif tokens[0] == 'push':
            _, segment, arg = tokens
            self.parse_push_command(arg, segment)

    def parse_push_command(self, arg=None, segment=SEG_CONSTANT):
        if arg is None:
            return

        commands = [
            '// push {} {}'.format(segment, arg),
        ]


        if segment == SEG_CONSTANT: # if pushing to the stack
            commands += [
                '@{}'.format(arg),
                'D=A',
                '@SP',  # assign data value to stack location
                'A=M',
                'M=D',
                '@SP',
                'M=M+1',  # move stack pointer
            ]

    def parse_pop_command(self, arg=None, segment=None):
        if segment is None: # if popping from the stack
            return popped

    def parse_operator_command(self, c_type):
        arg1 = self.parse_pop_command()
        arg2 = self.parse_pop_command()

        if c_type == ADD:
            self.parse_push_command(arg1 + arg2)
        elif c_type == SUB:
            self.parse_push_command(arg1 - arg2)
        elif c_type == NEG:
            self.parse_push_command(-arg1)
        elif c_type == EQ:
            self.parse_push_command(arg1 == 0)
        elif c_type == GT:
            self.parse_push_command(arg1 > arg2)
        elif c_type == LT:
            self.parse_push_command(arg1 < arg2)
        elif c_type == AND:
            self.parse_push_command(arg1 and arg2)
        elif c_type == OR:
            self.parse_push_command(arg1 or arg2)
        elif c_type == NOT:
            self.parse_push_command(not arg1)

    def write(self, input_path):
        output_path = input_path.replace('vm', 'asm')
        with open(output_path, 'w') as f:
            f.write('\n'.join(self.outputs))


if __name__ == '__main__':
    from sys import argv
    from os.path import exists, join, dirname
    script, filepath = argv

    if not exists(filepath):
        filepath = join(dirname(dirname(__file__)), filepath)

    translator = VMTranslator()
    translator.translate(filename)
