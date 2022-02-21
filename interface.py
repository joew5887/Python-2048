from abc import abstractmethod, ABC
from game import Game, NoMoveError
from typing import Any


class Interface(ABC):
    def __init__(self):
        self._game = Game()

    @abstractmethod
    def show(self) -> None:
        pass

    @abstractmethod
    def move(self, direction: str) -> None:
        pass

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
