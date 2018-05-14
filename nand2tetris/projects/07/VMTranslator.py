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

BINARY = 'binary'
UNARY = 'unary'

OPERATORS = {
    'add': { 'type': BINARY },
    'sub': { 'type': BINARY },
    'neg': { 'type': UNARY },
    'eq': { 'type': BINARY },
    'gt': { 'type': BINARY },
    'lt': { 'type': BINARY },
    'and': { 'type': BINARY },
    'or': { 'type': BINARY },
    'not': { 'type': UNARY },
}

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

MEMORY_SEGMENT_POINTERS = {
    'local': 'LCL',
    'argument': 'arg',
}


class VMTranslator:
    def __init__(self):
        self.outputs = []
        self.stack_address = STACK_BASE_ADDR
        self.unique_id = 0

    def translate(self, filepath):
        self.load(filepath)
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
            self.parse_operator_command(tokens[0])
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

        self.outputs += commands

    def parse_pop_command(self, arg=None, segment=None):
        if segment is None: # if popping from the stack
            return popped

    def parse_operator_command(self, c_type):
        commands = [
            '// {}'.format(c_type),
            '@SP',
            'M=M-1',
            'A=M', # move to the top number on stack
        ]

        op_type = OPERATORS[c_type]['type']
        if op_type == BINARY:
            commands += [
                'D=M', # take the number from top of stack
                '@SP',
                'M=M-1',
                'A=M',
            ]

        if c_type == ADD:
            commands += [
                'M=D+M', # add it to the next number on stack
            ]
        elif c_type == SUB:
            commands += [
                'M=M-D', # substract the top number from current numnber
            ]
        elif c_type == NEG:
            commands += [
                'M=-M',
            ]
        elif c_type == EQ:
            commands += [
                'D=M-D', # calc diff
                '@SET_TRUE_{}'.format(self.unique_id), # branch
                'D;JEQ',
                '@SET_FALSE_{}'.format(self.unique_id),
                'D;JNE',
                '(SET_TRUE_{})'.format(self.unique_id), # set true and jump
                'D=-1',
                '@NEXT_{}'.format(self.unique_id),
                'D;JMP',
                '(SET_FALSE_{})'.format(self.unique_id), # set false
                'D=0',
                '(NEXT_{})'.format(self.unique_id), # set it to M
                '@SP',
                'A=M',
                'M=D', # set to true
            ]
            self.unique_id += 1
        elif c_type == GT:
            commands += [
                'D=M-D', # calc diff
                '@SET_TRUE_{}'.format(self.unique_id), # branch
                'D;JGT',
                '@SET_FALSE_{}'.format(self.unique_id),
                'D;JLE',
                '(SET_TRUE_{})'.format(self.unique_id), # set true and jump
                'D=-1',
                '@NEXT_{}'.format(self.unique_id),
                'D;JMP',
                '(SET_FALSE_{})'.format(self.unique_id), # set false
                'D=0',
                '(NEXT_{})'.format(self.unique_id), # set it to M
                '@SP',
                'A=M',
                'M=D', # set to true
            ]
            self.unique_id += 1
        elif c_type == LT:
            commands += [
                'D=M-D', # calc diff
                '@SET_TRUE_{}'.format(self.unique_id), # branch
                'D;JLT',
                '@SET_FALSE_{}'.format(self.unique_id),
                'D;JGE',
                '(SET_TRUE_{})'.format(self.unique_id), # set true and jump
                'D=-1',
                '@NEXT_{}'.format(self.unique_id),
                'D;JMP',
                '(SET_FALSE_{})'.format(self.unique_id), # set false
                'D=0',
                '(NEXT_{})'.format(self.unique_id), # set it to M
                '@SP',
                'A=M',
                'M=D', # set to true
            ]
            self.unique_id += 1
        elif c_type == AND:
            commands += [
                'M=D&M',
            ]
        elif c_type == OR:
            commands += [
                'M=D|M',
            ]
        elif c_type == NOT:
            commands += [
                'M=!M',
            ]

        commands += [
            '@SP',
            'M=M+1',  # move stack pointer back up
        ]

        self.outputs += commands

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
    translator.translate(filepath)
