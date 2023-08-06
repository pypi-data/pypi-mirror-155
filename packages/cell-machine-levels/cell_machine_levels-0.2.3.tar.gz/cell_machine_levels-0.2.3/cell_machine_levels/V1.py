"""The level parser for V1 levels."""

from .level import Level, LevelParsingError, Cell
import re


def open(level_code: str) -> Level:
    if re.match(
        r"^V1;\d+;\d+;(\d\.\d,?)*;([0-8]\.[0-3]\.\d+\.\d+,?)*;[\w\d]*;[0-3]?$",
        level_code,
    ):
        level_list = level_code.split(";")
        level = Level(
            int(level_list[1]),
            int(level_list[2]),
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
    else:
        raise LevelParsingError("Invalid V1 level code.")


def save(level: Level) -> str:
    # Loop through the level and save it to 2 lists which are used in the V1 level code
    placeable = []
    cells = []
    for x, y, cell, place in level:
        if place:
            placeable.append(f"{x}.{y}")

        if cell.type != 0:
            cells.append(f"{int(cell.type)}.{int(cell.rotation)}.{x}.{y}")

    return f"V1;{level.width};{level.height};{';'.join(placeable)};{';'.join(cells)};{level.name};{int(level.wall_effect)}"
