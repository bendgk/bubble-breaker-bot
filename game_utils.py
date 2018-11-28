##################################
#		   game_utils			 #
##################################
from enum import Enum
from line_utils import Point
from collections import deque

dirs = lambda direction, current: {
    "DOWN_LEFT": Point(current.x - current.y%2, current.y - 1), #DOWN_LEFT
    "UP_LEFT": Point(current.x - current.y%2, current.y + 1), #UP_LEFT
    "LEFT": Point(current.x - 1, current.y), #LEFT
    "RIGHT": Point(current.x + 1, current.y), #RIGHT
    "DOWN_RIGHT": Point(current.x + (current.y + 1)%2, current.y - 1), #DOWN_RIGHT
    "UP_RIGHT": Point(current.x + (current.y + 1)%2, current.y + 1), #UP_RIGHT
}[direction]

def flood_fill(node, target_color: int, replacement_color: int):
	if target_color == replacement_color: return
