import pygame
from interface import Interface
from logic import MOVES, NoMoveError, Tile

DIRECTIONS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
KEY_TO_DIRECTION = dict(zip(DIRECTIONS, MOVES))  # {pygame.K_UP: 'u', ...}

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
    """
    Gets the tile colour based on it's value.

    Parameters
    ---
    tile_value (int): Numerical value of the tile. Used to retrieve the right colour.

    Returns
    ---
    colour (tuple[int, int, int]): RGB colour.

    """

    colour = TILE_COLOURS.get(tile_value)

    if colour is None:
        colour = WHITE

    return colour


class Tile:
    def __init__(self, tile: Tile):
        self.__tile = tile
        self.__colour = tile_to_colour(self.__tile.value)

    def draw(self, window: pygame.Surface, x_start: int, y_start: int, side: int) -> pygame.Surface:
        pygame.draw.rect(window, self.__colour,
                         (x_start, y_start, side, side))
        font_size = int(side / 2)
        font = pygame.font.Font(None, font_size)
        text = font.render(str(self.__tile), True, BLACK)
        text_rect = text.get_rect(center=(x_start+side/2, y_start+side/2))
        window.blit(text, text_rect)

        return window


class Board(Interface):
    def __init__(self, tiles_x: int, tiles_y: int, tile_size: int = 80, spacer_size: int = 10):
        super().__init__(tiles_x, tiles_y)
        self.__draw(tile_size, spacer_size)

    def __draw(self, tile_size: int, spacer_size: int) -> None:
        self.__tile_size = tile_size
        self.__spacer_size = spacer_size
        self.__y_shift = self.__tile_size / 2
        side_x = self.__tile_start_seq(self._game.shape.y)
        side_y = self.__tile_start_seq(self._game.shape.x)
        self.__shape = (side_x, self.__y_shift + side_y)
        self.__win = pygame.display.set_mode(self.__shape)
        pygame.display.set_caption("2048")

    def __tile_start_seq(self, tile_num: int) -> int:
        d = self.__tile_size + self.__spacer_size
        a = self.__spacer_size

        return a + d*tile_num

    def __update_tiles(self) -> dict[tuple[int, int], Tile]:
        tiles = {}

        for coord in self._game.coords:
            tile = self._game.state[coord]
            tiles[coord] = Tile(tile)

        return tiles

    def show(self) -> None:
        self.__win.fill(BLACK)
        tiles = self.__update_tiles()

        font_size = int(self.__tile_size / 2)
        font = pygame.font.Font(None, font_size)
        text = font.render(f'Score: {self._game.score}', True, WHITE, BLACK)
        self.__win.blit(text, (self.__spacer_size, self.__spacer_size))

        for y in range(self._game.shape.y):
            for x in range(self._game.shape.x):
                x_start = self.__tile_start_seq(y)
                y_start = self.__tile_start_seq(x) + self.__y_shift
                tile = tiles[(x, y)]
                self.__win = tile.draw(
                    self.__win, x_start, y_start, self.__tile_size)

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
            pygame.time.delay(120)

            self.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.endgame_sequence()

            direction = self.retrieve_input()

            if direction is not None:
                print(direction)
                try:
                    self.move(direction)
                except NoMoveError:
                    self.no_move_msg()

            pygame.display.update()

        self.endgame_sequence()


def main() -> None:
    game = Board(4, 4)
    game.run()


if __name__ == "__main__":
    main()
