##################################
#		   game_utils			 #
##################################
from enum import Enum
from line_utils import Point
from collections import deque

class Color(Enum):
    RED         = 1
    ORANGE      = 2
    GREEN       = 3
    PURPLE      = 4
    LIGHT_BLUE  = 5
    DARK_BLUE   = 6
    DEBUG       = -2

dirs = lambda direction, current: {
    "DOWN_LEFT": Point(current.x - current.y%2, current.y - 1), #DOWN_LEFT
    "UP_LEFT": Point(current.x - current.y%2, current.y + 1), #UP_LEFT
    "LEFT": Point(current.x - 1, current.y), #LEFT
    "RIGHT": Point(current.x + 1, current.y), #RIGHT
    "DOWN_RIGHT": Point(current.x + (current.y + 1)%2, current.y - 1), #DOWN_RIGHT
    "UP_RIGHT": Point(current.x + (current.y + 1)%2, current.y + 1), #UP_RIGHT
}[direction]

def flood_fill(game, start, color):
	print(game.at(9, 8))

	out = set()
	out.add(start)

	q = deque()
	q.append(start)

	while q:
		c = q.pop()

		for pos in get_adjacent(c):
			bubble = game.at(pos.x, pos.y)
			if bubble == color and pos not in out:
				out.add(pos)
				q.append(pos)

	return list(out)

def get_adjacent(current):
	return (dirs("UP_RIGHT", current), 	dirs("UP_LEFT", current),
			dirs("LEFT", current), 		dirs("RIGHT", current),
			dirs("DOWN_LEFT", current), dirs("DOWN_RIGHT", current))
