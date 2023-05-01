import json
from typing import List

grammer = """
Program⟶  Declaration_list
Declaration_list⟶  Declaration Declaration_list
Declaration_list⟶  EPSILON
Declaration⟶  Declaration_initial Declaration_prime
Declaration_initial⟶  Type_specifier ID
Declaration_prime⟶  Fun_declaration_prime
Declaration_prime⟶  Var_declaration_prime
Var_declaration_prime⟶  ;
Var_declaration_prime⟶  [ NUM ] ;
Fun_declaration_prime⟶  ( Params ) Compound_stmt
Type_specifier⟶  int
Type_specifier⟶  void
Params⟶  int ID Param_prime Param_list
Params⟶  void
Param_list⟶  , Param Param_list
Param_list⟶  EPSILON
Param⟶  Declaration_initial Param_prime
Param_prime⟶  [ ]
Param_prime⟶  EPSILON
Compound_stmt⟶  { Declaration_list Statement_list }
Statement_list⟶  Statement Statement_list
Statement_list⟶  EPSILON
Statement⟶  Expression_stmt
Statement⟶  Compound_stmt
Statement⟶  Selection_stmt
Statement⟶  Iteration_stmt
Statement⟶  Return_stmt
Expression_stmt⟶  Expression ;
Expression_stmt⟶  break ;
Expression_stmt⟶  ;
Selection_stmt⟶  if ( Expression ) Statement else Statement
Iteration_stmt⟶  repeat Statement until ( Expression )
Return_stmt⟶  return Return_stmt_prime
Return_stmt_prime⟶  ;
Return_stmt_prime⟶  Expression ;
Expression⟶  Simple_expression_zegond
Expression⟶  ID B
B⟶  = Expression
B⟶  [ Expression ] H
B⟶  Simple_expression_prime
H⟶  = Expression
H⟶  G D C
Simple_expression_zegond⟶  Additive_expression_zegond C
Simple_expression_prime⟶  Additive_expression_prime C
C⟶  Relop Additive_expression
C⟶  EPSILON
Relop⟶  <
Relop⟶  ==
Additive_expression⟶  Term D
Additive_expression_prime⟶  Term_prime D
Additive_expression_zegond⟶  Term_zegond D
D⟶  Addop Term D
D⟶  EPSILON
Addop⟶  +
Addop⟶  -
Term⟶  Factor G
Term_prime⟶  Factor_prime G
Term_zegond⟶  Factor_zegond G
G⟶  * Factor G
G⟶  EPSILON
Factor⟶  ( Expression )
Factor⟶  ID Var_call_prime
Factor⟶  NUM
Var_call_prime⟶  ( Args )
Var_call_prime⟶  Var_prime
Var_prime⟶  [ Expression ]
Var_prime⟶  EPSILON
Factor_prime⟶  ( Args )
Factor_prime⟶  EPSILON
Factor_zegond⟶  ( Expression )
Factor_zegond⟶  NUM
Args⟶  Arg_list
Args⟶  EPSILON
Arg_list⟶  Expression Arg_list_prime
Arg_list_prime⟶  , Expression Arg_list_prime
Arg_list_prime⟶  EPSILON
"""
first_sets = {
    "Program": ["int", "void", "\u03b5"],
    "Declaration_list": ["int", "void", "\u03b5"],
    "Declaration": ["int", "void"], "Declaration_initial": ["int", "void"],
    "Declaration_prime": [";", "[", "("],
    "Var_declaration_prime": [";", "["],
    "Fun_declaration_prime": ["("],
    "Type_specifier": ["int", "void"],
    "Params": ["int", "void"],
    "Param_list": [",", "\u03b5"],
    "Param": ["int", "void"],
    "Param_prime": ["[", "\u03b5"],
    "Compound_stmt": ["{"],
    "Statement_list": ["ID", ";", "NUM", "(", "{", "break", "if", "repeat", "return", "\u03b5"],
    "Statement": ["ID", ";", "NUM", "(", "{", "break", "if", "repeat", "return"],
    "Expression_stmt": ["ID", ";", "NUM", "(", "break"],
    "Selection_stmt": ["if"],
    "Iteration_stmt": ["repeat"],
    "Return_stmt": ["return"],
    "Return_stmt_prime": ["ID", ";", "NUM", "("],
    "Expression": ["ID", "NUM", "("],
    "B": ["[", "(", "=", "<", "==", "+", "-", "*", "\u03b5"],
    "H": ["=", "<", "==", "+", "-", "*", "\u03b5"],
    "Simple_expression_zegond": ["NUM", "("],
    "Simple_expression_prime": ["(", "<", "==", "+", "-", "*", "\u03b5"],
    "C": ["<", "==", "\u03b5"],
    "Relop": ["<", "=="],
    "Additive_expression": ["ID", "NUM", "("],
    "Additive_expression_prime": ["(", "+", "-", "*", "\u03b5"],
    "Additive_expression_zegond": ["NUM", "("],
    "D": ["+", "-", "\u03b5"],
    "Addop": ["+", "-"],
    "Term": ["ID", "NUM", "("],
    "Term_prime": ["(", "*", "\u03b5"],
    "Term_zegond": ["NUM", "("],
    "G": ["*", "\u03b5"],
    "Factor": ["ID", "NUM", "("],
    "Var_call_prime": ["[", "(", "\u03b5"],
    "Var_prime": ["[", "\u03b5"],
    "Factor_prime": ["(", "\u03b5"],
    "Factor_zegond": ["NUM", "("],
    "Args": ["ID", "NUM", "(", "\u03b5"],
    "Arg_list": ["ID", "NUM", "("],
    "Arg_list_prime": [",", "\u03b5"]
}

follow_sets = {"Program": ["$"],
               "Declaration_list": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "repeat", "return", "$"],
               "Declaration": ["ID", ";", "NUM", "(", "int", "void", "{", "}", "break", "if", "repeat", "return", "$"],
               "Declaration_initial": [";", "[", "(", ")", ","],
               "Declaration_prime": ["ID", ";", "NUM", "(", "int", "void", "{", "}", "break", "if", "repeat", "return",
                                     "$"],
               "Var_declaration_prime": ["ID", ";", "NUM", "(", "int", "void", "{", "}", "break", "if", "repeat",
                                         "return", "$"],
               "Fun_declaration_prime": ["ID", ";", "NUM", "(", "int", "void", "{", "}", "break", "if", "repeat",
                                         "return", "$"],
               "Type_specifier": ["ID"],
               "Params": [")"],
               "Param_list": [")"],
               "Param": [")", ","],
               "Param_prime": [")", ","],
               "Compound_stmt": ["ID", ";", "NUM", "(", "int", "void", "{", "}", "break", "if", "else", "repeat",
                                 "until", "return", "$"],
               "Statement_list": ["}"],
               "Statement": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until", "return"],
               "Expression_stmt": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until", "return"],
               "Selection_stmt": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until", "return"],
               "Iteration_stmt": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until", "return"],
               "Return_stmt": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until", "return"],
               "Return_stmt_prime": ["ID", ";", "NUM", "(", "{", "}", "break", "if", "else", "repeat", "until",
                                     "return"],
               "Expression": [";", "]", ")", ","],
               "B": [";", "]", ")", ","],
               "H": [";", "]", ")", ","],
               "Simple_expression_zegond": [";", "]", ")", ","],
               "Simple_expression_prime": [";", "]", ")", ","],
               "C": [";", "]", ")", ","],
               "Relop": ["ID", "NUM", "("],
               "Additive_expression": [";", "]", ")", ","],
               "Additive_expression_prime": [";", "]", ")", ",", "<", "=="],
               "Additive_expression_zegond": [";", "]", ")", ",", "<", "=="],
               "D": [";", "]", ")", ",", "<", "=="],
               "Addop": ["ID", "NUM", "("],
               "Term": [";", "]", ")", ",", "<", "==", "+", "-"],
               "Term_prime": [";", "]", ")", ",", "<", "==", "+", "-"],
               "Term_zegond": [";", "]", ")", ",", "<", "==", "+", "-"],
               "G": [";", "]", ")", ",", "<", "==", "+", "-"],
               "Factor": [";", "]", ")", ",", "<", "==", "+", "-", "*"],
               "Var_call_prime": [";", "]", ")", ",", "<", "==", "+", "-", "*"],
               "Var_prime": [";", "]", ")", ",", "<", "==", "+", "-", "*"],
               "Factor_prime": [";", "]", ")", ",", "<", "==", "+", "-", "*"],
               "Factor_zegond": [";", "]", ")", ",", "<", "==", "+", "-", "*"],
               "Args": [")"],
               "Arg_list": [")"],
               "Arg_list_prime": [")"]
               }


class NonTerminal:
    def __init__(self, name: str, first_set, follow_set):
        self.name = name.replace('_', '-')
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
        if "\u03b5" in path or 'EPSILON' in path:
            self.epsilon = True
            return
        self.paths.append(path)


def initialize_states():
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, 'first_sets.json')
    # first_sets = json.load(open(os.path.join(dirname, 'first_sets.json'), "r"))
    # follow_sets = json.load(open(os.path.join(dirname, 'follow_sets.json'), "r"))
    # production_rules = open(os.path.join(dirname, 'grammer.txt'), "r").readlines()
    production_rules = grammer.strip().split("\n")
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
    # for name, state in states.items():
    #     print(state.name)
    #     print("\t", "follow_set: ", state.follow_set)
    #     print("\t", "first_set: ", state.first_set)
    #     print("paths:")
    #     for path in state.transition_diagram.paths:
    #         print("\t", path)
    #     print()
    # print("Success")
    return states


states = initialize_states()
