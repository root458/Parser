from ast import keyword
from lex import lex
from yacc import yacc

# Global variables
has_error = False
scanner_error_logs = ''
error_logs = ''
# Keywords
types = ('float', 'string', 'int', 'void')
keywords = ('using', 'namespace', 'std', 'main',
            'return', 'cout', 'cin', 'if', 'else')

# Tokens
tokens = ('INCLUDE', 'IOSTREAM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
          'IDENTIFIER', 'ENDL', 'STDIN', 'STDOUT', 'STRINGLITERAL', 'COMMENT', 'AND', 'OR', 'GREATER', 'LESS', 'EQUAL',
          'GREATEREQUAL', 'LESSEQUAL', 'NOTEQUAL', 'EQUALITY', 'NUMBER')

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_INCLUDE = r'\#include'
t_IOSTREAM = r'<iostream>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_ENDL = r';'
t_STDIN = r'>>'
t_STDOUT = r'<<'
t_STRINGLITERAL = r'"+([^"]*)+"'
t_COMMENT = r'//+(.*)'
t_AND = r'&&'
t_OR = r'\|\|'
t_GREATER = r'>'
t_GREATEREQUAL = r'>='
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_NOTEQUAL = r'!='
t_EQUALITY = r'=='
t_EQUAL = r'='


def t_IDENTIFIER(t):
    r'[A-Za-z]([A-Za-z0-9_]+)?'
    t.value = t.value
    return t


def t_NUMBER(t):
    r'\d+(\.\d*)?'
    return t


def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print(f'Unexpected character {t.value[0]!r} at line no {t.lineno}')
    t.lexer.skip(1)


lexer = lex()

################
# GRAMMARS
################

# <compound stmt> --> { <stmt list> }
# <stmt list> --> <stmt> <stmt list> | epsilon


def p_program(p):
    '''
    program : include namespace main_def LCURLY body RCURLY
    '''
    p[0] = ('program', p[1], p[2], p[5])


def p_include(p):
    '''
    include : INCLUDE IOSTREAM
    '''
    p[0] = ('include', p[2])


def p_namespace(p):
    '''
    namespace : IDENTIFIER IDENTIFIER IDENTIFIER endl
    '''
    if (p[1] == 'using' and p[2] == 'namespace') and p[3] == 'std':
        p[0] = ('namespace', p[3])
    else:
        global has_error
        global error_logs
        has_error = True
        if p[1] != 'using':
            error_logs += "Expected 'using' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[1])

        if p[2] != 'namespace':
            error_logs += "Expected 'namespace' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[2])

        if p[3] != 'std':
            error_logs += "Expected 'std' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[3])


def p_main_def(p):
    '''
    main_def : IDENTIFIER IDENTIFIER LPAREN RPAREN
    '''
    if (p[1] == 'int' and p[2] == 'main'):
        p[0] = ('main', p[1] + ' ' + p[2] + p[3]+p[4])
    else:
        global has_error
        global error_logs
        has_error = True
        if p[1] != 'int':
            error_logs += "Expected 'int' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[1])

        if p[2] != 'main':
            error_logs += "Expected 'main' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[2])


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
    stmt_list : IDENTIFIER NUMBER endl
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
    conditional : IDENTIFIER LPAREN logical RPAREN LCURLY oneline RCURLY IDENTIFIER LCURLY oneline RCURLY
    '''
    if (p[1] == 'if' and p[8] == 'else'):
        p[0] = ('conditional', p[1], p[3], p[6], p[8], p[10])
    else:
        global has_error
        global error_logs
        has_error = True
        if p[1] != 'if':
            error_logs += "Expected 'if' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[1])

        if p[2] != 'else':
            error_logs += "Expected 'else' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[2])


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
            | expression GREATEREQUAL expression
            | expression LESS expression
            | expression LESSEQUAL expression
            | expression NOTEQUAL expression
            | expression EQUALITY expression
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
    factor : IDENTIFIER
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
    output : IDENTIFIER STDOUT string_literal endl
           | IDENTIFIER STDOUT variable_name endl
    '''
    if p[1] == 'cout':
        p[0] = ('output', p[3])
    else:
        global has_error
        global error_logs
        has_error = True
        if p[1] != 'cout':
            error_logs += "Expected 'cout' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[1])


def p_string_literal(p):
    '''
    string_literal : STRINGLITERAL
    '''
    p[0] = ('string literal', p[1])


def p_input(p):
    '''
    input : IDENTIFIER STDIN variable_name endl
    '''
    if (p[1] == 'cin'):
        p[0] = ('input', p[3])
    else:
        global has_error
        global error_logs
        has_error = True
        if p[1] != 'cin':
            error_logs += "Expected 'cin' instead of '{1}' on line {0}\n\n".format(
                p.lineno(1), p[1])


def p_declaration(p):
    '''
    declaration : data_type variable_name endl
    '''
    p[0] = ('declaration', p[1], p[2])


def p_data_type(p):
    '''
    data_type : IDENTIFIER
    '''
    if (p[1] in types):
        p[0] = ('data_type', p[1])
    else:
        global has_error
        global error_logs
        has_error = True
        error_logs += "'{1}' on line {0} is not a valid data type\n\n".format(
            p.lineno(1), p[1])


def p_variable_name(p):
    '''
    variable_name : IDENTIFIER
    '''
    # if (p[1] not in keyword):
    p[0] = ('variable', p[1])


def p_endl(p):
    '''
    endl : ENDL
    '''
    p[0] = ('endl', p[1])


def p_error(p):
    global scanner_error_logs
    scanner_error_logs += f'{p.value!r} on line number {p.lineno!r} is unexpected\n'

################
# PARSER
################


parser = yacc()

# Read code from file
with open('code.txt', 'r') as file:
    code = file.read()

# Parse an expression
ast = parser.parse(code)

if ast == None:
    print('\n')
    print('Error scanning code')
    print('\n')
    print(scanner_error_logs)
    print('\n')
else:
    print('\n\n\n')
    if has_error:
        print(error_logs)
    else:
        print(ast)
    print('\n\n\n')
