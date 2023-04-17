import json
from pprint import pprint
from typing import List


class NonTerminal:
    def __init__(self, name, first_set, follow_set):
        self.name = name
        self.follow_set = follow_set
        self.first_set = first_set
        self.transition_diagram = TransitionDiagram()

    def advance_forward(self, token):
        pass

    def __repr__(self):
        return self.name


class TransitionDiagram:
    def __init__(self):
        self.paths = []
        self.epsilon = False

    def add_new_path(self, path: List[NonTerminal | str]):
        if "\u03b5" in path:
            self.epsilon = True
            return
        self.paths.append(path)
def initialize_states():
    first_sets = json.load(open("./static/first_sets.json", "r"))
    follow_sets = json.load(open("./static/follow_sets.json", "r"))
    production_rules = open("./static/grammer.txt", "r").readlines()
    states = dict()
    for key, value in first_sets.items():
        non_terminal = NonTerminal(
            name=key,
            first_set=value,
            follow_set=follow_sets[key]
        )
        states[key] = non_terminal
    for rule in production_rules:
        non_terminal = states[rule.split("⟶")[0].strip()]
        transitions = rule.split("⟶")[1].strip().split()
        transitions = [
            (transition if transition not in states else states[transition])
            for transition in transitions
        ]
        non_terminal.transition_diagram.add_new_path(transitions)
    for name, state in states.items():
        print(state.name)
        print("\t", "follow_set: ", state.follow_set)
        print("\t", "first_set: ", state.first_set)
        print("paths:")
        for path in state.transition_diagram.paths:
            print("\t", path)
        print()
    print("Success")
    return states

states = initialize_states()