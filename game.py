import numpy as np
from scipy.ndimage.measurements import label
from enum import Enum
from colorama import init, Fore, Back, Style
from collections import namedtuple
from line_utils import evenr_linedraw
from line_utils import Point
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
    
class Game:
    def __init__(self, width: int, height: int):
        self.width = width + 1
        self.height = height
        
        self.origin = Point(int(self.width/2), 0)

        self.bubbles = []

        self.seed = 1337
        self.rows = 8

        #populate map
        self.reset_game()

    def boundtest(func):
        def onDecorator(self, x, y, *args, **kwargs):
            assert x in range(self.width), "Out of bounds! x: " + str(x) + " <--, y: " + str(y)
            assert y in range(self.height + 1), f"Out of bounds! x: " + str(x) + ", y: " + str(y) +" <--"
            return func(self, x, y, *args, **kwargs)

        return onDecorator

    def reset_game(self, seed=None):
        if seed: self.seed = seed
        random.seed(self.seed)
        self.populate(rows=8)


    def populate(self, rows):
        random.seed(self.seed)
        self.bubbles = []

        self.map = np.zeros(shape=(self.width + 1, self.height + 1), dtype=int)

        for y in range(self.height - 1, -1, -1):
            for x in range(self.width - 1, -1, -1):
                if y < rows:
                    color = random.randint(1, 6)
                    self.map[x + y%2, y] = color
                    self.bubbles.append([Point(x + y%2, y), -1 if (x == (self.width - 1) * ((y+1)%2)) else color])

            self.map[(self.width - 1) * ((y+1)%2), y] = -1

    def clear_board(self):
        for y in range(0, self.height, -1):
            for x in range(0, self.width, -1):
                if game.at(x, y) == -2:
                    game.set(x, y, 0)

    def add_row_of_bubbles(self):
        self.rows += 1
        t.game.populate(rows=self.rows)

    def shoot(self):
        return label(self.map)
    
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
        init()
        self.game = Game(11, 17)
        self.action_space = []
        self.observable_space = []

    def update_action_space(self):
        # mess of things for defining wall
        a = [Point(0, y) for y in range(2, self.game.height)]
        b = [Point(x, self.game.height - 1) for x in range(self.game.width)]
        c = [Point(self.game.width - 1, y) for y in range(2, self.game.height)]
        for i in b: a.append(i)
        for i in c: a.append(i)
        points_to_iterate = a

        results = set()
        
        for point in points_to_iterate:
            if point.x == 6 and point.y == 16: continue
            
            collided = False

            start = self.game.origin
            end = point

            dy = (end.y - start.y) * 2
            dx = (end.x - start.x) * 2
            
            while not collided:
                line = evenr_linedraw(start, end)

                for i in range(1, len(line)):
                    if self.game.at(line[i].x, line[i].y) > 0:
                        collided = True
                        #print("Collided at:", line[i - 1], "val:", self.game.at(line[i].x, line[i].y))
                        results.add(line[i - 1])
                        #self.game.render()
                        break

                    #self.game.set(line[i].x, line[i].y, Color.DEBUG)

                    
                ##########################################################
                #                       wall logic                       #
                ##########################################################
                start = end
                dx = -dx
                end = Point(start.x + int(np.sign(dx)*11), start.y + abs(int(dy/dx*11)))

        action_space = []
        for result in results:
            if self.game.at(result.x, result.y) != -1:
                action_space.append(result)

        #self.game.render()
        return action_space
    
    def update_observable_space(self):
        return self.game.map

if __name__ == '__main__':
    init()
    t = TrainingEnvironment()
    #t.game.render()
    t.game.add_row_of_bubbles()
    t.game.render()
    print(len(t.update_action_space()))

    #print(t.game.bubbles)
    #print(t.game.at(11, 8))
    #print([i[1] for i in t.game.bubbles[13: 24]])

    #bubbles = [[i[1] for i in t.game.bubbles[(x*12):(x*12)+12]] for x in range(t.game.rows)]
    #for row in bubbles:
        #print(row)
    #Implement floodfill for popping bubble



