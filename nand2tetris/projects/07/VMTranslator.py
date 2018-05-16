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
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT',
}


class VMTranslator:
    def __init__(self):
        self.outputs = []
        self.stack_address = STACK_BASE_ADDR
        self.unique_id = 0
        self.namespace = ''

    def translate(self, filepath):
        self.load(filepath)
        self.write(filepath)

    def load(self, filepath):
        self.namespace = filepath[:-3]

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
        elif tokens[0] == 'pop':
            _, segment, arg = tokens
            self.parse_pop_command(arg, segment)

    def parse_push_command(self, arg=None, segment=SEG_CONSTANT):
        if arg is None:
            return

        commands = [
            '// push {} {}'.format(segment, arg),
        ]

        if segment == SEG_CONSTANT: # if pushing to the stack
            commands += [
                '@{}'.format(arg),
                'D=A', # get constant value
            ]

        elif segment in {SEG_LOCAL, SEG_ARGUMENT, SEG_THIS, SEG_THAT}:
            segment_label = MEMORY_SEGMENT_POINTERS[segment]
            commands += [
                '@{}'.format(segment_label),
                'D=M', # get segment base!
                '@{}'.format(arg),
                'A=D+A', # add the offset
                'D=M', # get value from memory location
            ]

        elif segment == SEG_STATIC:
            ref = '{}.{}'.format(self.namespace, arg)
            pass

        elif segment == SEG_POINTER:
            if int(arg) == 0:
                pointer = MEMORY_SEGMENT_POINTERS['this']
            elif int(arg) == 1:
                pointer = MEMORY_SEGMENT_POINTERS['that']
            else:
                raise Exception('invalid argument for pop pointer command')

            commands += [
                '@{}'.format(pointer),
                'D=M',
            ]

        elif segment == SEG_TEMP:
            if int(arg) >= 8:
                raise Exception('temp address is too large')

            commands += [
                # the 8-place from 5 to 12
                '@{}'.format(int(arg) + 5),
                'D=M',
            ]

        commands += [
            '@SP',  # assign data value to stack location
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',  # move stack pointer
        ]

        self.outputs += commands

    def parse_pop_command(self, arg=None, segment=None):
        """
        e.g. pop local 2
        pop the top of the stack and put it @ local + 2
        """
        commands = [
            '// pop {} {}'.format(segment, arg),
        ]

        if segment in {SEG_LOCAL, SEG_ARGUMENT, SEG_THIS, SEG_THAT}:
            segment_label = MEMORY_SEGMENT_POINTERS[segment]
            commands += [
                '@{}'.format(segment_label),
                'D=M', # get segment base!
                '@{}'.format(arg),
                'D=D+A', # add the offset
                '@tempaddr', # store this address in tempaddr
                'M=D',
                '@SP',
                'M=M-1',
                'A=M', # move to the top number on stack
                'D=M', # take the number from top of stack
                '@tempaddr', # now jump to target address
                'A=M',
                'M=D',
            ]

        elif segment == SEG_STATIC:
            ref = '{}.{}'.format(self.namespace, arg)
            pass

        elif segment == SEG_POINTER:
            if int(arg) == 0:
                pointer = MEMORY_SEGMENT_POINTERS['this']
            elif int(arg) == 1:
                pointer = MEMORY_SEGMENT_POINTERS['that']
            else:
                raise Exception('invalid argument for pop pointer command')

            commands += [
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                '@{}'.format(pointer),
                'M=D',
            ]

        elif segment == SEG_TEMP:
            if int(arg) >= 8:
                raise Exception('temp address is too large')

            commands += [
                '@SP',
                'M=M-1',
                'A=M',
                'D=M',
                # the 8-place from 5 to 12
                '@{}'.format(int(arg) + 5),
                'M=D',
            ]

        self.outputs += commands

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
        elif c_type in {EQ, GT, LT}:
            if c_type == EQ:
                true_jump, false_jump = 'JEQ', 'JNE'
            elif c_type == GT:
                true_jump, false_jump = 'JGT', 'JLE'
            elif c_type == LT:
                true_jump, false_jump = 'JLT', 'JGE'

            # TODO: come back to fix this piece of mess
            commands += [
                'D=M-D', # calc diff
                '@SET_TRUE_{}'.format(self.unique_id), # branch
                'D;{}'.format(true_jump),
                '@SET_FALSE_{}'.format(self.unique_id),
                'D;{}'.format(false_jump),
                '(SET_TRUE_{})'.format(self.unique_id), # set true and jump
                'D=-1',
                '@NEXT_{}'.format(self.unique_id),
                'D;JMP',
                '(SET_FALSE_{})'.format(self.unique_id), # set false
                'D=0',
                '(NEXT_{})'.format(self.unique_id), # set it to M
                '@SP',
                'A=M',
                'M=D',
            ]
            self.unique_id += 1

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
