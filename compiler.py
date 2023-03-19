from collections import defaultdict

from scanner.scanner import Scanner


def read_input_file():
    with open("input.txt", "r") as file:
        return file.read()


def log_tokens(tokens):
    report = ""
    for line_number, tokens in tokens.items():
        report += str(line_number) + ".\t"
        for token in tokens:
            report += "(" + token[0] + ", " + token[1] + ")" + " "
        report += "\n"
    return report


def log_lexical_erros(lexical_errors):
    if not lexical_errors:
        return "There is no lexical error."
    report = ""
    for line_number, lexical_errors in lexical_errors.items():
        report += str(line_number) + ".\t"
        for lexical_error in lexical_errors:
            if lexical_error[1] == "Unclosed comment":
                text = lexical_error[0] if len(lexical_error[0]) <= 7 else lexical_error[0][:7] + "..."
                report += "(" + text + ", " + lexical_error[1] + ")" + " "
                continue
            report += "(" + lexical_error[0] + ", " + lexical_error[1] + ")" + " "
        report += "\n"
    return report


def log_symbols(symbols):
    report = ""
    for i, symbol in enumerate(symbols):
        report += str(i + 1) + ".\t" + symbol + "\n"
    return report


def print_in_file(report, file_name):
    with open(file_name, "w") as file:
        file.write(report)


def run():
    data = read_input_file()
    scanner = Scanner(data)
    tokens = defaultdict(list)
    lexical_errors = defaultdict(list)
    symbols = ["break", "else", "if", "int", "repeat", "return", "until", "void"]
    while scanner.code:
        line_number, token_name, word = scanner.get_next_token()
        if token_name in ["Unmatched comment", "Invalid number", "Invalid input", "Unclosed comment"]:
            lexical_errors[line_number].append((word, token_name))
        elif token_name in ["white space", "COMMENT"]:
            continue
        else:
            if token_name in ["KEYWORD", "ID"]:
                if word not in symbols:
                    symbols.append(word)
            tokens[line_number].append((token_name, word.strip()))
    print_in_file(log_tokens(tokens), "tokens.txt")
    print_in_file(log_lexical_erros(lexical_errors), "lexical_errors.txt")
    print_in_file(log_symbols(symbols), "symbol_table.txt")


run()
