from ast import literal_eval as make_tuple

code = ''


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

            if body[1][1][0] == 'declaration':
                code += '\n{}'.format(gen_declaration(body[1][1]))

            if body[1][1][0] == 'output':
                code += '\n{}'.format(gen_output(body[1][1]))

            if body[1][1][0] == 'input':
                code += '\n{}'.format(gen_input(body[1][1]))

            body = body[2]


if __name__ == "__main__":
    body = make_tuple(get_ast_from_file())[3][1]
    # print(body)
    generate_code(body)
    # print(len(body))
    print(code)
