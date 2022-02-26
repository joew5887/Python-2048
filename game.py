import pygame
from interface import Interface
from logic import MOVES, NoMoveError, Tile

DIRECTIONS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
KEY_TO_DIRECTION = dict(zip(DIRECTIONS, MOVES))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE_COLOURS = {
    2: (230, 230, 230), 4: (200, 200, 200), 8: (235, 168, 52),
    16: (235, 146, 52), 32: (235, 113, 52),
    64: (235, 94, 52), 128: (235, 229, 52),
    256: (235, 219, 52), 512: (235, 210, 52),
    1024: (235, 204, 52), 2048: (235, 198, 52)
}

pygame.init()


def tile_to_colour(tile_value: int) -> tuple[int, int, int]:
    colour = TILE_COLOURS.get(tile_value)

    if colour is None:
        colour = WHITE

    return colour


class Tile:
    def __init__(self, tile: Tile):
        self.__tile = tile
        self.__colour = tile_to_colour(self.__tile.value)

    def draw(self, window: pygame.Surface, x_start: int, y_start: int, x_size: int, y_size: int) -> pygame.Surface:
        pygame.draw.rect(window, self.__colour,
                         (x_start, y_start, x_size, y_size))
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.__tile), True, BLACK)
        text_rect = text.get_rect(center=(x_start+x_size/2, y_start+y_size/2))
        window.blit(text, text_rect)

        return window


class Board(Interface):
    def __init__(self, side: int = 500):
        super().__init__()
        self.__win = pygame.display.set_mode((side, side))
        self._game.coords
        self._game.shape
        pygame.display.set_caption("Game")

    def __update_tiles(self) -> dict[tuple[int, int], Tile]:
        tiles = {}

        for coord in self._game.coords:
            tile = self._game.state[coord]
            tiles[coord] = Tile(tile)

        return tiles

    def show(self) -> None:
        self.__win.fill(BLACK)
        tiles = self.__update_tiles()

        for x in range(self._game.shape.x):
            for y in range(self._game.shape.y):
                x_start = 100*y + 20
                y_start = 100*x + 20
                tile = tiles[(x, y)]
                self.__win = tile.draw(self.__win, x_start, y_start, 90, 90)

    def retrieve_input(self, events: list) -> str:
        for event in events:
            if event.type == pygame.QUIT:
                self.endgame_sequence()

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
            pygame.time.delay(80)

            self.show()
            direction = self.retrieve_input(pygame.event.get())

            if direction is not None:
                try:
                    self.move(direction)
                    print(self._game)
                except NoMoveError:
                    self.no_move_msg()

            pygame.display.update()

        self.endgame_sequence()


if __name__ == "__main__":
    game = Board()
    game.run()
