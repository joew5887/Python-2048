from __future__ import annotations
from typing import Any, Optional, overload, Union
import random
from copy import deepcopy


DEFAULT_SIZE_X = 4
DEFAULT_SIZE_Y = 4
MOVES = ["u", "d", "l", "r"]
DEFAULT_STARTING_VALUES = [2, 4]
START_TILES_NUM = 2


class NoMoveError(Exception):
    pass


class Tile:
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Tile({self.value})"

    def __eq__(self, other: Any) -> Union[bool, NotImplementedError]:
        if isinstance(other, Tile):
            return self.value == other.value

        raise NotImplementedError

    @overload
    def __add__(self, other: Tile) -> tuple[Tile, Tile]: ...

    @overload
    def __add__(self, other: EmptyTile) -> tuple[EmptyTile, Tile]: ...

    def __add__(self, other: Any) -> NotImplementedError:
        if isinstance(other, EmptyTile):
            return self
            # return (other, self)

        if isinstance(other, Tile):
            if other == self:
                return Tile(other.value + self.value)

            return self
            # return (self, other)

        raise NotImplementedError

        '''if isinstance(other, EmptyTile):
            return (other, self)

        if isinstance(other, Tile):
            if self == other:
                return (EmptyTile(), Tile(self.value + other.value))

            return (self, other)

        raise NotImplementedError'''

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int) -> Optional[Exception]:
        if value < 0:
            raise Exception("Value must be positive.")

        self.__value = value

    def is_empty(self) -> bool:
        return False


class EmptyTile(Tile):
    def __init__(self):
        super().__init__(0)

    def __repr__(self) -> str:
        return "EmptyTile()"

    def __str__(self) -> str:
        return ""

    @overload
    def __add__(self, other: EmptyTile) -> tuple[EmptyTile, EmptyTile]: ...

    @overload
    def __add__(self, other: Tile) -> tuple[EmptyTile, Tile]: ...

    def __add__(self, other: Any) -> NotImplementedError:
        if isinstance(other, EmptyTile):
            return self
            # return (other, self)

        if isinstance(other, Tile):
            return other
            # return (self, other)

        raise NotImplementedError

    def is_empty(self) -> bool:
        return True


class Board:
    def __init__(self, shape: Shape, starting_values: list[int]):
        self.__shape = shape
        self.__starting_values = starting_values
        self.__new_grid()

    def __str__(self) -> str:
        out = []

        for i in range(self.__shape.x):
            row = []

            for j in range(self.__shape.y):
                row.append(str(self[(i, j)]))

            out.append(" ".join(row))

        return "\n".join(out)

    def __repr__(self) -> str:
        out = []

        for i in range(self.__shape.x):
            row = []

            for j in range(self.__shape.y):
                row.append(self[(i, j)])

            out.append(row)

        return str(out)

    @overload
    def __eq__(self, other: Board) -> bool: ...

    def __eq__(self, other: Any) -> NotImplementedError:
        if isinstance(other, Board):
            return self.all_tiles == other.all_tiles

        raise NotImplementedError

    def __getitem__(self, idx: tuple[int, int]) -> Union[EmptyTile, Tile]:
        return self.__grid[idx]

    def __setitem__(self, idx: tuple[int, int], tile: Union[EmptyTile, Tile]):
        self.__grid[idx] = tile

    def __new_grid(self) -> None:
        self.__grid = self.__empty_grid(self.__shape)
        self.add_random_tile(START_TILES_NUM)

    def add_random_tile(self, num_to_add: int) -> None:
        coords_available = [
            coord for coord in self.__grid if self[coord].is_empty()
        ]

        for _ in range(num_to_add):
            coord_chosen = random.choice(coords_available)
            self[coord_chosen] = Tile(random.choice(self.__starting_values))
            coords_available.remove(coord_chosen)

    def __empty_grid(self, shape: Shape) -> dict:
        grid = {}

        for i in range(shape.x):
            for j in range(shape.y):
                grid[(i, j)] = EmptyTile()

        return grid

    def move_horizontal(self, direction: str) -> tuple[Board, int]:
        coords_in_set = []

        for i in range(self.__shape.x):
            row = []

            for j in range(self.__shape.y):
                row.append((i, j))

            if direction == "r":
                row = row[::-1]

            coords_in_set.append(row)

        '''coords_in_set = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(0, 3), (1, 3), (2, 3), (3, 3)]
        ]'''

        return self._move(coords_in_set)

    def move_vertical(self, direction: str) -> tuple[Board, int]:
        coords_in_set = []

        for i in range(self.__shape.x):
            row = []

            for j in range(self.__shape.y):
                row.append((j, i))

            if direction == "d":
                row = row[::-1]

            coords_in_set.append(row)

        '''coords_in_set = [
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(3, 0), (3, 1), (3, 2), (3, 3)]
        ]'''

        return self._move(coords_in_set)

    def _move_row(self, coords: list[tuple[int, int]]) -> Board:
        tiles = [self[coord] for coord in coords if not self[coord].is_empty()]
        num_empty = len(coords) - len(tiles)
        tiles_added = []
        tiles_added: list[Tile]
        score_for_row = 0

        i = 0
        j = 0
        while (i < len(tiles)):
            curr_tile = tiles[i]

            if i + 1 < len(tiles):
                next_tile = tiles[i+1]
            else:
                tiles_added.append(curr_tile)
                break

            tiles_added.append(curr_tile + next_tile)
            if not (tiles_added[j] == curr_tile):
                score_for_row += tiles_added[j].value
                num_empty += 1
                i += 1

            j += 1
            i += 1

        for _ in range(num_empty):
            tiles_added.append(EmptyTile())

        for coord, tile in zip(coords, tiles_added):
            self[coord] = tile

        return self, score_for_row

    def _move(self, coords_rows: list[list[tuple[int, int]]]) -> tuple[Board, int]:
        new = deepcopy(self)
        score_for_move = 0

        for coords in coords_rows:
            new, score = new._move_row(coords)
            score_for_move += score

        if new == self:
            raise NoMoveError

        return new, score_for_move

    @property
    def all_tiles(self) -> list[Union[EmptyTile, Tile]]:
        return list(self.__grid.values())

    @property
    def coords(self) -> list[tuple[int, int]]:
        return list(self.__grid.keys())

    @property
    def empty_tiles(self) -> list[tuple[int, int]]:
        return [
            coord for coord in self.__grid.keys()
            if isinstance(self.__grid[coord], EmptyTile)
        ]


class Shape:
    def __init__(self, size_x: int, size_y: int):
        self.dim = (size_x, size_y)

    def __str__(self) -> str:
        return str(self.dim)

    def __repr__(self) -> str:
        return f"Shape{self.__str__()}"

    @property
    def dim(self) -> tuple[int, int]:
        return self.__dim

    @dim.setter
    def dim(self, dim: tuple[int, int]) -> None:
        self.__dim = dim

    @property
    def x(self) -> int:
        return self.dim[0]

    @property
    def y(self) -> int:
        return self.dim[1]


class State:
    def __init__(self, board: Board, parent: State = None):
        self.__board = board
        self.__parent = parent

    def __str__(self) -> str:
        return str(self.__board)

    def __repr__(self) -> str:
        return f"State({self.__board.__repr__()})"

    def __getitem__(self, idx: tuple[int, int]) -> Union[EmptyTile, Tile]:
        return self.__board[idx]

    def move(self, direction: str) -> Union[tuple[State, int], Exception]:
        if direction not in MOVES:
            raise Exception("Unknown move")

        if direction in ["u", "d"]:
            new_board, score_retrieved = self.__board.move_vertical(direction)
        else:
            new_board, score_retrieved = self.__board.move_horizontal(
                direction)

        new_board.add_random_tile(1)

        return State(new_board, self), score_retrieved

    def no_child_state(self) -> bool:
        for move in MOVES:
            try:
                new_state = self.move(move)
            except NoMoveError:
                continue
            else:
                return False

        return True

    @property
    def coords(self) -> list[tuple[int, int]]:
        return self.__board.coords


class Game:
    def __init__(
        self, size_x: int = DEFAULT_SIZE_X,
        size_y: int = DEFAULT_SIZE_Y,
        starting_values: list[int] = DEFAULT_STARTING_VALUES
    ):

        self.__shape = Shape(size_x, size_y)
        self.__current_state = State(Board(self.shape, starting_values))
        self.score = 0

    def __str__(self) -> str:
        return str(self.state)

    def __repr__(self) -> str:
        return f"Game({self.state.__repr__()})"

    @property
    def shape(self) -> Shape:
        return self.__shape

    @property
    def state(self) -> State:
        return self.__current_state

    @state.setter
    def state(self, state: State) -> None:
        self.__current_state = state

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        self.__score = score

    @property
    def coords(self) -> list[tuple[int, int]]:
        return self.state.coords

    def move(self, direction: str) -> Optional[Exception]:
        self.state, score_received = self.state.move(direction)
        self.score += score_received

    def is_over(self) -> bool:
        return self.state.no_child_state()
