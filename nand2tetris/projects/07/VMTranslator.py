class VMTranslator
    def __init__():
        self.lines = []
        self.outputs = []

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

                find_space = l.find(' ')
                if find_space > -1:  # strip comments
                    l = l[:find_space]
                self.lines.append(l)

    def parse_line(self):
        pass

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
