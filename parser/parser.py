from anytree import NodeMixin, RenderTree, Node

from parser.states import NonTerminal, states
from scanner.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_state = None

    def parse(self):
        first_token = self.scanner.get_next_token()
        program = states["Program"]
        root = NodeParser(program, first_token, self.scanner)
        root.parse()
        Node("$", parent=root)
        final_result = ""
        for pre, fill, node in RenderTree(root):
            final_result += "%s%s" % (pre, node.name) + '\n'
        with open('parse_tree.txt', 'w') as file:
            file.write(final_result[:-1])
        with open('syntax_errors.txt', 'w') as file:
            file.write("There is no syntax error.")


class NodeParser(NodeMixin):

    def __init__(self, node: NonTerminal, current_token, scanner, parent=None):
        self.node: NonTerminal = node
        self.name = node.name
        self.current_token = current_token
        self.scanner = scanner
        self.parent = parent

    def parse(self):
        for path in self.node.transition_diagram.paths:
            if self.advance_forward(path):
                return self.current_token
        if self.node.transition_diagram.epsilon:
            Node("epsilon", parent=self)
            return self.current_token
        else:
            raise Exception()
            # TODO: Handle Panic Mode

    def advance_forward(self, path):
        if isinstance(
                path[0], NonTerminal
        ) and ((
                       self.current_token[0] in path[0].first_set or self.current_token[1] in path[0].first_set
               ) or (
                       'ε' in path[0].first_set
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
                self.current_token = NodeParser(transition, self.current_token, self.scanner, parent=self).parse()
            else:
                if transition in ['ID', 'NUM'] and transition == self.current_token[0]:
                    Node("(" + self.current_token[0] + ", " + str(self.current_token[1]) + ")", parent=self)
                    self.current_token = self.scanner.get_next_token()
                elif self.current_token[1] == transition:
                    Node("(" + self.current_token[0] + ", " + str(self.current_token[1]) + ")", parent=self)
                    self.current_token = self.scanner.get_next_token()
