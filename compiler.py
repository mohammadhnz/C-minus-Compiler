from parser.parser import Parser
from scanner.scanner import Scanner


def run():
    scanner = Scanner()
    parser = Parser(scanner)
    parser.parse()

run()
