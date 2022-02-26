import pygame
from interface import Interface
from logic import MOVES, NoMoveError, Tile

DIRECTIONS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_DOWN]
KEY_TO_DIRECTION = dict(zip(DIRECTIONS, MOVES))

pygame.init()


class Tile:
    def __init__(self, tile: Tile):
        self.__tile = Tile


class Board(Interface):
    def __init__(self, side: int = 500):
        super().__init__()
        self.__win = pygame.display.set_mode((side, side))
        self.__coords = self._game.coords
        pygame.display.set_caption("Game")

    def show(self) -> None:
        pass

    def retrieve_input(self) -> str:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            return KEY_TO_DIRECTION[pygame.K_UP]
        elif keys[pygame.K_DOWN]:
            return KEY_TO_DIRECTION[pygame.K_DOWN]
        elif keys[pygame.K_LEFT]:
            return KEY_TO_DIRECTION[pygame.K_LEFT]
        elif keys[pygame.K_RIGHT]:
            return KEY_TO_DIRECTION[pygame.K_RIGHT]
        else:
            return None

    def no_move_msg(self) -> str:
        pass

    def endgame_sequence(self):
        pygame.quit()

    def run(self) -> None:
        while (not self._game.is_over()):
            pygame.time.delay(10)

            self.show()
            direction = self.retrieve_input()

            if direction is not None:
                try:
                    self.move(direction)
                except NoMoveError:
                    self.no_move_msg()

            pygame.display.update()

        self.endgame_sequence()


if __name__ == "__main__":
    game = Board()
    game.run()
