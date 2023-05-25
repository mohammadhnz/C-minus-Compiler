from anytree import NodeMixin, RenderTree, Node

from parser_utils.states import NonTerminal, initialize_states
from scanner_utils.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_state = None

    def parse(self):
        first_token = self.scanner.get_next_token()
        states = initialize_states()
        program = states["Program"]
        errors = []
        root = NodeParser(program, first_token, self.scanner, errors=errors)
        root.parse()
        final_result = ""
        for pre, fill, node in RenderTree(root):
            final_result += "%s%s" % (pre, node.name) + '\n'
        with open('parse_tree.txt', 'w', encoding="utf-8") as file:
            file.write(final_result[:-1])
        with open('syntax_errors.txt', 'w', encoding="utf-8") as file:
            if errors:
                for error in errors:
                    file.write(error + "\n")
            else:
                file.write('There is no syntax error.')


class NodeParser(NodeMixin):

    def __init__(self, node: NonTerminal, current_token, scanner, parent=None, errors=None):
        self.node: NonTerminal = node
        self.name = node.name
        self.current_token = current_token
        self.scanner = scanner
        self.parent = parent
        self.errors = list() if errors is None else errors

    def parse(self):
        while True:
            for first_set, path in self.node.transition_diagram.paths:
                if self.advance_forward(path, first_set):
                    if self.current_token[0] == '$':
                        if self.name == 'Program' and not self._is_unexpected_eof():
                            Node("$", parent=self)
                    return self.current_token
            if self._is_unexpected_eof():
                self.parent = None
                return self.current_token
            if self.node.transition_diagram.epsilon:
                if self.current_token[0] in self.node.follow_set or self.current_token[1] in self.node.follow_set:
                    Node("epsilon", parent=self)
                    return self.current_token
                else:
                    if self.current_token[0] == '$' and not self._is_unexpected_eof():
                        self.parent = None
                        self._create_unexpected_eof_err()
                        return self.current_token
                    self._log_illegal()
                    self.current_token = self.scanner.get_next_token()
            else:
                if self.current_token[0] in self.node.follow_set or self.current_token[1] in self.node.follow_set:
                    self.errors.append(
                        "#" + str(self.current_token[2]) + " : syntax error, missing " + self.name
                    )
                    self.parent = None
                    return self.current_token
                else:
                    self._log_illegal()
                    self.current_token = self.scanner.get_next_token()

    def _unexpected_eof(self):
        if not self.errors:
            return False
        return "Unexpected EOF" not in self.errors[-1]

    def _is_unexpected_eof(self):
        if not self.errors:
            return False
        return "Unexpected EOF" in self.errors[-1]

    def _log_illegal(self):
        if self.current_token[0] in ['ID', 'NUM']:
            self.errors.append(
                "#" + str(self.current_token[2]) + " : syntax error, illegal " + str(self.current_token[0]))
        else:
            self.errors.append(
                "#" + str(self.current_token[2]) + " : syntax error, illegal " + str(self.current_token[1]))

    def advance_forward(self, path, first_set: set):
        if isinstance(
                path[0], NonTerminal
        ) and ((
                       self.current_token[0] in path[0].first_set or self.current_token[1] in path[0].first_set
               ) or (
                       'ε' in first_set and (
                       self.current_token[0] in path[0].follow_set or self.current_token[1] in path[0].follow_set
               )
               )):
            self.advance_forward_path(path)
            return True
        elif isinstance(path[0], str) and (path[0] in self.current_token):
            self.advance_forward_path(path)
            return True
        else:
            return False

    def advance_forward_path(self, path):
        for transition in path:
            if isinstance(transition, NonTerminal):
                self.current_token = NodeParser(
                    transition,
                    self.current_token,
                    self.scanner,
                    parent=self,
                    errors=self.errors
                ).parse()
            else:
                if transition in ['ID', 'NUM'] and transition == self.current_token[0]:
                    Node("(" + self.current_token[0] + ", " + str(self.current_token[1]) + ")", parent=self)
                    self.current_token = self.scanner.get_next_token()
                elif self.current_token[1] == transition:
                    Node("(" + self.current_token[0] + ", " + str(self.current_token[1]) + ")", parent=self)
                    self.current_token = self.scanner.get_next_token()
                elif self.current_token[0] == '$':
                    if self._unexpected_eof():
                        self._create_unexpected_eof_err()
                    return
                else:
                    self.errors.append(
                        "#" + str(self.current_token[2]) + " : syntax error, missing " + transition
                    )

    def _create_unexpected_eof_err(self):
        self.errors.append("#" + str(self.current_token[2]) + " : syntax error, Unexpected EOF")
