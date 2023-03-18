from collections import defaultdict

from compiler.scanner import Scanner


def read_input_file():
    with open("input.txt", "r") as file:
        return file.read()


def run():
    data = read_input_file()
    # scanner = Scanner("123!456d    12348\n   12345")
    scanner = Scanner("void ali = < > ==")
    tokens = defaultdict(list)
    errs = defaultdict
    while scanner.code:
        token = scanner.get_next_token()
        print(token)


run()
