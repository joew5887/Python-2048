from interface import Interface


class Screen(Interface):
    def __init__(self):
        super().__init__()

    def show(self) -> None:
        print(self._game.state)

    def move(self, direction: str) -> None:
        self._game.move(direction)

    def retrieve_input(self) -> str:
        direction = input("")

        return direction

    def no_move_msg(self) -> str:
        print("Cannot do that move.")

    def endgame_sequence(self):
        print(f"Game Over. Score = {self._game.score}")


if __name__ == "__main__":
    x = Screen()
    x.run()
