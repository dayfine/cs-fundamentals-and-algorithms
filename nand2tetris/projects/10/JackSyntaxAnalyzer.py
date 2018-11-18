from collections import namedtuple, defaultdict

# KEYWORD CONSTANTS
K_CLASS = 'class'
K_CONSTRUCTOR = 'constructor'
K_FUNCTION = 'function'
K_METHOD = 'method'
K_FIELD	= 'field'
K_STATIC	= 'static'
K_VAR	= 'var'
K_INT	= 'int'
K_CHAR	= 'char'
K_BOOLEAN	= 'boolean'
K_VOID	= 'void'
K_TRUE	= 'true'
K_FALSE	= 'false'
K_NULL	= 'null'
K_THIS	= 'this'
K_LET	= 'let'
K_DO	= 'do'
K_IF	= 'if'
K_ELSE	= 'else'
K_WHILE	= 'while'
K_RETURN  = 'return'

KEYWORDS = {
	K_CLASS, K_CONSTRUCTOR, K_FUNCTION, K_METHOD, K_FIELD, K_STATIC, K_VAR,
	K_INT, K_CHAR, K_BOOLEAN, K_VOID, K_TRUE, K_FALSE, K_NULL, K_THIS, K_LET,
	K_DO, K_IF, K_ELSE, K_WHILE, K_RETURN,
}

KEYWORD_CONSTANTS = {K_TRUE, K_FALSE, K_NULL, K_THIS}
BUILT_IN_TYPES = {K_INT, K_CHAR, K_BOOLEAN}
CLASS_VAR_KEYWORDS = {K_FIELD, K_STATIC}
SUBROUTINE_KEYWORDS = {K_CONSTRUCTOR, K_FUNCTION, K_METHOD}

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


ASTNode = namedtuple('ASTNode', ['type', 'body'])


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = 0
		self.classNames = {}
		self.varNamesByClass = {}
		self.subroutineNamesByClass = {}

	def get_token(self):
		token = self.tokens[self.idx]
		self.idx += 1
		return token

	def peek_token(self):
		return self.tokens[self.idx]

	def assert_and_consume(self, token_type=None, value=None):
		t = self.peek_token()
		if token_type is not None:
			assert(t.type == token_type)
		if value is not None:
			assert(t.value == value)
		return self.get_token()

	def check_symbol(self, value):
		t = self.peek_token()
		return t.type == T_SYMBOL and t.value == value

	def check_keyword(self, value):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value == value

	def walk(self):
		self.parse_class()

	def parse_class(self):
		""" class: 'class' className '{' classVarDec* subroutineDec* '}' """
		body = [
			self.assert_and_consume(T_KEYWORD, K_CLASS),
			self.assert_and_consume(T_IDENTIFIER),
			self.assert_and_consume(T_SYMBOL, '{'),
		]
		while self._next_is_class_var_decl():
			body.append(self.parse_class_var_decl())
		while self._next_is_subroutine_decl():
			body.append(self.parse_subroutine_decl())
		body.append(self.assert_and_consume(T_SYMBOL, '}'))
		return ASTNode('class', body)

	def parse_class_var_decl(self):
		""" classVarDec: ('static'|'field') type varName (',' varName)* ';' """
		body = [
			self.get_token(),
			self.parse_type(),
			self.assert_and_consume(T_IDENTIFIER),
		]
		while (self.check_symbol(',')):
			body.extend([
				self.get_token(),
				self.assert_and_consume(T_IDENTIFIER)
			])
		self.assert_and_consume(T_SYMBOL, ';'),
		return ASTNode('classVarDec', body)

	def _next_is_class_var_decl(self):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value in CLASS_VAR_KEYWORDS

	def parse_type(self):
		""" type: 'int' | 'char' | 'boolean' | className """
		if self._next_is_type():
			return self.get_token()
		raise TypeError('Not a type!')

	def _next_is_type(self):
		t = self.peek_token()
		return (t.type == T_KEYWORD and t.value in BUILT_IN_TYPES)
			or t.type == T_IDENTIFIER

	def parse_subroutine_decl(self):
		""" subroutineDec: ('constructor'|'function'|'method') ('void'|type)
				subroutineName '(' paramaterList ')' subroutineBody
		"""
		body = [
			self.get_token()
		]
		if self.check_keyword(K_VOID):
			body.append(self.get_token())
		else:
			body.append(self.parse_type())
		body.extend([
			self.assert_and_consume(T_IDENTIFIER),
			self.assert_and_consume(T_SYMBOL, '('),
			self.parse_parameter_list(),
			self.assert_and_consume(T_SYMBOL, ')'),
			self.parse_subroutine_body(),
		])
		return ASTNode('subroutineDec', body)

	def _next_is_subroutine_decl(self):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value in SUBROUTINE_KEYWORDS

	def parse_parameter_list(self):
		""" paramaterList: ((type varName) (',' type varName)*)? """
		body = []
		while self._next_is_type():
			body.extend([
				self.get_token(),
				self.assert_and_consume(T_IDENTIFIER),
			])
			if self.check_symbol(','):
				self.get_token()
			else:
				break
		return ASTNode('paramaterList', body)

	def parse_subroutine_body(self):
		""" subroutineBody: '{' varDec* statements '}' """
		body = [self.assert_and_consume(T_SYMBOL, '{')]
		while self._next_is_var_decl():
			body.append(self.parse_var_decl())
		body.append(self.parse_stmts())
		body.append(self.assert_and_consume(T_SYMBOL, '}'))
		return ASTNode('subroutineBody', body)

	def parse_var_decl(self):
		""" varDec: 'var' type varName (',' varName)* ';' """
		body = [
			self.assert_and_consume(T_KEYWORD, K_VAR),
			self.parse_type(),
			self.assert_and_consume(T_IDENTIFIER),
		]
		while (self.check_symbol(',')):
			body.extend([
				self.get_token(),
				self.assert_and_consume(T_IDENTIFIER)
			])
		self.assert_and_consume(T_SYMBOL, ';'),
		return ASTNode('varDec', body)

	def _next_is_var_decl(self):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value == K_VAR

	def parse_stmts(self):
		""" statements: statement* """
		stmts = []
		while not (self.check_symbol('}')):
			stmts.append(self.compie_stmt())
		return ASTNode('statements', stmts)

	def parse_stmt(self):
		""" statement: letStatement | ifStatement | whileStatement |
				doStatement | returnStatement
		"""
		t = self.peek_token()
		assert(t.type == T_KEYWORD)
		if t.value = K_IF:
			return self.parse_if_stmt()
		elif t.value = K_WHILE:
			return self.parse_while_stmt()
		elif t.value = K_LET:
			return self.parse_let_stmt()
		elif t.value = K_DO:
			return self.parse_do_stmt()
		elif t.value = K_RETURN:
			return self.parse_return_stmt()
		else:
			raise Exception('Not a statement!')

	def parse_if_stmt(self):
		""" ifStatement: 'if' '(' expression ')' '{' statements '}'
				('else' '{' statements '}')?
		"""
		body = [
			self.assert_and_consume(T_KEYWORD, K_IF),
			self.assert_and_consume(T_SYMBOL, '('),
			self.parse_expr(),
			self.assert_and_consume(T_SYMBOL, ')'),
			self.assert_and_consume(T_SYMBOL, '{'),
			self.parse_stmts(),
			self.assert_and_consume(T_SYMBOL, '}'),
		]
		if self.check_keyword(K_ELSE):
			body.extend([
				self.get_token(),
				self.assert_and_consume(T_SYMBOL, '{'),
				self.parse_stmts(),
				self.assert_and_consume(T_SYMBOL, '}'),
			])
		return ASTNode('ifStatement', body)

	def parse_while_stmt(self):
		""" whileStatement: 'while' '(' expression ')' '{' statements '}' """
		body = [
			self.assert_and_consume(T_KEYWORD, K_WHILE),
			self.assert_and_consume(T_SYMBOL, '('),
			self.parse_expr(),
			self.assert_and_consume(T_SYMBOL, ')'),
			self.assert_and_consume(T_SYMBOL, '{'),
			self.parse_stmts(),
			self.assert_and_consume(T_SYMBOL, '}'),
		]
		return ASTNode('whileStatement', body)

	def parse_let_stmt(self):
		""" letStatement: 'let' varName('[' expression ']')? '=' expression ';'
		"""
		body = [
			self.assert_and_consume(T_KEYWORD, 'let'),
			self.assert_and_consume(T_IDENTIFIER),
		]
		if self.check_symbol('['):
			body.extend([
				self.get_token(),
				self.parse_expr(),
				self.assert_and_consume(T_SYMBOL, ']'),
			])
		body.extend([
			self.assert_and_consume(T_SYMBOL, '='),
			self.parse_expr(),
			self.assert_and_consume(T_SYMBOL, ';'),
		])
		return ASTNode('letStatement', body)

	def parse_do_stmt(self):
		""" doStatement: 'do' subroutineCall ';' """
		body = [
			self.assert_and_consume(T_KEYWORD, K_DO),
			self.parse_subroutine_call(),
			self.assert_and_consume(T_SYMBOL, ';'),
		]
		return ASTNode('doStatement', body)

	def parse_return_stmt(self):
		""" returnStatement: 'return' expression? ';' """
		body = []
		body.append(self.assert_and_consume(T_KEYWORD, K_RETURN))
		if not (self.check_symbol(';')):
			body.append(self.parse_expr())
		body.append(self.assert_and_consume(T_SYMBOL, ';'))
		return ASTNode('returnStatement', body)

	def parse_expr_list(self):
		""" expresionList: (expresion (',' expresion)*)? """
		body = []
		# try catch here?
		pass

	def parse_expr(self):
		""" expresion: term (op term)? """
		# might need a try catch based on term
		body = [self.parse_term()]
		token = self.peek_token()
		if token.value in OPERATORS:
			body.append(token)
			body.append(parse_term());
		return ASTNode('expression', token)

	def parse_term(self):
		""" term: integerConstant | stringConstant | keywordConstant | varName |
				varName'[' expression ']' | subroutineCall | '(' expression ')'
				| unaryOp term
		"""
		t = self.peek_token()
		# constants
		if (t.type == T_STRING_CONSTANT or
			t.type == T_INTEGER_CONSTANT or
			(t.type == T_KEYWORD and t.value in KEYWORD_CONSTANTS)):
			return ASTNode('term', [self.get_token()])
		elif
		# TODO: ... many other cases
		raise Exception('Not a term')

	def parse_subroutine_call(self):
		""" subroutineCall: subroutineName '(' expressionList ')' |
				( className | varName )'.' subroutineName '(' expressionList ')'
		"""
		body = []
		return ASTNode('subroutineCall', token)


class JackSyntaxAnalyzer:
	def __init__(self, tokenizer, parser):
		self.lines = []
		self.outputs = []
		self.tokenizer = tokenizer
		self.parser = parser

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
	parser = Parser()
	return JackSyntaxAnalyzer(tokenizer, parser)


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
