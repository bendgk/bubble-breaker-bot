import numpy as np
import pprint
from enum import Enum
import random

class Game:
    def __init__(self, width: int, height: int):
        self.width = width - 1
        self.height = height - 1
        
        self.map = np.zeros(shape=(width, height), dtype=int)

        #populate map
        random.seed(a=None)
        self.populate()

    def boundtest(func):
        def onDecorator(self, x, y, *args, **kwargs):
            assert x in range(game.width) and y in range(game.height)
            return func(self, x, y, *args, **kwargs)

        return onDecorator

    def populate(self):
        for y in range(8):
            for x in range(self.width - 1):
                self.map[x + y%2, y] = random.randint(1, 6)
                
    @boundtest
    def at(self, x: int, y: int) -> int:
        return self.map[x, y]

    @boundtest
    def set(self, x: int, y: int, data):
        self.map[x, y] = data.value
        
    def clear(self):
        self.map = np.zeros(shape=(self.height, self.width), dtype=int)
            
    def render(self):
        b = ""
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x, y] == 0: b += "  "
                else: b += str(self.map[x, y]) + " "
            b += "\n"

        print(b)

class Color(Enum):
    RED         = 1
    ORANGE      = 2
    GREEN       = 3
    PURPLE      = 4
    LIGHT_BLUE  = 5
    DARK_BLUE   = 6

if __name__ == '__main__':
    game = Game(12, 17)
    game.set(1, 1, Color.RED)
    game.render()
