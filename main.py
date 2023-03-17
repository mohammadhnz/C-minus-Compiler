from collections import defaultdict

from compiler.scanner import Scanner


def read_input_file():
    with open("input.txt", "r") as file:
        return file.read()


def run():
    data = read_input_file()
    scanner = Scanner(data)
    tokens = defaultdict(list)
    errs = defaultdict
    while scanner.code:
        line, err, token = scanner.get_next_token()
        if err != None:
            print("err")
        print(token)
        break

run()