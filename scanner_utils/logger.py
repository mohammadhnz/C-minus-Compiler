from abc import ABC, abstractmethod


class Logger(ABC):
    file_path = ""

    def __init__(self, data):
        self.data = data

    def log(self):
        presented_data = self._present_data()
        self.print_to_file(presented_data)

    def print_to_file(self, presented_data):
        with open(self.file_path, "w") as file:
            file.write(presented_data)

    @abstractmethod
    def _present_data(self):
        pass


class TokenLogger(Logger):
    file_path = "tokens.txt"

    def _present_data(self):
        report = ""
        for line_number, tokens in self.data.items():
            report += str(line_number) + ".\t"
            for token in tokens:
                report += "(" + token[0] + ", " + token[1] + ")" + " "
            report += "\n"
        return report


class LexicalErrorsLogger(Logger):
    file_path = "lexical_errors.txt"

    def _present_data(self):
        if not self.data:
            return "There is no lexical error."
        report = ""
        for line_number, lexical_errors in self.data.items():
            report += str(line_number) + ".\t"
            for lexical_error in lexical_errors:
                if lexical_error[1] == "Unclosed comment":
                    text = lexical_error[0] if len(lexical_error[0]) <= 7 else lexical_error[0][:7] + "..."
                    report += "(" + text + ", " + lexical_error[1] + ")" + " "
                    continue
                report += "(" + lexical_error[0] + ", " + lexical_error[1] + ")" + " "
            report += "\n"
        return report


class SymbolsLogger(Logger):
    file_path = "symbol_table.txt"

    def _present_data(self):
        report = ""
        for i, symbol in enumerate(self.data):
            report += str(i + 1) + ".\t" + symbol + "\n"
        return report
