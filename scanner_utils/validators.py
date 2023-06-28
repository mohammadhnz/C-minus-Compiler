def is_digit(character: str):
    return ord('9') >= ord(character) >= ord('0')


def is_letter(character: str):
    return character.isalpha()


def is_whitespace(character: str):
    return ord(character) in [32, 10, 13, 9, 11, 12]


def is_letter_or_digit(character: str):
    return is_letter(character) or is_digit(character)


def is_symbol(character: str):
    return character in [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "<"]


def is_star(character: str):
    return character == '*'


def is_slash(character: str):
    return character == '/'


def is_equal_sign(character: str):
    return character == "="


def is_invalid(character: str):
    return not (
            is_letter_or_digit(character) or
            is_whitespace(character) or
            is_symbol(character) or
            is_equal_sign(character) or
            is_slash(character) or
            is_star(character)
    )
