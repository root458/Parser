from ast import literal_eval as make_tuple

code = ''


def get_ast_from_file():
    with open('ast.txt', 'r') as file:
        ast = file.read()
    return ast


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
            code += '\n{}'.format(body[1][1])
            body = body[2]


if __name__ == "__main__":
    body = make_tuple(get_ast_from_file())[3][1]
    # print(body)
    generate_code(body)
    # print(len(body))
    print(code)
