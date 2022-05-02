from ast import literal_eval as make_tuple

def get_ast_from_file():
    with open('ast.txt', 'r') as file:
        ast = file.read()
    return ast


if __name__ == "__main__":
    body = make_tuple(get_ast_from_file())[3]
    print(body)
