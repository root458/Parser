
def get_ast_from_file():
    with open('ast.txt', 'r') as file:
        ast = file.read()
    return ast

if __name__ == "__main__":
    print(get_ast_from_file())