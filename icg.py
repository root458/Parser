from ast import literal_eval as make_tuple

code = ''
temp = 1
label = 1


def get_ast_from_file():
    with open('ast.txt', 'r') as file:
        ast = file.read()
    return ast

#################################
#
# QUADRUPLES STATEMENT GENERATORS
#
#################################


def gen_declaration(tup):
    return '(DECLARE, {}, {})'.format(tup[1][1], tup[2][1])


def gen_output(tup):
    if tup[1][0] == 'variable':
        return '(PRINT, VARIABLE, {})'.format(tup[1][1])
    if tup[1][0] == 'string literal':
        return '(PRINT, LITERAL, {})'.format(tup[1][1])


def gen_input(tup):
    return '(GET, {})'.format(tup[1][1])


def gen_assignment(tup):
    snippet = ''
    global temp
    if tup[2][0] == 'term':
        if tup[2][1] == '*':
            snippet += '(MUL, T{}, {}, {})'.format(temp,
                                                   tup[2][2][1], tup[2][3][1])
            temp += 1
        if tup[2][1] == '/':
            snippet += '(DIV, T{}, {}, {})'.format(temp,
                                                   tup[2][2][1], tup[2][3][1])
            temp += 1
        snippet += '\n(ASSIGN, {}, T{})'.format(tup[1][1], (temp-1))

    if tup[2][0] == 'expression':

        # Variable and variable
        if tup[2][2][0] != 'term' and tup[2][3][0] != 'term':
            if tup[2][1] == '+':
                snippet += '(ADD, {}, {}, {})'.format(
                    tup[1][1], tup[2][2][1], tup[2][3][1])
            else:
                snippet += '(SUB, {}, {}, {})'.format(
                    tup[1][1], tup[2][2][1], tup[2][3][1])

        # Term variable/number |
        if tup[2][2][0] == 'term':
            if tup[2][2][1] == '*':
                snippet += '(MUL, T{}, {}, {})'.format(temp,
                                                       tup[2][2][2][1], tup[2][2][3][1])
                temp += 1
            if tup[2][2][1] == '/':
                snippet += '(DIV, T{}, {}, {})'.format(temp,
                                                       tup[2][2][2][1], tup[2][2][3][1])
                temp += 1

            if tup[2][3][0] == 'term':
                if tup[2][3][1] == '*':
                    snippet += '\n(MUL, T{}, {}, {})'.format(temp,
                                                             tup[2][3][2][1], tup[2][3][3][1])
                    temp += 1
                if tup[2][3][1] == '/':
                    snippet += '\n(DIV, T{}, {}, {})'.format(temp,
                                                             tup[2][3][2][1], tup[2][3][3][1])
                    temp += 1

                if tup[2][1] == '+':
                    snippet += '\n(ADD, {}, T{}, T{})'.format(
                        tup[1][1], (temp-2), (temp-1))
                else:
                    snippet += '\n(SUB, {}, T{}, T{})'.format(
                        tup[1][1], (temp-2), (temp-1))
            else:
                if tup[2][1] == '+':
                    snippet += '\n(ADD, {}, T{}, {})'.format(
                        tup[1][1], (temp-1), tup[2][3][1])
                else:
                    snippet += '\n(SUB, {}, T{}, {})'.format(
                        tup[1][1], (temp-1), tup[2][3][1])

        else:
            if tup[2][3][0] == 'term':
                if tup[2][3][1] == '*':
                    snippet += '(MUL, T{}, {}, {})'.format(temp,
                                                           tup[2][3][2][1], tup[2][3][3][1])
                    temp += 1
                if tup[2][3][1] == '/':
                    snippet += '(DIV, T{}, {}, {})'.format(temp,
                                                           tup[2][3][2][1], tup[2][3][3][1])
                    temp += 1

                if tup[2][1] == '+':
                    snippet += '\n(ADD, {}, {}, T{})'.format(
                        tup[1][1], tup[2][2][1], (temp-1))
                else:
                    snippet += '\n(SUB, {}, {}, T{})'.format(
                        tup[1][1], tup[2][2][1], (temp-1))

    return snippet


def gen_if_clause(tup):
    snippet = ''
    global temp
    global label

    condition = tup[1]

    if condition[0] == 'boolean':
        if condition[1] == '>':
            snippet += '(GT, T{}, {}, {})'.format(temp,
                                                  condition[2][1], condition[3][1])
            temp += 1
        elif condition[1] == '>=':
            snippet += '(GE, T{}, {}, {})'.format(temp,
                                                  condition[2][1], condition[3][1])
            temp += 1
        elif condition[1] == '<':
            snippet += '(LT, T{}, {}, {})'.format(temp,
                                                  condition[2][1], condition[3][1])
            temp += 1
        elif condition[1] == '<=':
            snippet += '(LE, T{}, {}, {})'.format(temp,
                                                  condition[2][1], condition[3][1])
            temp += 1
        elif condition[1] == '==':
            snippet += '(EQ, T{}, {}, {})'.format(temp,
                                                  condition[2][1], condition[3][1])
            temp += 1
        else:
            snippet += '(NEQ, T{}, {}, {})'.format(temp,
                                                   condition[2][1], condition[3][1])
            temp += 1

        snippet += '\n(NOT, T{}, T{})'.format((temp), (temp-1))
        temp += 1
        snippet += '\n(IF, T{}, GOTO LABEL L{})'.format((temp-1), label)
        label += 1
        snippet += '\n*'
        snippet += '\n(LABEL L{})'.format((label-1))

    else:
        # For logical
        # First clause
        if condition[2][1] == '>':
            snippet += '(GT, T{}, {}, {})'.format(temp,
                                                  condition[2][2][1], condition[2][3][1])
            temp += 1
        elif condition[2][1] == '>=':
            snippet += '(GE, T{}, {}, {})'.format(temp,
                                                  condition[2][2][1], condition[2][3][1])
            temp += 1
        elif condition[2][1] == '<':
            snippet += '(LT, T{}, {}, {})'.format(temp,
                                                  condition[2][2][1], condition[2][3][1])
            temp += 1
        elif condition[2][1] == '<=':
            snippet += '(LE, T{}, {}, {})'.format(temp,
                                                  condition[2][2][1], condition[2][3][1])
            temp += 1
        elif condition[2][1] == '==':
            snippet += '(EQ, T{}, {}, {})'.format(temp,
                                                  condition[2][2][1], condition[2][3][1])
            temp += 1
        else:
            snippet += '(NEQ, T{}, {}, {})'.format(temp,
                                                   condition[2][2][1], condition[2][3][1])
            temp += 1

        # Second clause
        if condition[3][1] == '>':
            snippet += '\n(GT, T{}, {}, {})'.format(temp,
                                                    condition[3][2][1], condition[3][3][1])
            temp += 1
        elif condition[3][1] == '>=':
            snippet += '\n(GE, T{}, {}, {})'.format(temp,
                                                    condition[3][2][1], condition[3][3][1])
            temp += 1
        elif condition[3][1] == '<':
            snippet += '\n(LT, T{}, {}, {})'.format(temp,
                                                    condition[3][2][1], condition[3][3][1])
            temp += 1
        elif condition[3][1] == '<=':
            snippet += '\n(LE, T{}, {}, {})'.format(temp,
                                                    condition[3][2][1], condition[3][3][1])
            temp += 1
        elif condition[3][1] == '==':
            snippet += '\n(EQ, T{}, {}, {})'.format(temp,
                                                    condition[3][2][1], condition[3][3][1])
            temp += 1
        else:
            snippet += '\n(NEQ, T{}, {}, {})'.format(temp,
                                                     condition[3][2][1], condition[3][3][1])
            temp += 1

        # Combine Logical
        if condition[1] == '&&':
            snippet += '\n(AND, T{}, T{}, T{})'.format(temp,
                                                       (temp-2), (temp-1))
            temp += 1
            snippet += '\n(NOT, T{}, T{})'.format(temp, (temp-1))
            temp += 1
        else:
            snippet += '\n(OR, T{}, T{}, T{})'.format(temp, (temp-2), (temp-1))
            temp += 1
            snippet += '\n(NOT, T{}, T{})'.format(temp, (temp-1))
            temp += 1
        snippet += '\n(IF, T{}, GOTO LABEL L{})'.format((temp-1), label)
        label += 1
        snippet += '\n*'
        snippet += '\n(LABEL L{})'.format((label-1))

    snippet = snippet.replace('\n*', gen_else_clause(tup[2]))

    return snippet


def gen_else_clause(tup):
    snippet = ''

    # 0 -> block
    # 1 -> statement tuple
    # 2 -> block tuple

    while (True):
        if tup[0] == 'end':
            break
        else:
            if tup[1][1][0] == 'output':
                snippet += '\n{}'.format(gen_output(tup[1][1]))

            if tup[1][1][0] == 'input':
                snippet += '\n{}'.format(gen_input(tup[1][1]))

            if tup[1][1][0] == 'declaration':
                snippet += '\n{}'.format(gen_declaration(tup[1][1]))

            if tup[1][1][0] == 'assignment':
                snippet += '\n{}'.format(gen_assignment(tup[1][1]))

            if tup[1][1][0] == 'if clause':
                snippet += '\n{}'.format(gen_if_clause(tup[1][1]))

            if tup[1][1][0] == 'else clause':
                snippet += '\n{}'.format(gen_else_clause(tup[1][1]))

            tup = tup[2]

    return snippet


########################################################


def generate_code(body):
    global code

    # 0 -> statements
    # 1 -> statement
    # 2 -> statement tuple

    stmt = body[1]
    while True:
        if body[0] == 'end':
            code += '\n(END)'
            # Get code
            break
        else:
            print(body[1][1])
            # Skip comment statement

            if body[1][1][0] == 'declaration':
                code += '\n{}'.format(gen_declaration(body[1][1]))

            if body[1][1][0] == 'output':
                code += '\n{}'.format(gen_output(body[1][1]))

            if body[1][1][0] == 'input':
                code += '\n{}'.format(gen_input(body[1][1]))

            if body[1][1][0] == 'assignment':
                code += '\n{}'.format(gen_assignment(body[1][1]))

            if body[1][1][0] == 'if clause':
                code += '\n{}'.format(gen_if_clause(body[1][1]))

            if body[1][1][0] == 'else clause':
                code += '{}'.format(gen_else_clause(body[1][1][1]))

            body = body[2]


if __name__ == "__main__":
    body = make_tuple(get_ast_from_file())[3][1]
    generate_code(body)
    print(code)
