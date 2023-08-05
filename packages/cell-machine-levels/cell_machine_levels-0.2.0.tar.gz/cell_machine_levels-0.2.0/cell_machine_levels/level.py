from enum import IntEnum
from . import _plugins
import importlib


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


class Rotations(IntEnum):
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
    def __init__(self, type: CellEnum = 0, rotation: Rotations = 0) -> None:
        self.type = type
        self.rotation = rotation

    def rotate_left(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    def rotate_right(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def __str__(self) -> str:
        return f"{self.type}:{self.rotation}"

    __repr__ = __str__

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cell):
            return self.type == other.type and self.rotation == other.rotation
        elif isinstance(other, int):
            return self.type == other
        elif isinstance(other, tuple[int, int]) or isinstance(other, list[int, int]):
            return self.type == other[0] and self.rotation == other[1]
        elif isinstance(other, str):
            return str(self) == other
        else:
            raise TypeError(f"Cannot compare Cell to {type(other)}")


class Level:
    """The main class for levels. You can use this class to create levels and to parse level codes."""

    def __init__(
        self, width: int, height: int, name: str = "", wall_effect: WallEffect = 0
    ) -> None:
        self._size = (width, height)
        self.cell_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.place_grid = [[False for _ in range(width)] for _ in range(height)]
        self.name = name
        self.wall_effect = wall_effect

    def optimized(self) -> "Level":
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
                result[x, y, False] = Cell(cell.type, 0)
            elif cell.type == CellEnum.slide:
                result[x, y, False] = Cell(cell.type, cell.rotation % 2)
            else:
                result[x, y, False] = cell

            result[x, y, True] = place

        return result

    def optimize(self) -> None:
        self = self.optimized()

    # Saving the level

    def save(self, format: str, v4: bool = True) -> str:
        if format in _plugins:
            return importlib.import_module(f".{format}", "cell_machine_levels").save(
                self, v4=v4
            )
        else:
            raise ValueError(f"The format {format} is not supported or doesn't exist.")

    # Iterable methods

    def __iter__(self) -> "Level":
        self._pos = [0, 0]
        return self

    def __next__(self) -> tuple[int, int, Cell, bool]:
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
        else:
            raise StopIteration

    # Getters and setters

    def __getitem__(self, pos: tuple[int, int, bool]) -> Cell:
        if pos[2]:
            return self.place_grid[pos[1]][pos[0]]
        else:
            return self.cell_grid[pos[1]][pos[0]]

    def __setitem__(self, pos: tuple[int, int, bool], value: Cell) -> None:
        if pos[2]:
            self.place_grid[pos[1]][pos[0]] = value
        else:
            self.cell_grid[pos[1]][pos[0]] = value

    # Getting size

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    # Comparisons

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Level):
            return (
                self.cell_grid == other.cell_grid
                and self.place_grid == other.place_grid
                and self.name == other.name
                and self.wall_effect == other.wall_effect
            )
        elif isinstance(other, str):
            try:
                return (
                    self.save(other.split(";")[0], bool(other.split(";")[-1])) == other
                )
            except ValueError:
                raise ValueError(
                    f"The format {(f := other.split(';')[0])[:10] + '...' if len(f) > 10 else f} is not supported or doesn't exist."
                )
        elif isinstance(other, list):
            return self.cell_grid == other
        else:
            raise TypeError(f"Cannot compare Level with {type(other)}")


class LevelParsingError(Exception):
    pass


def open(level_code: str, v4: bool = True) -> Level:
    for plugin in _plugins:
        if level_code.startswith(plugin + ";"):
            return importlib.import_module(f".{plugin}", "cell_machine_levels").open(
                level_code, v4=v4
            )
