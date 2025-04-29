from game import Game
from constants import WIDTH, HEIGHT
class Multiplayer:
    def __init__(self):
        self._game1 = Game(WIDTH // 2 - 2, HEIGHT - 1)
        self._game2 = Game(WIDTH // 2 - 2, HEIGHT - 1)

    def multiply(self, number):
        return number * self.factor