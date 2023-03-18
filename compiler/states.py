from .validators import is_digit, is_letter, is_whitespace


class States:
    INITIALIZE = 0
    DIGIT_DETECTED = 1
    DIGIT_FINISHED = 2
    INVALID_NUMBER = -2
    WHITE_SPACE = 16


ACCEPT_STATES = [States.DIGIT_FINISHED, States.WHITE_SPACE]
ERROR_STATES = [States.INVALID_NUMBER, ]

TOKEN_NAMES = {
    States.DIGIT_FINISHED: "NUM",
    States.DIGIT_DETECTED: "NUM",
    States.INVALID_NUMBER: "Invalid number",
    States.WHITE_SPACE: "white space"
}
transitions = {
    States.INITIALIZE: [
        (is_digit, States.DIGIT_DETECTED),
        (is_whitespace, States.WHITE_SPACE)
    ],
    States.DIGIT_DETECTED: [
        (is_digit, States.DIGIT_DETECTED),
        (is_letter, States.INVALID_NUMBER)
    ],
    States.WHITE_SPACE: []
}
