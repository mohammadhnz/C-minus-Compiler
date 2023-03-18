def is_digit(character: str):
    return ord('9') >= ord(character) >= ord('0')


def is_letter(character: str):
    return character.isalpha()


def is_whitespace(character: str):
    return ord(character) in [32, 10, 13, 9, 11, 12]
