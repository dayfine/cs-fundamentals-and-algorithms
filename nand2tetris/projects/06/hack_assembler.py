from copy import copy

SYMBOL_TABLE_TEMPLATE = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
}

COMPUTATION = {
    '':    '0000000',
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

DESTINATION = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111',
}

JUMP = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


def translate_a_instr(address):
    return '{0:b}'.format(address).zfill(16)

def translate_c_instr(c_instr):
    """
    >>> translate_c_instr('MD=D+1')
    '1110011111011000'
    """
    find_eq = c_instr.find('=')
    find_semi = c_instr.find(';')

    dest = c_instr[:find_eq] if find_eq > -1 else ''
    jump = c_instr[find_semi+1:] if find_semi > -1 else ''

    if find_semi > -1:
        comp = c_instr[find_eq+1:find_semi]
    else:
        comp = c_instr[find_eq+1:]

    compb = COMPUTATION[comp]
    destb = DESTINATION[dest]
    jumpb = JUMP[jump]
    return '111{}{}{}'.format(compb, destb, jumpb)

class Assembler:
    def __init__(self):
        self.lines = []
        self.outputs = []
        self.symbol_table = copy(SYMBOL_TABLE_TEMPLATE)
        self.next_var_addr = 16

    def assemble(self, filepath):
        self.load(filepath)
        self.second_pass()
        self.write_output(filepath)

    def load(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith('//'):
                    continue

                # first pass
                if l.startswith('('):
                    label = l[1:-1]
                    self.symbol_table[label] = len(self.lines)
                    continue

                find_space = l.find(' ')
                if find_space > -1:  # strip comments
                    l = l[:find_space]
                self.lines.append(l)

    def second_pass(self):
        for line in self.lines:
            if line.startswith('@'):
                # A-instruction
                symbol = line[1:]
                if symbol.isdigit():
                    self.symbol_table[symbol] = int(symbol)
                elif symbol not in self.symbol_table:
                    self.symbol_table[symbol] = self.next_var_addr
                    self.next_var_addr += 1
                address = self.symbol_table[symbol]
                self.outputs.append(translate_a_instr(address))
            else:
                # C-instruction
                self.outputs.append(translate_c_instr(line))

    def write_output(self, input_path):
        output_path = input_path.replace('asm', 'hack')
        with open(output_path, 'w') as f:
            f.write('\n'.join(self.outputs))

if __name__ == "__main__":
    from sys import argv
    from os.path import exists, join, dirname
    script, filepath = argv

    if not exists(filepath):
        filepath = join(dirname(dirname(__file__)), filepath)
    assembler = Assembler()
    assembler.assemble(filepath)

