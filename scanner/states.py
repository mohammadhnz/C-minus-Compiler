from .validators import is_digit, is_letter, is_whitespace, is_letter_or_digit, is_invalid, is_symbol, is_equal_sign, \
    is_slash, is_star


class States:
    INITIALIZE = 0
    DIGIT_DETECTED = 1
    DIGIT_FINISHED = 2
    ID_DETECTED = 3
    ID_FINISHED = 4
    SYMBOL_DETECTED = 5
    SINGLE_EQUAL_SIGN = 6
    DOUBLE_EQUAL_SIGN = 7
    SLASH_DETECTED = 8
    COMMENT_OPENING = 9
    COMMENT_CLOSING_STAR_DETECTED = 10
    COMMENT_CLOSED = 11
    SINGLE_STAR_DETECTED = 12
    UNMATCHED_COMMENT = 13
    INVALID_NUMBER = -2
    INVALID_INPUT = -3
    WHITE_SPACE = 16
    KEYWORD = 17


ACCEPT_STATES = [
    States.DIGIT_FINISHED,
    States.WHITE_SPACE,
    States.SYMBOL_DETECTED,
    States.DOUBLE_EQUAL_SIGN,
    States.SYMBOL_DETECTED,
    States.COMMENT_CLOSED
]
ERROR_STATES = [
    States.INVALID_NUMBER,
    States.INVALID_INPUT,
    States.UNMATCHED_COMMENT
]

TOKEN_NAMES = {
    States.DIGIT_FINISHED: "NUM",
    States.DIGIT_DETECTED: "NUM",
    States.ID_DETECTED: "ID",
    States.ID_FINISHED: "ID",
    States.SYMBOL_DETECTED: "SYMBOL",
    States.SINGLE_EQUAL_SIGN: "SYMBOL",
    States.DOUBLE_EQUAL_SIGN: "SYMBOL",
    States.KEYWORD: "KEYWORD",
    States.COMMENT_CLOSED: "COMMENT",
    States.SINGLE_STAR_DETECTED: "SYMBOL",
    States.COMMENT_OPENING: "Unclosed comment",
    States.COMMENT_CLOSING_STAR_DETECTED: "Unclosed comment",
    States.SLASH_DETECTED: "Invalid input",
    States.UNMATCHED_COMMENT: "Unmatched comment",
    States.INVALID_NUMBER: "Invalid number",
    States.INVALID_INPUT: "Invalid input",
    States.WHITE_SPACE: "white space"
}
transitions = {
    States.INITIALIZE: [
        (is_digit, States.DIGIT_DETECTED),
        (is_whitespace, States.WHITE_SPACE),
        (is_letter, States.ID_DETECTED),
        (is_symbol, States.SYMBOL_DETECTED),
        (is_equal_sign, States.SINGLE_EQUAL_SIGN),
        (is_slash, States.SLASH_DETECTED),
        (is_star, States.SINGLE_STAR_DETECTED),
        (is_invalid, States.INVALID_INPUT),
    ],
    States.DIGIT_DETECTED: [
        (is_digit, States.DIGIT_DETECTED),
        (is_letter, States.INVALID_NUMBER),
        (is_invalid, States.INVALID_INPUT)
    ],
    States.ID_DETECTED: [
        (is_letter_or_digit, States.ID_DETECTED),
        (is_invalid, States.INVALID_INPUT),
    ],
    States.SINGLE_EQUAL_SIGN: [
        (is_equal_sign, States.DOUBLE_EQUAL_SIGN),
        (is_invalid, States.INVALID_INPUT)
    ],
    States.SLASH_DETECTED: [
        (is_star, States.COMMENT_OPENING),
        (is_invalid, States.INVALID_INPUT)
    ],
    States.COMMENT_OPENING: [
        (is_star, States.COMMENT_CLOSING_STAR_DETECTED),
        (lambda x: not is_star(x), States.COMMENT_OPENING)
    ],
    States.COMMENT_CLOSING_STAR_DETECTED: [
        (is_slash, States.COMMENT_CLOSED),
        (lambda x: not is_slash(x), States.COMMENT_OPENING),
    ],
    States.SINGLE_STAR_DETECTED: [
        (is_slash, States.UNMATCHED_COMMENT),
        (is_invalid, States.INVALID_INPUT)
    ],
    States.WHITE_SPACE: [],
    States.SYMBOL_DETECTED: [],
}
