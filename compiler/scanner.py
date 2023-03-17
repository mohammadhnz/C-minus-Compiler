class Scanner:
    def __init__(self, input_code):
        self.code = input_code
        keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
        symbols = [
            ";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="
        ]
        self.patterns = [
            ("NUM",),
            ("KEYWORD", "(" + "|".join(keywords) + ")"),
            ("ID", ""),
            ("SYMBOL", "(" + "|".join(symbols) + ")"),

        ]

    def get_next_token(self):
        return None, None, None

    def find_num(self):
