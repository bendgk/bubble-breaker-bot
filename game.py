import numpy as np
import pprint
from enum import Enum
import random
from colorama import init
from colorama import Fore, Back, Style

case = {
    -1: Fore.BLACK + Back.RED + "- ",
    0:  "  ",
    1:  Fore.RED + Back.BLACK + "R ",
    2:  Fore.YELLOW + Back.BLACK + "O ",
    3:  Fore.GREEN + Back.BLACK + "G ",
    4:  Fore.MAGENTA + Back.BLACK + "P ",
    5:  Fore.CYAN + Back.BLACK + "b ",
    6:  Fore.BLUE + Back.BLACK + "B "
}

class Game:
    def __init__(self, width: int, height: int):
        self.width = width - 1
        self.height = height - 1
        
        self.map = np.zeros(shape=(width, height), dtype=int)

        #populate map
        random.seed(a=1)
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

            self.map[(self.width - 1) * ((y+1)%2), y] = -1
    
    @boundtest
    def at(self, x: int, y: int) -> int:
        return self.map[x, y]
    

    @boundtest
    def set(self, x: int, y: int, data):
        self.map[x, y] = data.value
        
    def clear(self):
        self.map = np.zeros(shape=(self.width, self.height), dtype=int)
            
    def render(self):
        out = ""
        for y in range(self.height):
            b = ""
            for x in range(self.width):
                b += case[self.map[x, y]] + Fore.RESET + Back.RESET
                
            out += "-"*((y + 1)%2) + b + "-"*(y%2) + "\n"

        print(out)

class Color(Enum):
    RED         = 1
    ORANGE      = 2
    GREEN       = 3
    PURPLE      = 4
    LIGHT_BLUE  = 5
    DARK_BLUE   = 6

if __name__ == '__main__':
    init()
    game = Game(12, 18)
    game.set(1, 1, Color.RED)
    game.render()
