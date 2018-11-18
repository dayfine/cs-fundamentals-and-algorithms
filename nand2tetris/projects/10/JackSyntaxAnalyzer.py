from collections import namedtuple

KEYWORDS = {
	'class',
	'constructor',
	'function',
	'method',
	'field',
	'static',
	'var',
	'int',
	'char',
	'boolean',
	'void',
	'true',
	'false',
	'null',
	'this',
	'let',
	'do',
	'if',
	'else',
	'while',
	'return',
}

SYMBOLS = {
	'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&',
	'|', '<', '>', '=', '~',
}

Token = namedtuple('Token', ['type', 'value'])

# TOKEN TYPES
T_KEYWORD = 'keyword'
T_SYMBOL = 'symbol'
T_INTEGER_CONSTANT = 'integerConstant'
T_STRING_CONSTANT = 'stringConstant'
T_IDENTIFIER = 'identifier'

class Tokenizer:
	ESCAPE_MAP = {
		'<': '&lt;',
		'>': '&gt;',
		'"': '&quot;',
		'&': '&amp;',
	}

	def __init__(self):
		self.tokens = []

	def tokenize(self, code):
		"""Tokenizer performs lexical analysis, and parse the input into five types
		of tokens: keyword, symbol, integerConstant, stringConstant, and identifier.
		"""
		idx = 0
		while idx < len(code):
			char = code[idx]
			if char in SYMBOLS:
				escaped = self.escape_token(char)
				self.tokens.append(Token(T_SYMBOL, escaped))
				idx += 1
				continue
			elif char.isspace():
				idx += 1
				continue
			elif char.isdigit():
				num = ''
				while char.isdigit():
					num += char
					idx += 1
					char = code[idx]
				self.tokens.append(Token(T_INTEGER_CONSTANT, num))
				continue
			elif char == '"':
				txt = ''
				idx += 1
				char = code[idx]
				while char != '"':
					txt += char
					idx += 1
					char = code[idx]
				self.tokens.append(Token(T_STRING_CONSTANT, txt))
				idx += 1 # skip closing quote
				continue
			else:
				idr = ''
				while not char.isspace() and char not in SYMBOLS:
					idr += char
					idx += 1
					char = code[idx]
				token_type = T_KEYWORD if idr in KEYWORDS else T_IDENTIFIER
				self.tokens.append(Token(token_type, idr))
				continue
		return self.tokens

	def escape_token(self, sym):
		escaped = self.ESCAPE_MAP.get(sym, sym)
		return escaped


class Parser:
	def __init__(self):
		pass

	def get_token(self):
		pass

	def compile_stmts(self):
		pass

	def compile_if_stmt(self):
		pass

	def compile_while_stmt(self):
		# while
		# (
		# compileExpression
		# > compileTerm
		# > OP
		# > compileTerm
		# )
		# {
		# compileStatements
		# }
		pass

	def compile_let_stmt(self):
		# LET
		# VARNAME
		# =
		# compileExpression
		# ;
		pass

	def compile_expr(self):
		pass

	def compile_term(self):
		pass


class JackSyntaxAnalyzer:
	def __init__(self, tokenizer):
		self.lines = []
		self.outputs = []

		self.tokenizer = tokenizer

	def load(self, filepath):
		self.lines = []
		self.outputs = []

		with open(filepath, 'r') as f:
			in_comment_block = False
			for line in f:
				l = line.strip()
				# skip comments
				if not l or l.startswith('//'):
					continue
				# skip multi-line comments
				if l.startswith('/*'):
					in_comment_block = True
				if in_comment_block and l.endswith('*/'):
					in_comment_block = False
					continue
				if not in_comment_block:
					self.lines.append(l)


	def analyze(self):
		tokens = self.tokenizer.tokenize(' '.join(self.lines))
		self.outputs = ["<{}> {} </{}>".format(t, v, t) for t,v in tokens]

	def write(self, output_path):
		with open(output_path, 'w') as f:
			f.write('\n'.join(self.outputs))

def SyntaxAnalyzerFactory():
	tokenizer = Tokenizer()
	return JackSyntaxAnalyzer(tokenizer)

if __name__ == '__main__':
	from sys import argv
	from os import listdir, path
	script, filepath = argv

	if not path.exists(filepath):
		filepath = path.join(path.dirname(path.dirname(__file__)), filepath)

	analyzer = SyntaxAnalyzerFactory()
	analyzer.load(filepath)
	analyzer.analyze()
	output_path = filepath.replace('jack', 'xhtml')
	analyzer.write(output_path)
