"""This module contains the level class and the cell class."""

import importlib
from enum import IntEnum
from typing import Tuple, Union
from . import _plugins


class CellEnum(IntEnum):
    """The enum used for cell types in the Cell class."""

    generator = 0
    spinner_right = 1
    spinner_left = 2
    mover = 3
    slide = 4
    push = 5
    immobile = 6
    immovable = immobile
    enemy = 7
    trash = 8
    bg = 9


class Rotation(IntEnum):
    """The enum used for rotations in the Cell class."""

    right = 0
    down = 1
    left = 2
    up = 3


class WallEffect(IntEnum):
    """The Mystic Mod V4 wall effect enum."""

    stop = 0
    wrap = 1
    delete = 2
    flip = 3


class Cell:
    """The class used for cells in the Level class."""

    def __init__(
        self, type: CellEnum = CellEnum.bg, rotation: Rotation = Rotation.right
    ) -> None:
        self.type = type
        self._rotation = rotation if type != CellEnum.bg else Rotation.right

    def rotate_left(self) -> None:
        """Rotate the cell left."""
        self.rotation = (self.rotation - 1) % 4

    def rotate_right(self) -> None:
        """Rotate the cell right."""
        self.rotation = (self.rotation + 1) % 4

    def __str__(self) -> str:
        return f"{self.type}:{self.rotation}"

    __repr__ = __str__

    @property
    def rotation(self) -> Rotation:
        """Get the rotation of the cell.

        Returns:
            Rotation: The rotation of the cell."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: Rotation) -> None:
        """Set the rotation of the cell.

        Args:
            value (Rotation): The rotation to set the cell to."""
        if self.type != CellEnum.bg:
            self._rotation = value % 4

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.type == other.type and self.rotation == other.rotation
        if isinstance(other, int):
            return self.type == other
        if isinstance(other, (tuple, list)):
            if len(other) == 2:
                return self.type == other[0] and self.rotation == other[1]
            raise TypeError(
                f"Cannot compare Cell to {type(other)} with length {len(other)}."
            )
        if isinstance(other, str):
            return str(self) == other
        raise TypeError(f"Cannot compare Cell to {type(other)}.")


class Level:
    """The main class for levels. You can use this class to create levels
    and to parse level codes."""

    def __init__(
        self,
        width: int,
        height: int,
        tutorial_text: str = "",
        name: str = "",
        wall_effect: WallEffect = 0,
    ) -> None:
        self._size = (width, height)
        self.cell_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.place_grid = [[False for _ in range(width)] for _ in range(height)]
        self.tutorial_text = tutorial_text
        self.name = name
        self.wall_effect = wall_effect
        self._pos = None  # Cause pylint is complaining

    def optimized(self) -> "Level":
        """Optimize the level.

        Returns:
            Level: The optimized level."""
        result = Level(self.width, self.height, self.name, self.wall_effect)

        for x, y, cell, place in self:
            if cell.type in (
                CellEnum.enemy,
                CellEnum.immobile,
                CellEnum.push,
                CellEnum.trash,
                CellEnum.spinner_left,
                CellEnum.spinner_right,
            ):
                result[x, y] = Cell(cell.type, 0)
            elif cell.type == CellEnum.slide:
                result[x, y] = Cell(cell.type, cell.rotation % 2)
            else:
                result[x, y] = cell

            result[x, y] = place

        return result

    def optimize(self) -> None:
        """Optimize this level without returning anything."""
        self.cell_grid = self.optimized().cell_grid

    def __str__(self) -> str:
        output = [[] for _ in range(self.height)]

        for _, y, cell, place in self:
            output[y].append(f"{cell},{place}")

        return str(output)

    __repr__ = __str__

    # Saving the level

    def save(self, format: str) -> str:
        """Save the level to a level code of the given format.

        Args:
            format (str): The format to save the level in.

        Returns:
            str: The level code."""
        if format in _plugins:
            return importlib.import_module(f".{format}", "cell_machine_levels").save(
                self
            )
        raise ValueError(f"The format {format} is not supported or doesn't exist.")

    # Iterable methods

    def __iter__(self) -> "Level":
        self._pos = [0, 0]
        return self

    def __next__(self) -> Tuple[int, int, Cell, bool]:
        if self._pos[1] < self.height:
            ret = (
                self._pos[0],
                self._pos[1],
                self.cell_grid[self._pos[1]][self._pos[0]],
                self.place_grid[self._pos[1]][self._pos[0]],
            )
            self._pos[0] += 1
            if self._pos[0] >= self.width:
                self._pos = [0, self._pos[1] + 1]
            return ret
        raise StopIteration

    # Getters and setters

    def __getitem__(self, pos: Tuple[int, int, bool]) -> Union[Cell, bool]:
        if pos[2]:
            return self.place_grid[pos[1]][pos[0]]
        return self.cell_grid[pos[1]][pos[0]]

    def __setitem__(
        self, pos: Tuple[int, int], value: Union[Cell, bool, Tuple[Cell, bool]]
    ) -> None:
        if isinstance(value, bool):
            self.place_grid[pos[1]][pos[0]] = value
        elif isinstance(value, Cell):
            self.cell_grid[pos[1]][pos[0]] = value
        elif isinstance(value, tuple):
            if len(value) == 2:
                self.cell_grid[pos[1]][pos[0]] = value[0]
                self.place_grid[pos[1]][pos[0]] = value[1]
            else:
                raise ValueError(
                    f"Value has to be a tuple of length 2 being (Cell, bool), not {len(value)}"
                )
        else:
            raise ValueError(f"Invalid value type {type(value)}")

    # Getting size

    @property
    def size(self):
        """Tuple[int, int]: The size of the level."""
        return self._size

    @property
    def width(self):
        """int: The width of the level."""
        return self._size[0]

    @property
    def height(self):
        """int: The height of the level."""
        return self._size[1]

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Level):
            return (
                self.cell_grid == other.cell_grid
                and self.place_grid == other.place_grid
                and self.tutorial_text == other.tutorial_text
                and self.name == other.name
                and self.wall_effect == other.wall_effect
            )
        if isinstance(other, str):
            try:
                return self.save(other.split(";")[0]) == other
            except ValueError as ex:
                form = other.split(";")[0]
                raise ValueError(
                    f"The format {form[:10] + '...' if len(form) > 10 else form} is not supported or doesn't exist."
                ) from ex
        if isinstance(other, list):
            return self.cell_grid == other
        raise TypeError(f"Cannot compare Level with {type(other)}")


def open(level_code: str, max_size: Tuple[int, int] = (0, 0)) -> Level:
    """Open a level from a level code.

    Args:
        level_code (str): The level code.
        max_size (Tuple[int, int]): The maximum size of the level.

    Returns:
        Level: The level.

    Raises:
        LevelParseError: If the level code is invalid.
        LevelTooBigError: If the level is bigger than the given max size."""
    for plugin in _plugins:
        if level_code.startswith(plugin + ";"):
            return importlib.import_module(f".{plugin}", "cell_machine_levels").open(
                level_code,
                max_size,
            )
    raise LevelParsingError(
        f"The format {level_code.split(';')[0]} is not supported or doesn't exist."
    )


# Exceptions


class LevelParsingError(Exception):
    """Exception raised when parsing a level fails."""


class LevelTooBigError(Exception):
    """Exception raised when a level is bigger than the given max size."""
