import random

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def generate_random_letter(alphabet: str) -> str:
    """
    Generates random letter from alphabet
    :param alphabet: string representing full alphabet
    :return: one random letter from the alphabet
    """
    index = random.randint(0, len(alphabet) - 1)
    letter = alphabet[index]
    return letter


def create_password(alphabet: str, length: int) -> str:
    """
    Creates a password of specified length using letters from ALPHABET
    :param alphabet: string representing full alphabet
    :param length: length of password - an integer > 0
    :return: a password of specified length using letters from ALPHABET
    """
    assert (length > 0)
    password = ""
    for i in range(length):
        letter = generate_random_letter(alphabet)
        password = password + letter
    return password
