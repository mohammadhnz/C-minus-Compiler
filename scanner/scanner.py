from scanner.states import States, ACCEPT_STATES, transitions, TOKEN_NAMES, ERROR_STATES


class Scanner:
    def __init__(self, input_code):
        self.code = input_code
        self.line_number = 1
        self.keywords = ["break", "else", "if", "int", "repeat", "return", "until", "void" ]
        symbols = [
            ";", ":", ",", "\[", "\]", "\(", "\)", "\{", "\}", "\+", "\-", "\*", "=", "<", "=="
        ]
        # self.patterns = [
        #     ("NUM", r'(\d+).*'),
        #     ("KEYWORD", "(" + "|".join(keywords) + ").*"),
        #     ("ID", r'([A-Za-z][A-Za-z0-9]*).*'),
        #     ("SYMBOL", "(" + "|".join(symbols) + ").*"),
        # ]

    def get_next_token(self):
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
        return line_number, TOKEN_NAMES[self.get_state(current_state, word)], word

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
