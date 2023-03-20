from scanner.scanner import Scanner


def run():
    scanner = Scanner()
    while scanner.code:
        scanner.get_next_token()


run()
