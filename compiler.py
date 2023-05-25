from parser_utils.parser import Parser
from scanner_utils.scanner import Scanner


def run():
    scanner = Scanner()
    parser = Parser(scanner)
    parser.parse()

run()
