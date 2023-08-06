"""The level parser for V3 levels."""

import re
from typing import Tuple
from .level import Level, Cell, CellEnum
from .level import LevelParsingError, LevelTooBigError
from .base74 import b74_decode, b74_encode


def open(level_code: str, max_size: Tuple[int, int] = (0, 0)) -> Level:
    """Use level.open, that's how to open a level."""
    if re.match(
        r"^V3;[\da-zA-Z!$%&+-.=?^{}]+;[\da-zA-Z!$%&+-.=?^{}]+;[\da-zA-Z!$%&+-.=?^{}()]*;[\w\d]*;[\w\d]*;[0-3]?$",
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

        level_cells = ""
        data = level_list[3]
        data_index = 0
        while data_index < len(data):
            if data[data_index] == "(" or data[data_index] == ")":
                if data[data_index] == ")":
                    offset = data[data_index + 1]
                    distance = data[data_index + 2]
                    data_index += 3

                else:
                    offset = ""
                    data_index += 1
                    while data[data_index] != "(" and data[data_index] != ")":
                        offset += data[data_index]
                        data_index += 1
                    if data[data_index] == ")":
                        distance = data[data_index + 1]
                        data_index += 2
                    else:
                        distance = ""
                        data_index += 1
                        while data[data_index] != ")":
                            distance += data[data_index]
                            data_index += 1
                        data_index += 1

                for _ in range(b74_decode(distance)):
                    level_cells += level_cells[-b74_decode(offset) - 1]

            else:
                level_cells += data[data_index]
                data_index += 1

        for i, j in enumerate(level_cells):
            cell_num = b74_decode(j)
            if cell_num > 71:
                level[i % width, i // height] = cell_num % 2 == 1
            else:
                level[i % width, i // height] = (
                    Cell(cell_num // 2 % 9, cell_num // 18 % 4),
                    cell_num % 2 == 1,
                )

        return level

    raise LevelParsingError("Invalid V3 level code.")


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

    max_match_offset = 0
    data_index = 0

    while data_index < len(level_string):
        max_match_length = 0
        for match_offset in range(1, data_index + 1):
            match_length = 0
            while (
                data_index + match_length < len(level_string)
                and level_string[data_index + match_length]
                == level_string[data_index + match_length - match_offset]
            ):
                match_length += 1
                if match_length > max_match_length:
                    max_match_length = match_length
                    max_match_offset = match_offset - 1

        if max_match_length > 3:
            if len(b74_encode(max_match_length)) == 1:
                if len(b74_encode(max_match_offset)) == 1:
                    if max_match_length > 3:
                        result_level_string += (
                            ")"
                            + b74_encode(max_match_offset)
                            + b74_encode(max_match_length)
                        )
                        data_index += max_match_length - 1
                    else:
                        result_level_string += level_string[data_index]
                else:
                    if max_match_length > 3 + len(b74_encode(max_match_offset)):
                        result_level_string += (
                            "("
                            + b74_encode(max_match_offset)
                            + ")"
                            + b74_encode(max_match_length)
                        )
                        data_index += max_match_length - 1
                    else:
                        result_level_string += level_string[data_index]
            else:
                result_level_string += (
                    "("
                    + b74_encode(max_match_offset)
                    + "("
                    + b74_encode(max_match_length)
                    + ")"
                )
                data_index += max_match_length - 1
        else:
            result_level_string += level_string[data_index]

        max_match_length = 0
        data_index += 1

    return f"V3;{b74_encode(level.width)};{b74_encode(level.height)};{result_level_string};{level.tutorial_text};{level.name};{int(level.wall_effect)}"
