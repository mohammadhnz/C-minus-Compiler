import re


class Scanner:
    def __init__(self, input_code):
        self.code = input_code
        keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
        symbols = [
            ";", ":", ",", "\[", "\]", "\(", "\)", "\{", "\}", "\+", "\-", "\*", "=", "<", "=="
        ]
        self.patterns = [
            ("NUM", r'(\d+).*'),
            ("KEYWORD", "(" + "|".join(keywords) + ").*"),
            ("ID", r'([A-Za-z][A-Za-z0-9]*).*'),
            ("SYMBOL", "(" + "|".join(symbols) + ").*"),
        ]

    def get_next_token(self):
        for token_type, token_pattern in self.patterns:
            pattern = re.compile(token_pattern, re.DOTALL)
            match = re.fullmatch(pattern, self.code)
            print(token_type, match, pattern)

        return None, None, None

    def find_num(self):
        pass
