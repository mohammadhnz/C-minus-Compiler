"""
MohammadAli Hosseinnezhad Abdi 98170787
Roya Ghavami Adel 98171031
"""
from parser.parser import Parser
from scanner.scanner import Scanner


def run():
    scanner = Scanner()
    parser = Parser(scanner)
    parser.parse()
    # initialize_states()
    # scanner = Scanner()
    # while scanner.code:
    #     scanner.get_next_token()


run()
