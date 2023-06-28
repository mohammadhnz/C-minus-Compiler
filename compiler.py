from parser_utils.code_generator import log_codes
from parser_utils.parser import Parser
from scanner_utils.scanner import Scanner


def run():
    try:
        scanner = Scanner()
        parser = Parser(scanner)
        parser.parse()
    except:
        pass
    log_codes()


run()
