from parser.states import NonTerminal, states
from scanner.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.current_state = None

    def parse(self):
        first_token = self.scanner.get_next_token()
        program = states["Program"]
        NodeParser(program, first_token, self.scanner).parse()


class NodeParser:

    def __init__(self, node: NonTerminal, current_token, scanner, depth=0):
        self.node: NonTerminal = node
        self.current_token = current_token
        self.scanner = scanner
        self.depth = depth

    def parse(self):
        print(self.node.name)
        for path in self.node.transition_diagram.paths:
            if self.advance_forward(path):
                return

        if self.node.transition_diagram.epsilon:
            return
        else:
            pass
            #TODO: Handle Panic Mode

    def advance_forward(self, path):
        if isinstance(
                path[0], NonTerminal
        ) and (
                self.current_token[0] in path[0].first_set or self.current_token[1] in path[0].first_set
        ):
            self.advance_forward_path(path)
        elif isinstance(path[0], str) and (path[0] in self.current_token):
            self.advance_forward_path(path)
            return True
        else:
            return False

    def advance_forward_path(self, path):
        for transition in path:
            if isinstance(transition, NonTerminal):
                NodeParser(transition, self.current_token, self.scanner).parse()
                self.current_token = self.scanner.get_next_token()
                return True
            else:
                pass
