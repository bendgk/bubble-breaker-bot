import numpy as np
from enum import Enum
from colorama import init, Fore, Back, Style
from collections import namedtuple
from line_utils import evenr_linedraw
import math, random


case = {
    -1: Fore.BLACK + Back.RED + "XX",
    0:  "  ",
    1:  Fore.RED + Back.BLACK + "R ",
    2:  Fore.YELLOW + Back.BLACK + "O ",
    3:  Fore.GREEN + Back.BLACK + "G ",
    4:  Fore.MAGENTA + Back.BLACK + "P ",
    5:  Fore.CYAN + Back.BLACK + "b ",
    6:  Fore.BLUE + Back.BLACK + "B ",
    -2:  Fore.WHITE + Back.RED + "+ "
}

case_raw = {
    -1: Fore.BLACK + Back.RED + "X",
    0:  Fore.WHITE + Back.BLACK + "0",
    1:  Fore.RED + Back.BLACK + "1",
    2:  Fore.YELLOW + Back.BLACK + "2",
    3:  Fore.GREEN + Back.BLACK + "3",
    4:  Fore.MAGENTA + Back.BLACK + "4",
    5:  Fore.CYAN + Back.BLACK + "5",
    6:  Fore.BLUE + Back.BLACK + "6",
    -2:  Fore.WHITE + Back.RED + "+"
}

class Color(Enum):
    RED         = 1
    ORANGE      = 2
    GREEN       = 3
    PURPLE      = 4
    LIGHT_BLUE  = 5
    DARK_BLUE   = 6
    DEBUG       = -2


class RenderMode(Enum):
    DEFAULT = 0
    HEX = 0
    GRID = 1
    RAW = 2

Point = namedtuple('Point', ['x', 'y'])
    
class Game:
    def __init__(self, width: int, height: int):
        self.width = width + 1
        self.height = height
        
        self.origin = Point(int(self.width/2), 0)

        self.bubbles = []

        #populate map
        self.reset_game()

    def boundtest(func):
        def onDecorator(self, x, y, *args, **kwargs):
            assert x in range(game.width), f"Out of bounds! x: {x} <--, y: {y}"
            assert y in range(game.height + 1), f"Out of bounds! x: {x}, y: {y} <--"
            return func(self, x, y, *args, **kwargs)

        return onDecorator

    def reset_game(self):
        random.seed(a=1337)
        self.map = np.zeros(shape=(self.width + 1, self.height + 1), dtype=int)
        
        for y in range(self.height):
            for x in range(self.width):
                if y < 8:
                    color = random.randint(1, 6)
                    self.map[x + y%2, y] = color
                    self.bubbles.append(Point(x + y%2, y))

            self.map[(self.width - 1) * ((y+1)%2), y] = -1
    
    @boundtest
    def at(self, x: int, y: int) -> int:
        return self.map[x, self.height - y - 1]
    

    @boundtest
    def set(self, x: int, y: int, data):
        self.map[x, self.height - y - 1] = data.value
            
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

class TrainingEnvironment:
    def __init__(self):
        self.game = Game(11, 17)

    def get_action_space(self):
        pass
    def get_observable_space(self):
        pass

if __name__ == '__main__':
    init()
    game = Game(11, 17)

    game.render()

    results = set()
    
    for y in range(2, game.height):
        collided = False

        start = game.origin
        end = Point(0, y)

        dy = (end.y - start.y) * 2
        dx = (end.x - start.x) * 2
        
        while not collided:
            line = evenr_linedraw(start, end)

            for i in range(1, len(line)):
                if game.at(line[i].x, line[i].y) > 0:
                    collided = True
                    print("Collided at:", line[i - 1])
                    results.add(line[i - 1])
                    break

                game.set(line[i].x, line[i].y, Color.DEBUG)

                
            ##########################################################
            #                       wall logic                       #
            ##########################################################
            start = end
            dx = -dx
            end = Point(start.x + int(np.sign(dx)*11), start.y + abs(int(dy/dx*11)))

            game.render()
            print(start, end)
            input()

        game.reset_game()

    print(len(results))
