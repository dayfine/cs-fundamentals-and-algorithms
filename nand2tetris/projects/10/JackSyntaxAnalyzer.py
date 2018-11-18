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

KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}

SYMBOLS = {
	'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&',
	'|', '<', '>', '=', '~',
}

OPERATORS = {
	'+', '-', '=', '>', '<',
}

UNARY_OPS = {'-', '~'}

# TOKEN TYPES
T_KEYWORD = 'keyword'
T_SYMBOL = 'symbol'
T_INTEGER_CONSTANT = 'integerConstant'
T_STRING_CONSTANT = 'stringConstant'
T_IDENTIFIER = 'identifier'


Token = namedtuple('Token', ['type', 'value'])

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


# class ASTNode:
# 	def __init__(self, node_type, value, children=None):
# 		self.type = node_type
# 		self.value = value
# 		self.children = children or []
ASTNode = namedtuple('ASTNode', ['type', 'body'])


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = 0

	def get_token(self):
		token = self.tokens[self.idx]
		self.idx += 1
		return token

	def peek_token(self):
		return self.tokens[self.idx]

	def check_and_consume(self, token_type=None, value=None):
		t = self.peek_token()
		if token_type is not None:
			assert(t.type == token_type)
		if value is not None:
			assert(t.value == value)
		return self.get_token()

	def walk(self):
		token = self.peek_token()
		if token.type == T_INTEGER_CONSTANT:
			t = self.get_token()
			return ASTNode(t.type, t.value)
		elif token.tyep == T_STRING_CONSTANT:
			self.idx += 1
			return ASTNode(token.type, token.value)
		elif token.type == T_KEYWORD:
			if token.value = 'if':
				self.idx += 1
				return self.compile_if_stmt()
		else:
			pass

	def var_declaration(self):
		pass

	def compile_stmts(self):
		""" statements: statement* """
		stmts = []
		t = self.peek_token()
		while not (self.peek_token().type == T_SYMBOL && self.peek_token().value == '}'):
			stmts.append(self.compie_stmt())
		return ASTNode('statements', stmts)

	def compie_stmt(self):
		""" statement: letStatement | ifStatement | whileStatement |
				doStatement | returnStatement
		"""
		t = self.peek_token()
		assert(t.type == T_KEYWORD)
		if t.value = 'if':
			return self.compile_if_stmt()
		elif t.value = 'while':
			return self.compile_while_stmt()
		elif t.value = 'let':
			return self.compile_let_stmt()
		elif t.value = 'do':
			return self.compile_do_stmt()
		elif t.value = 'return':
			return self.compile_return_stmt()
		else:
			raise Exception('Not a statement!')

	def compile_if_stmt(self):
		""" ifStatement: 'if' '(' expression ')' '{' statements '}'
				('else' '{' statements '}')?
		"""
		body = [
			self.check_and_consume(T_KEYWORD, 'if'),
			self.check_and_consume(T_SYMBOL, '('),
			self.compile_expr(),
			self.check_and_consume(T_SYMBOL, ')'),
			self.check_and_consume(T_SYMBOL, '{'),
			self.compile_stmts(),
			self.check_and_consume(T_SYMBOL, '}'),
		]
		t = self.peek_token()
		if t.type == T_KEYWORD and t.value == 'else':
			body.extend([
				self.get_token(),
				self.check_and_consume(T_SYMBOL, '{'),
				self.compile_stmts(),
				self.check_and_consume(T_SYMBOL, '}'),
			])
		return ASTNode('ifStatement', body)

	def compile_while_stmt(self):
		""" whileStatement: 'while' '(' expression ')' '{' statements '}' """
		body = [
			self.check_and_consume(T_KEYWORD, 'while'),
			self.check_and_consume(T_SYMBOL, '('),
			self.compile_expr(),
			self.check_and_consume(T_SYMBOL, ')'),
			self.check_and_consume(T_SYMBOL, '{'),
			self.compile_stmts(),
			self.check_and_consume(T_SYMBOL, '}'),
		]
		return ASTNode('whileStatement', body)

	def compile_let_stmt(self):
		""" letStatement: 'let' varName('[' expression ']')? '=' expression ';'
		"""
		body = [
			self.check_and_consume(T_KEYWORD, 'let'),
			self.check_and_consume(T_IDENTIFIER),
		]

		t = self.peek_token()
		if t.type == T_SYMBOL and t.value == '[':
			body.extend([
				self.get_token(),
				self.compile_expr(),
				self.check_and_consume(T_SYMBOL, ']'),
			])

		body.extend([
			self.check_and_consume(T_SYMBOL, '='),
			self.compile_expr(),
			self.check_and_consume(T_SYMBOL, ';'),
		])
		return ASTNode('letStatement', body)

	def compile_do_stmt(self):
		""" doStatement: 'do' subroutineCall ';' """
		body = [
			self.check_and_consume(T_KEYWORD, 'return'),
			self.compile_subroutine_call(),
			self.check_and_consume(T_SYMBOL, ';'),
		]
		return ASTNode('doStatement', body)


	def compile_return_stmt(self):
		""" returnStatement: 'return' expression? ';' """
		body = []
		body.append(self.check_and_consume(T_KEYWORD, 'return'))
		if not (t.type == T_SYMBOL and t.value == ';'):
			body.append(self.compile_expr())
		body.append(self.check_and_consume(T_SYMBOL, ';'))
		return ASTNode('returnStatement', body)

	def compile_expr_list(self):
		""" expresionList: (expresion (',' expresion)*)? """
		pass

	def compile_expr(self):
		""" expresion: term (op term)? """
		body = []
		body.append(compile_term());
		token = self.peek_token()
		if token.value in OPERATORS:
			body.append(token)
			body.append(compile_term());
		return ASTNode('expression', token)

	def compile_term(self):
		""" term: """
		t = self.peek_token()
		# constants
		if (t.type == T_STRING_CONSTANT or
			t.type == T_INTEGER_CONSTANT or
			(t.type == T_KEYWORD and t.value in KEYWORD_CONSTANTS)):
			return ASTNode('term', [self.get_token()])
		# TODO: ... many other cases
		raise Exception('Term should be an identifier or a constant')

	def compile_subroutine_call(self):
		""" subroutineCall: """
		body = []
		return ASTNode('subroutineCall', token)


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


def main():
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


if __name__ == '__main__':
	main()
