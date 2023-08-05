"""The level parser for V1 levels."""

from .level import Level, LevelParsingError, Cell
import re


def open(level_code: str, v4: bool = True) -> Level:
    if re.match(
        r"^V1;\d+;\d+;(\d\.\d,?)*;([0-8]\.[0-3]\.\d+\.\d+,?)*;[\w\d]*;[0-3]?$",
        level_code,
    ):
        level_code = level_code.split(";")
        level = Level(
            int(level_code[1]),
            int(level_code[2]),
            level_code[5],
            int(level_code[6]) if v4 else 0,
        )

        # Loop through all the placeable cells and set them to True
        for i in level_code[3].split(","):
            x, y = i.split(".")
            level[int(x), level.height - int(y) - 1, True] = True

        # Loop through all the cells and set them
        for i in level_code[4].split(","):
            type, rotation, x, y = i.split(".")
            level[int(x), level.height - int(y) - 1, False] = Cell(
                int(type), int(rotation)
            )

        return level
    else:
        raise LevelParsingError("Invalid V1 level code.")


def save(level: Level, v4: bool = True) -> str:
    # Loop through the level and save it to 2 lists which are used in the V1 level code
    placeable = []
    cells = []
    for x, y, cell, place in level:
        if place:
            placeable.append(f"{x}.{level.height - y - 1}")

        if cell.type != 0:
            cells.append(
                f"{int(cell.type)}.{int(cell.rotation)}.{x}.{level.height - y - 1}"
            )

    return f"V1;{level.width};{level.height};{';'.join(placeable)};{';'.join(cells)};{level.name};{int(level.wall_effect) if v4 else ''}"
