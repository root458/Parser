from lex import lex
from yacc import yacc

# Tokens
tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
          'VARIABLE', 'ENDL', 'CIN', 'STDIN', 'COUT',
          'STDOUT', 'STRINGLITERAL', 'COMMENT', 'AND', 'OR', 'GREATER', 'LESS', 'EQUAL',
          'IF', 'ELSE', 'RETURN', 'DATATYPE', 'NUMBER')

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_VARIABLE = r'_[A-Za-z]([A-Za-z0-9_]+)?'
t_ENDL = r';'
t_CIN = r'cin'
t_STDIN = r'>>'
t_COUT = r'cout'
t_STDOUT = r'<<'
t_STRINGLITERAL = r'"+([^"]*)+"'
t_COMMENT = r'//+(.*)'
t_AND = r'&&'
t_OR = r'\|\|'
t_GREATER = r'>'
t_LESS = r'<'
t_EQUAL = r'='
t_IF = r'if'
t_ELSE = r'else'
t_RETURN = r'return'


def t_DATATYPE(t):
    r'^(string|float)'
    t.value = t.value
    return t


def t_NUMBER(t):
    r'\d+(\.\d*)?'
    return t


def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print(f'Unexpected character {t.value[0]!r}')
    t.lexer.skip(1)


lexer = lex()

################
# GRAMMARS
################

# <compound stmt> --> { <stmt list> }
# <stmt list> --> <stmt> <stmt list> | epsilon


def p_body(p):
    '''
    body : stmt_list
    '''
    p[0] = ('body', p[1])


def p_stmt_list(p):
    '''
    stmt_list : statement stmt_list
    '''
    p[0] = ('statements', p[1], p[2])


def p_stmt_list_end(p):
    '''
    stmt_list : RETURN NUMBER endl
    '''
    p[0] = ('end ', p[1] + ' ' + p[2])


def p_statement(p):
    '''
    statement : comment
              | declaration
              | assignment
              | output
              | input
              | conditional
    '''
    p[0] = ('statement', p[1])


def p_conditional(p):
    '''
    conditional : IF LPAREN logical RPAREN LCURLY oneline RCURLY ELSE LCURLY oneline RCURLY
    '''
    p[0] = ('conditional', p[1], p[3], p[6], p[8], p[10])


def p_oneline(p):
    '''
    oneline : comment
            | declaration
            | assignment
            | output
            | input
    '''
    p[0] = ('statement', p[1])


def p_logical(p):
    '''
    logical : boolean AND boolean
            | boolean OR boolean
    '''
    p[0] = ('logical', p[2], p[1], p[3])


def p_logical_boolean(p):
    '''
    logical : boolean
    '''
    p[0] = p[1]


def p_boolean(p):
    '''
    boolean : expression GREATER expression
            | expression LESS expression
    '''
    p[0] = ('boolean', p[2], p[1], p[3])


def p_assignment(p):
    '''
    assignment : variable_name EQUAL expression endl
    '''
    p[0] = ('assignment', p[1], p[3])


def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    #            | term GREATER term
    #           | term LESS term
    p[0] = ('expression', p[2], p[1], p[3])


def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]


def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('term', p[2], p[1], p[3])


def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]


def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])


def p_factor_name(p):
    '''
    factor : VARIABLE
    '''
    p[0] = ('variable', p[1])


def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])


def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped expression', p[2])


def p_comment(p):
    '''
    comment : COMMENT
    '''
    p[0] = ('comment', p[1])


def p_output(p):
    '''
    output : COUT STDOUT string_literal endl
           | COUT STDOUT variable_name endl
    '''
    p[0] = ('output', p[3])


def p_string_literal(p):
    '''
    string_literal : STRINGLITERAL
    '''
    p[0] = ('string literal', p[1])


def p_input(p):
    '''
    input : CIN STDIN variable_name endl
    '''
    p[0] = ('input', p[3])


def p_declaration(p):
    '''
    declaration : data_type variable_name endl
    '''
    p[0] = ('declaration', p[1], p[2])


def p_data_type(p):
    '''
    data_type : DATATYPE
    '''
    p[0] = ('data_type', p[1])


def p_variable_name(p):
    '''
    variable_name : VARIABLE
    '''
    p[0] = ('variable', p[1])


def p_endl(p):
    '''
    endl : ENDL
    '''
    p[0] = ('endl', p[1])


def p_error(p):
    print(f'Syntax error at {p.value!r}, line number {p.lineno!r}')

################
# PARSER
################


parser = yacc()

# Read code from file
with open('code.txt', 'r') as file:
    code = file.read()

print(code)

# Parse an expression
ast = parser.parse(code)
print(ast)
