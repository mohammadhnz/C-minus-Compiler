from collections import defaultdict

from scanner_utils.states import States, ACCEPT_STATES, transitions, TOKEN_NAMES, ERROR_STATES
from scanner_utils.logger import TokenLogger, LexicalErrorsLogger, SymbolsLogger


class Scanner:
    def __init__(self):
        self.code = self.read_input_file()
        self.line_number = 1
        self.keywords = ["break", "else", "if", "int", "repeat", "return", "until", "void"]
        self.tokens = defaultdict(list)
        self.lexical_errors = defaultdict(list)
        self.symbols = self.keywords.copy()

    def read_input_file(self):
        with open("input.txt", "r") as file:
            return file.read()

    def get_next_token(self):
        if not self.code:
            return "$", "$", self.line_number
        current_state = States.INITIALIZE
        word = ""
        line_number = self.line_number
        while current_state not in ACCEPT_STATES + ERROR_STATES:
            character = self._read_first_character()
            state = self.get_next_state(current_state, character)
            if state == -1:
                self._handle_extra_readed_character(character)
                break
            current_state = state
            word += character
            if not self.code:
                break
        # self._log_token(line_number, TOKEN_NAMES[self.get_state(current_state, word)], word)
        if TOKEN_NAMES[self.get_state(current_state, word)] in ['COMMENT', 'white space']:
            return self.get_next_token()
        return TOKEN_NAMES[self.get_state(current_state, word)], word, self.line_number

    def _handle_extra_readed_character(self, character):
        if ord(character) == 10:
            self.line_number -= 1
        self.code = character + self.code

    def _read_first_character(self):
        self.code, character = self.code[1:], self.code[0]
        if ord(character) == 10:
            self.line_number += 1
        return character

    def get_next_state(self, current_state, character):
        for is_valid, next_state in transitions[current_state]:
            if is_valid(character):
                return next_state
        return -1

    def get_state(self, state, word):
        if state in [States.ID_DETECTED, States.ID_FINISHED] and word in self.keywords:
            return States.KEYWORD
        return state

    def _log_token(self, line_number, token_name, word):
        if token_name in ["Unmatched comment", "Invalid number", "Invalid input", "Unclosed comment"]:
            self.lexical_errors[line_number].append((word, token_name))
        elif token_name in ["white space", "COMMENT"]:
            return
        else:
            if token_name in ["KEYWORD", "ID"]:
                if word not in self.symbols:
                    self.symbols.append(word)
            self.tokens[line_number].append((token_name, word.strip()))
        TokenLogger(self.tokens).log()
        SymbolsLogger(self.symbols).log()
        LexicalErrorsLogger(self.lexical_errors).log()
