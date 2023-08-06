"""The level parser for V2 levels."""

import re
from typing import Tuple
from .level import Level, Cell, CellEnum
from .level import LevelParsingError, LevelTooBigError
from .base74 import b74_decode, b74_encode


def open(level_code: str, max_size: Tuple[int, int] = (0, 0)) -> Level:
    """Use level.open, that's how to open a level."""
    if re.match(
        r"^V2;[\da-zA-Z!$%&+-.=?^{}]+;[\da-zA-Z!$%&+-.=?^{}]+;[\da-zA-Z!$%&+-.=?^{}()]*;[\w\d]*;[\w\d]*;[0-3]?$",
        level_code,
    ):
        level_list = level_code.split(";")

        width, height = b74_decode(level_list[1]), b74_decode(level_list[2])

        if max_size[0] > 0 or max_size[1] > 0:
            if width > max_size[0] or height > max_size[1]:
                raise LevelTooBigError(
                    f"Level is too big. Max size is {max_size[0]}x{max_size[1]}."
                )

        level = Level(
            width,
            height,
            level_list[4],
            level_list[5],
            int(level_list[6]) if level_list[6] != "" else 0,
        )

        if level_list[3] == "":
            return level

        level_list[3] += "0"  # To not error when checking for ) or (

        count = pos = 0
        while count < len(level_list[3]) - 1:
            if level_list[3][count + 1] == ")":
                repeat = b74_decode(level_list[3][count + 2]) + 1
                count_add = 3
            elif level_list[3][count + 1] == "(":
                repeat = b74_decode(level_list[3][count + 2 :].split(")")[0]) + 1
                count_add = 3 + len(level_list[3][count + 2 :].split(")")[0])
            else:
                repeat = 1
                count_add = 1

            cell_num = b74_decode(level_list[3][count])
            for i in range(repeat):
                if cell_num > 71:
                    level[(pos + i) % width, (pos + i) // height] = cell_num % 2 == 1
                else:
                    level[(pos + i) % width, (pos + i) // height] = (
                        Cell(cell_num // 2 % 9, cell_num // 18 % 4),
                        cell_num % 2 == 1,
                    )

            count += count_add
            pos += repeat

        return level

    raise LevelParsingError("Invalid V2 level code.")


def save(level: Level) -> str:
    """Use level.Level.save, that's how to save a level."""

    # gen  ror  rol  mov  sli  pus  wal  ene  tra
    # 01   23   45   67   89   ab   cd   ef   gh
    # ij   kl   mn   op   qr   st   uv   wx   yz
    # AB   CD   EF   GH   IJ   KL   MN   OP   QR
    # ST   UV   WX   YZ   !$   %&   +-   .=   ?^

    # bg   place
    # {    }

    level_string = ""
    for _, _, cell, place in level:
        if cell.type == CellEnum.bg:
            level_string += b74_encode(72 + int(place))
        else:
            level_string += b74_encode(cell.type * 2 + cell.rotation * 18 + int(place))

    # Remove the space using bgs at the end of the level
    level_string = re.sub(r"\{+$", "", level_string, 0)

    result_level_string = ""
    repeat = 0
    previous = ""
    for i in level_string:
        if i == previous:
            repeat += 1
        else:
            if repeat < 4:
                result_level_string += previous * repeat
            elif repeat < 74:
                result_level_string += previous + ")" + b74_encode(repeat - 1)
            else:
                result_level_string += previous + "(" + b74_encode(repeat - 1) + ")"
            repeat = 1
            previous = i

    if repeat < 4:
        result_level_string += previous * repeat
    elif repeat < 74:
        result_level_string += previous + ")" + b74_encode(repeat - 1)
    else:
        result_level_string += previous + "(" + b74_encode(repeat - 1) + ")"

    return f"V2;{b74_encode(level.width)};{b74_encode(level.height)};{result_level_string};{level.tutorial_text};{level.name};{int(level.wall_effect)}"
