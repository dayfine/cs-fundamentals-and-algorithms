from collections import namedtuple, defaultdict

# KEYWORD CONSTANTS
K_CLASS = 'class'
K_CONSTRUCTOR = 'constructor'
K_FUNCTION = 'function'
K_METHOD = 'method'
K_FIELD	= 'field'
K_STATIC = 'static'
K_VAR = 'var'
K_INT = 'int'
K_CHAR = 'char'
K_BOOLEAN = 'boolean'
K_VOID = 'void'
K_TRUE = 'true'
K_FALSE = 'false'
K_NULL = 'null'
K_THIS = 'this'
K_LET = 'let'
K_DO = 'do'
K_IF = 'if'
K_ELSE = 'else'
K_WHILE = 'while'
K_RETURN = 'return'

KEYWORDS = {
	K_CLASS, K_CONSTRUCTOR, K_FUNCTION, K_METHOD, K_FIELD, K_STATIC, K_VAR,
	K_INT, K_CHAR, K_BOOLEAN, K_VOID, K_TRUE, K_FALSE, K_NULL, K_THIS, K_LET,
	K_DO, K_IF, K_ELSE, K_WHILE, K_RETURN,
}

KEYWORD_CONSTANTS = {K_TRUE, K_FALSE, K_NULL, K_THIS}
CLASS_VAR_KEYWORDS = {K_FIELD, K_STATIC}
SUBROUTINE_KEYWORDS = {K_CONSTRUCTOR, K_FUNCTION, K_METHOD}

BUILT_IN_TYPES = {K_INT, K_CHAR, K_BOOLEAN}
STD_LIBS_CLASSES = {'Array', 'String', 'Memory', 'Screen', 'Keyboard'}

ESCAPE_MAP = {
	'<': '&lt;',
	'>': '&gt;',
	'"': '&quot;',
	'&': '&amp;',
}

# used for tokenizer, unescaped
SYMBOLS = {
	'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&',
	'|', '<', '>', '=', '~',
}
# used for parser, escaped
OPERATORS = {'+', '-', '=', '>', '<', '/'}
OPERATORS = {ESCAPE_MAP.get(sym, sym) for sym in list(OPERATORS)}
UNARY_OPS = {'-', '~'}

# TOKEN TYPES
T_KEYWORD = 'keyword'
T_SYMBOL = 'symbol'
T_INTEGER_CONSTANT = 'integerConstant'
T_STRING_CONSTANT = 'stringConstant'
T_IDENTIFIER = 'identifier'

TERIMAL_TYPES = {
	T_KEYWORD, T_SYMBOL, T_INTEGER_CONSTANT, T_STRING_CONSTANT, T_IDENTIFIER,
}

# LOCAL_SCOPE: for var declared in current scope, instead associated with a class
LOCAL_SCOPE = 'LOCAL_SCOPE'


Token = namedtuple('Token', ['type', 'value'])


class Tokenizer:
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
		escaped = ESCAPE_MAP.get(sym, sym)
		return escaped


ASTNode = namedtuple('ASTNode', ['type', 'body'])


class Parser:
	def __init__(self):
		self.tokens = []
		self.idx = 0
		self.curr_class = ''
		self.class_names = set(STD_LIBS_CLASSES)
		self.var_names_by_class = defaultdict(set)
		self.sub_names_by_class = defaultdict(set)

	def set_input(self, tokens):
		self.tokens = tokens
		self.idx = 0

	def get_token(self):
		token = self.tokens[self.idx]
		self.idx += 1
		return token

	def peek_token(self):
		return self.tokens[self.idx]

	def assert_and_consume(self, t_type=None, value=None):
		t = self.peek_token()
		if t_type is not None:
			assert t.type == t_type, f"token: ({t}), exp_type: '{t_type}')"
		if value is not None:
			assert t.value == value, f"token: ({t}), exp_value: '{value}' idx:{self.idx})"
		return self.get_token()

	def check_symbol(self, value):
		t = self.peek_token()
		return t.type == T_SYMBOL and t.value == value

	def check_keyword(self, value):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value == value

	def walk(self, tokens):
		self.set_input(tokens)
		ast = self.parse_class()
		return ast

	def parse_class(self):
		""" class: 'class' className '{' classVarDec* subroutineDec* '}' """
		body = [self.assert_and_consume(T_KEYWORD, K_CLASS)]
		# add classname to set
		t = self.assert_and_consume(T_IDENTIFIER)
		self.class_names.add(t.value)
		self.curr_class = t.value
		body.append(t)
		# parse class body
		body.append(self.assert_and_consume(T_SYMBOL, '{'))
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
			self._add_class_var(),
		]
		while (self.check_symbol(',')):
			body.extend([
				self.get_token(),
				self._add_class_var(),
			])
		self.assert_and_consume(T_SYMBOL, ';')
		return ASTNode('classVarDec', body)

	def _next_is_class_var_decl(self):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value in CLASS_VAR_KEYWORDS

	def _add_class_var(self):
		t = self.assert_and_consume(T_IDENTIFIER)
		var_name = t.value
		self.var_names_by_class[self.curr_class].add(var_name)
		return t

	def parse_type(self):
		""" type: 'int' | 'char' | 'boolean' | className """
		if self._next_is_type():
			return self.get_token()
		raise TypeError('Not a type!')

	def _next_is_type(self):
		t = self.peek_token()
		return ((t.type == T_KEYWORD and t.value in BUILT_IN_TYPES) or
			 	(t.type == T_IDENTIFIER and t.value in self.class_names))

	def parse_subroutine_decl(self):
		""" subroutineDec: ('constructor'|'function'|'method') ('void'|type)
				subroutineName '(' parameterList ')' subroutineBody
		"""
		body = [
			self.get_token()
		]
		if self.check_keyword(K_VOID):
			body.append(self.get_token())
		else:
			body.append(self.parse_type())
		# register sub name
		t = self.assert_and_consume(T_IDENTIFIER)
		sub_name = t.value
		self.sub_names_by_class[self.curr_class].add(sub_name)
		body.append(t)
		# parameter list and sub body
		body.extend([
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
		""" parameterList: ((type varName) (',' type varName)*)? """
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
		return ASTNode('parameterList', body)

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
			self._add_local_var(),
		]
		while (self.check_symbol(',')):
			body.extend([
				self.get_token(),
				self._add_local_var(),
			])
		body.append(self.assert_and_consume(T_SYMBOL, ';'))
		return ASTNode('varDec', body)

	def _next_is_var_decl(self):
		t = self.peek_token()
		return t.type == T_KEYWORD and t.value == K_VAR

	def _add_local_var(self):
		t = self.assert_and_consume(T_IDENTIFIER)
		var_name = t.value
		self.var_names_by_class[LOCAL_SCOPE].add(var_name)
		return t

	def parse_stmts(self):
		""" statements: statement* """
		stmts = []
		while not (self.check_symbol('}')):
			stmts.append(self.parse_stmt())
		return ASTNode('statements', stmts)

	def parse_stmt(self):
		""" statement: letStatement | ifStatement | whileStatement |
				doStatement | returnStatement
		"""
		t = self.peek_token()
		assert t.type == T_KEYWORD, f"Not a keyword: {self.idx}:{t}"
		if t.value == K_IF:
			return self.parse_if_stmt()
		elif t.value == K_WHILE:
			return self.parse_while_stmt()
		elif t.value == K_LET:
			return self.parse_let_stmt()
		elif t.value == K_DO:
			return self.parse_do_stmt()
		elif t.value == K_RETURN:
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
		body = [self.assert_and_consume(T_KEYWORD, 'let')]
		body.extend(self.parse_lvalue())
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
		] + self.parse_subroutine_call() + [
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
		try:
			expr = self.parse_expr()
			body.append(expr)
		except TypeError as e:
			return ASTNode('expressionList', body)
		while (self.check_symbol(',')):
			body.extend([
				self.get_token(),
				self.parse_expr(),
			])
		return ASTNode('expressionList', body)

	def parse_expr(self):
		""" expresion: term (op term)? """
		body = [self.parse_term()]
		t = self.peek_token()
		if t.value in OPERATORS:
			body.append(self.get_token())
			body.append(self.parse_term());
		return ASTNode('expression', body)

	def parse_lvalue(self):
		""" lvalue is a var or a subscript expr """
		t = self.peek_token()
		if not self._next_is_lvalue():
			raise TypeError('Not an lvalue!')
		res = [self.get_token()]
		if self.check_symbol('['):
			res.extend([
				self.get_token(),
				self.parse_expr(),
				self.assert_and_consume(T_SYMBOL, ']'),
			])
		return res

	def _next_is_lvalue(self):
		t = self.peek_token()
		return (t.type == T_IDENTIFIER and
			(t.value in self.var_names_by_class[self.curr_class] or
			 t.value in self.var_names_by_class[LOCAL_SCOPE]))

	def parse_term(self):
		""" term: integerConstant | stringConstant | keywordConstant | varName |
				varName'[' expression ']' | subroutineCall | '(' expression ')'
				| unaryOp term
		"""
		body = []
		t = self.peek_token()
		# constants
		if (t.type == T_STRING_CONSTANT or
			t.type == T_INTEGER_CONSTANT or
			(t.type == T_KEYWORD and t.value in KEYWORD_CONSTANTS)):
			body = [self.get_token()]
		elif self.check_symbol('('):
			body = [
				self.get_token(),
				self.parse_expr(),
				self.assert_and_consume(T_SYMBOL, ')'),
			]
		elif t.type == T_SYMBOL and t.value in UNARY_OPS:
			body = [self.get_token()] + self.parse_term()
		elif self._next_is_lvalue():
			body = self.parse_lvalue()
		elif self._next_is_subroutine_call():
			body = self.parse_subroutine_call()
		else:
			raise TypeError('Not a term')
		return ASTNode('term', body)

	def parse_subroutine_call(self):
		""" subroutineCall: subroutineName '(' expressionList ')' |
				( className | varName )'.' subroutineName '(' expressionList ')'
		"""
		tokens = []
		# check if it is a membership call expression
		t = self.peek_token()
		if not self._is_regiestered_sub_name(t):
			tokens.append(self.assert_and_consume(T_IDENTIFIER))
			tokens.append(self.assert_and_consume(T_SYMBOL, '.'))
		# consume sub name
		tokens.append(self.assert_and_consume(T_IDENTIFIER))
		tokens.extend([
			self.assert_and_consume(T_SYMBOL, '('),
			self.parse_expr_list(),
			self.assert_and_consume(T_SYMBOL, ')'),
		])
		return tokens

	def _is_regiestered_sub_name(self, t):
		return (t.type == T_IDENTIFIER and
				t.value in self.sub_names_by_class[self.curr_class])

	def _next_is_subroutine_call(self):
		t = self.peek_token()
		if self._is_regiestered_sub_name(t):
			return True
		if (t.value in self.var_names_by_class[self.curr_class] or
			t.value in self.var_names_by_class[LOCAL_SCOPE] or
			t.value in STD_LIBS_CLASSES):
			next_token = self.tokens[self.idx+1]
			# check for '.'
			if not (next_token.type == T_SYMBOL and next_token.value == '.'):
				return False
			# do not bother check the call on std lib classes
			if t.value in STD_LIBS_CLASSES:
				return True
			# check user defined sub is registered (TODO: this is unrealistic without
			# extra work of actually checking the type of a var)
			return self._is_regiestered_sub_name(next_next_token)
		return False


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
		ast = self.parser.walk(tokens)
		self.generate_outputs_from_ast(ast)

	def generate_outputs_from_ast(self, ast):
		def write_xml_line(token, indent_lv):
			self.outputs.append(
				f"{'  ' * indent_lv}<{token.type}> {token.value} </{token.type}>")
		def write_xml_open_tag(ast, indent_lv):
			self.outputs.append(f"{'  ' * indent_lv}<{ast.type}>")
		def write_xml_close_tag(ast, indent_lv):
			self.outputs.append(f"{'  ' * indent_lv}</{ast.type}>")
		self.visit(ast, write_xml_line, write_xml_open_tag, write_xml_close_tag)

	def visit(self, ast, term_cb, enter_cb = None, exit_cb = None, level = 0):
		is_terminal = ast.type in TERIMAL_TYPES
		if not is_terminal:
			if enter_cb is not None: enter_cb(ast, level)
			for node in ast.body:
				self.visit(node, term_cb, enter_cb, exit_cb, level + 1)
			if exit_cb is not None: exit_cb(ast, level)
		else:
			term_cb(ast, level)

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
