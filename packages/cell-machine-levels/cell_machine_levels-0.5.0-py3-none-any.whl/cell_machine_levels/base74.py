"""This module is used in V2 and V3 encoding, maybe some others too."""

b74_key = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&+-.=?^{}"


def b74_decode(chars: str, /) -> int:
    """Decode base 74 number to regular integer.

    Args:
        chars (string): The base 74 number to decode.

    Returns:
        integer: The decoded number.
    """
    result = 0

    for char in chars:
        result *= 74
        if (b74_char := b74_key.find(char)) == -1:
            raise ValueError(f"Invalid character in base 74 number: {char}")
        else:
            result = result + b74_char

    return result


def b74_encode(num: int, /) -> str:
    """Encode regular positive integer to base 74 number.

    Args:
        num (integer): The number to encode.

    Returns:
        string: The base 74 number.
    """
    if num < 10:
        return str(num)

    result = ""
    counter = 0

    while num >= (74**counter):
        result += b74_key[num // (74**counter) % 74]
        counter += 1

    return result
