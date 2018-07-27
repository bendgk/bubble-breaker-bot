import numpy as np
import pprint
from enum import Enum
import random
from colorama import init
from colorama import Fore, Back, Style

case = {
    -1: Fore.BLACK + Back.RED + "XX",
    0:  "  ",
    1:  Fore.RED + Back.BLACK + "R ",
    2:  Fore.YELLOW + Back.BLACK + "O ",
    3:  Fore.GREEN + Back.BLACK + "G ",
    4:  Fore.MAGENTA + Back.BLACK + "P ",
    5:  Fore.CYAN + Back.BLACK + "b ",
    6:  Fore.BLUE + Back.BLACK + "B "
}

case_raw = {
    -1: Fore.BLACK + Back.RED + "X",
    0:  Fore.WHITE + Back.BLACK + "0",
    1:  Fore.RED + Back.BLACK + "1",
    2:  Fore.YELLOW + Back.BLACK + "2",
    3:  Fore.GREEN + Back.BLACK + "3",
    4:  Fore.MAGENTA + Back.BLACK + "4",
    5:  Fore.CYAN + Back.BLACK + "5",
    6:  Fore.BLUE + Back.BLACK + "6"
}

class Color(Enum):
    RED         = 1
    ORANGE      = 2
    GREEN       = 3
    PURPLE      = 4
    LIGHT_BLUE  = 5
    DARK_BLUE   = 6


class RenderMode(Enum):
    DEFAULT = 0
    HEX = 0
    GRID = 1
    RAW = 2
    
class Game:
    def __init__(self, width: int, height: int):
        self.map = np.zeros(shape=(width, height), dtype=int)
        self.width = width - 1
        self.height = height - 1
        

        #populate map
        random.seed(a=1)
        self.populate()

    def boundtest(func):
        def onDecorator(self, x, y, *args, **kwargs):
            assert x in range(game.width) and y in range(game.height)
            return func(self, x, y, *args, **kwargs)

        return onDecorator

    def populate(self):
        for y in range(self.height):
            for x in range(self.width):
                if y < 8:
                    self.map[x + y%2, y] = random.randint(1, 6)

            self.map[(self.width - 1) * ((y+1)%2), y] = -1
    
    @boundtest
    def at(self, x: int, y: int) -> int:
        return self.map[x, y]
    

    @boundtest
    def set(self, x: int, y: int, data):
        self.map[x, y] = data.value
            
    def render(self, mode=RenderMode.DEFAULT):
        out = ""
        for y in range(self.height):
            if mode is RenderMode.RAW: b = "-----" * self.width + "\n"
            else: b = ""
            for x in range(self.width):
                if mode in [RenderMode.DEFAULT, RenderMode.HEX, RenderMode.GRID] : b += case[self.map[x, y]] + Fore.RESET + Back.RESET
                else:
                    b += "- " + case_raw[self.map[x, y]] + Fore.RESET + Back.RESET + " -"

            if mode.value == 0: out += "-"*((y + 1)%2) + b + "-"*(y%2) + "\n"
            else: out += b + "\n"

        print(out)

if __name__ == '__main__':
    init()
    game = Game(11, 17)
    game.set(1, 1, Color.LIGHT_BLUE)
    game.render(mode = RenderMode.RAW)
