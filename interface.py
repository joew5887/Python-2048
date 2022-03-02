from abc import abstractmethod, ABC
from logic import Game, NoMoveError


class Interface(ABC):
    def __init__(self, tiles_x: int, tiles_y: int):
        self._game = Game(tiles_x, tiles_y)

    @abstractmethod
    def show(self) -> None:
        pass

    def move(self, direction: str) -> None:
        self._game.move(direction)

    @abstractmethod
    def retrieve_input(self) -> str:
        pass

    @abstractmethod
    def no_move_msg(self) -> str:
        pass

    @abstractmethod
    def endgame_sequence(self):
        pass

    def run(self) -> None:
        while (not self._game.is_over()):
            self.show()
            direction = self.retrieve_input()

            if direction == "q":
                break

            try:
                self.move(direction)
            except NoMoveError:
                self.no_move_msg()

        self.endgame_sequence()
