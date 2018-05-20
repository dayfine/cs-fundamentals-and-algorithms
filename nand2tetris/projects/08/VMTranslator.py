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
    STACK_BASE_ADDR = 256

    def __init__(self):
        self.lines = []
        self.outputs = []
        self.stack_address = self.STACK_BASE_ADDR
        self.unique_jump_id = 0
        self.namespace = ''
        self.current_func = ''
        self.unique_return_id = 0
        self.unique_frame_id = 0

    def load(self, filepath):
        idx = filepath.rfind('/')
        self.namespace = filepath[idx+1:-3]
        self.lines = []

        with open(filepath, 'r') as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith('//'):
                    continue
                self.lines.append(l)

    def translate(self):
        for line in self.lines:
            self.parse_line(line)
        return self.outputs

    def parse_line(self, line):
        code = line.split('// ')[0].strip()  # strip inline comments
        tokens = code.split(' ')

        if len(tokens) == 1 and tokens[0] != 'return':
            commands = self.parse_operator_command(tokens[0])
        if len(tokens) == 1 and tokens[0] == 'return':
            commands = self.parse_return_command()
        elif tokens[0] == 'push':
            _, segment, arg = tokens
            commands = self.parse_push_command(arg, segment)
        elif tokens[0] == 'pop':
            _, segment, arg = tokens
            commands = self.parse_pop_command(arg, segment)
        elif tokens[0] == 'label':
            _, label = tokens
            commands = self.parse_label_command(label)
        elif tokens[0] == 'goto':
            _, label = tokens
            commands = self.parse_goto_command(label)
        elif tokens[0] == 'if-goto':
            _, label = tokens
            commands = self.parse_if_command(label)
        elif tokens[0] == 'function':
            _, func, num_local_var = tokens
            commands = self.parse_function_command(func, num_local_var)
        elif tokens[0] == 'call':
            _, func, num_args = tokens
            commands = self.parse_call_command(func, num_args)
        self.outputs += commands

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
            commands += [
                '@{}.{}'.format(self.namespace, arg),
                'D=M',
            ]

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

        return commands

    def parse_pop_command(self, arg=None, segment=None):
        """
        e.g. pop local 2
        pop the top of the stack and put it @ local + 2
        """
        commands = [
            '// pop {} {}'.format(segment, arg),
        ]
        pop_target = None

        if segment in {SEG_LOCAL, SEG_ARGUMENT, SEG_THIS, SEG_THAT}:
            segment_label = MEMORY_SEGMENT_POINTERS[segment]
            commands += [
                '@{}'.format(segment_label),
                'D=M', # get segment base!
                '@{}'.format(arg),
                'D=D+A', # add the offset
                '@tempaddr', # store this address in tempaddr
                'M=D',
            ]
            pop_target = '@tempaddr'

        elif segment == SEG_STATIC:
            pop_target = '@{}.{}'.format(self.namespace, arg)

        elif segment == SEG_POINTER:
            if int(arg) == 0:
                pointer = MEMORY_SEGMENT_POINTERS['this']
            elif int(arg) == 1:
                pointer = MEMORY_SEGMENT_POINTERS['that']
            else:
                raise Exception('invalid argument for pop pointer command')
            pop_target = '@{}'.format(pointer)

        elif segment == SEG_TEMP:
            # the 8-place from 5 to 12
            if int(arg) >= 8:
                raise Exception('temp address is too large')
            pop_target = '@{}'.format(int(arg) + 5)

        commands += [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            pop_target,
        ]

        if segment in {SEG_LOCAL, SEG_ARGUMENT, SEG_THIS, SEG_THAT}:
            commands += ['A=M']
        commands += ['M=D']

        return commands

    def parse_operator_command(self, c_type):
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

        # parser
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
                '@SET_TRUE_{}'.format(self.unique_jump_id), # branch
                'D;{}'.format(true_jump),
                '@SET_FALSE_{}'.format(self.unique_jump_id),
                'D;{}'.format(false_jump),
                '(SET_TRUE_{})'.format(self.unique_jump_id), # set true and jump
                'D=-1',
                '@NEXT_{}'.format(self.unique_jump_id),
                'D;JMP',
                '(SET_FALSE_{})'.format(self.unique_jump_id), # set false
                'D=0',
                '(NEXT_{})'.format(self.unique_jump_id), # set it to M
                '@SP',
                'A=M',
                'M=D',
            ]
            self.unique_jump_id += 1

        commands += [
            '@SP',
            'M=M+1',  # move stack pointer back up
        ]

        return commands

    def parse_label_command(self, label):
        if self.current_func:
            label = '{}${}'.format(self.current_func, label)

        commands = [
            '// label {}'.format(label),
            '({})'.format(label),
        ]

        return commands

    def parse_goto_command(self, label):
        if self.current_func and not label.startswith(self.namespace):
            label = '{}${}'.format(self.current_func, label)

        commands = [
            '// goto {}'.format(label),
            '@{}'.format(label),
            '0;JMP',
        ]

        return commands

    def parse_if_command(self, label):
        self.outputs += [
            '// if-goto {}'.format(label),
        ]
        self.parse_pop_command(0, SEG_TEMP)

        commands = [
            '@5', # temp segment base
            'D=M',
            '@{}'.format(label),
            'D;JNE',
        ]

        return commands

    def parse_function_command(self, func, num_local_var):
        commands = [
            '// function {} {}'.format(func, num_local_var),
            '({})'.format(func),  # call command will come to this label
        ]
        # initiate all local vars as zero
        for i in range(int(num_local_var)):
            commands += self.parse_push_command(0, SEG_CONSTANT)
            commands += self.parse_pop_command(i, SEG_LOCAL)

        # point stack
        commands += [
            '@{}'.format(num_local_var),
            'D=A',
            '@SP',
            'M=M+D',
        ]

        self.current_func = func
        return commands

    def parse_call_command(self, func, num_args):
        commands = [
            '// call {} {}'.format(func, num_args),
        ]

        LCL = MEMORY_SEGMENT_POINTERS['local']
        ARG = MEMORY_SEGMENT_POINTERS['argument']
        THIS = MEMORY_SEGMENT_POINTERS['this']
        THAT = MEMORY_SEGMENT_POINTERS['that']

        retAddr = '{}$ret.{}'.format(func, self.unique_return_id)
        self.unique_return_id += 1

        PUSH_BOILERPLATE = [
            '@SP',  # assign data value to stack location
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',  # move stack pointer
        ]

        # first, push return address to stack
        commands += [
            '@{}'.format(retAddr),
            'D=A',
        ] + PUSH_BOILERPLATE

        # store current frame
        for idx, label in enumerate([LCL, ARG, THIS, THAT], 1):
            commands += [
                '@{}'.format(label),
                'D=M',
            ] + PUSH_BOILERPLATE

        # Move ARG pointer
        commands += [
            # jump beyond arguments and the above stored slots
            '@{}'.format(5 + int(num_args)),
            'D=A',
            '@SP',
            'D=M-D',
            '@{}'.format(ARG),
            'M=D',
        ]

        # Move LCL pointer
        commands += [
            '@SP',
            'D=M',
            '@{}'.format(LCL),
            'M=D',
        ]

        # transfer control to the function
        commands += self.parse_goto_command(func)

        # make return address label
        commands += [
            '({})'.format(retAddr),
        ]

        return commands

    def parse_return_command(self):
        commands = [
            '// return',
        ]

        LCL = MEMORY_SEGMENT_POINTERS['local']
        ARG = MEMORY_SEGMENT_POINTERS['argument']
        THIS = MEMORY_SEGMENT_POINTERS['this']
        THAT = MEMORY_SEGMENT_POINTERS['that']

        endFrame = '{}$endFrame.{}'.format(self.current_func, self.unique_frame_id)
        # note this is different from the return address in call command
        retAddr = '{}$retAddr.{}'.format(self.current_func, self.unique_frame_id)

        # assign top of the stack to arg0, and reset
        commands += [
            '@{}'.format(LCL),
            'D=M',
            '@{}'.format(endFrame),
            'M=D',
            '@5',
            'D=A',
            '@{}'.format(endFrame),
            'A=M-D', # go to the variable that holds return address
            'D=M', # this is the return address, save it somewhere
            '@{}'.format(retAddr),
            'M=D',
        ]

        # pop argument 0
        commands += self.parse_pop_command(0, SEG_ARGUMENT)

        commands += [
            '@{}'.format(ARG),
            'D=M',
            '@SP',
            'M=D+1', # move stack pointer
        ]

        # restore caller frame
        for idx, label in enumerate([THAT, THIS, ARG, LCL], 1):
            commands += [
                '@{}'.format(endFrame),
                'D=M',
                '@{}'.format(idx),
                'A=D-A',
                'D=M',
                '@{}'.format(label),
                'M=D',
            ]

        # goto return address
        commands += [
            '@{}'.format(retAddr),
            'A=M',
            '0;JMP',
        ]

        self.current_func = ''
        self.unique_frame_id += 1
        return commands

    def write(self, outputs, output_path):
        with open(output_path, 'w') as f:
            f.write('\n'.join(outputs))


if __name__ == '__main__':
    from sys import argv
    from os import listdir, path
    script, filepath = argv

    if not path.exists(filepath):
        filepath = path.join(path.dirname(path.dirname(__file__)), filepath)

    translator = VMTranslator()

    # compiling all vm file in the dir if a dir is passed
    if path.isdir(filepath):
        asm_codes = []
        vm_files = [path.join(filepath, file)
                    for file in listdir(filepath)
                    if file[-3:] == '.vm']

        for f in vm_files:
            translator.load(f)
            asm_codes += translator.translate()
        output_path = path.join(filepath, '{}.asm'.format(path.basename(filepath)))
        translator.write(asm_codes, output_path)
    # or just one vm file
    else:
        translator.load(filepath)
        asm_codes = translator.translate()
        output_path = filepath.replace('vm', 'asm')
        translator.write(asm_codes, output_path)
