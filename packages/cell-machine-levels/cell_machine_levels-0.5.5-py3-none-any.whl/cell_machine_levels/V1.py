"""The level parser for V1 levels."""

import re
from typing import Tuple
from .level import Level, Cell, CellEnum
from .level import LevelParsingError, LevelTooBigError


def open(level_code: str, max_size: Tuple[int, int] = (0, 0)) -> Level:
    """Use level.open, that's how to open a level."""
    if re.match(
        r"^V1;\d+;\d+;(\d\.\d,?)*;([0-8]\.[0-3]\.\d+\.\d+,?)*;[\w\d]*;[0-3]?$",
        level_code,
    ):
        level_list = level_code.split(";")

        width, height = int(level_list[1]), int(level_list[2])

        if max_size[0] > 0 or max_size[1] > 0:
            if width > max_size[0] or height > max_size[1]:
                raise LevelTooBigError(
                    f"Level is too big. Max size is {max_size[0]}x{max_size[1]}."
                )

        level = Level(
            width,
            height,
            "",
            level_list[5],
            int(level_list[6]) if level_list[6] != "" else 0,
        )

        # Loop through all the placeable cells and set them to True
        for i in level_list[3].split(","):
            x, y = i.split(".")
            level[int(x), int(y)] = True

        # Loop through all the cells and set them
        for i in level_list[4].split(","):
            type, rotation, x, y = i.split(".")
            level[int(x), int(y)] = Cell(int(type), int(rotation))

        return level

    raise LevelParsingError("Invalid V1 level code.")


def save(level: Level) -> str:
    """Use level.Level.save, that's how to save a level."""
    # Loop through the level and save it to 2 lists which are used in the V1 level code
    placeable = []
    cells = []
    for x, y, cell, place in level:
        if place:
            placeable.append(f"{x}.{y}")

        if cell.type != CellEnum.bg:
            cells.append(f"{int(cell.type)}.{int(cell.rotation)}.{x}.{y}")

    return f"V1;{level.width};{level.height};{','.join(placeable)};{','.join(cells)};{level.name};{int(level.wall_effect)}"
