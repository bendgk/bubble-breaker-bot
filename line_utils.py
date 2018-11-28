import numpy as np
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Cube = namedtuple('Cube', ['x', 'y', 'z'])

dirs = lambda i, j, current: {
    (-1, -1): Point(current.x - current.y%2, current.y - 1), #DOWN_LEFT
    (-1, 1): Point(current.x - current.y%2, current.y + 1), #UP_LEFT
    (0, -1): Point(current.x - 1, current.y), #LEFT
    (0, 1): Point(current.x + 1, current.y), #RIGHT
    (1, -1): Point(current.x + (current.y + 1)%2, current.y - 1), #DOWN_RIGHT
    (1, 1): Point(current.x + (current.y + 1)%2, current.y + 1), #UP_RIGHT
}[(i, j)]

def line_of_sight(start: Point, end: Point):
    current = start

    dx = end.x - start.x
    dy = end.y - start.y

    x_sign = np.sign(dx)
    y_sign = np.sign(dy)

    dx = abs(dx)
    dy = abs(dy)
    
    e = 0

    points = []
    
    while current != end:
        if e > 1:
            current = dirs(-x_sign, y_sign, current) #UP_LEFT
            e = e - (3*dy)/(4*dx) - 1.5

        else:
            e = e + (3*dy)/(4*dx)

            if e > 0.5:
                current = dirs(x_sign, y_sign, current) #UP_RIGHT
                e = e - 1.5

            else:
                if e < -0.5:
                    current = dirs(x_sign, -y_sign, current) #DOWN_RIGHT
                    e = e + 1.5

                else:
                    current = dirs(0, x_sign, current) #RIGHT
                    e = e = e + (3*dy)/(4*dx)
  
        points.append(current)

    return points

def evenr_to_cube(point: Point):
    x = point.x - (point.y + (point.y&1))/2
    z = point.y
    y = -x - z

    return Cube(x, y, z)

def cube_to_evenr(cube: Cube):
    x = int(cube.x + (cube.z + (cube.z&1)) / 2)
    y = int(cube.z)

    return Point(x, y)

def lerp(a, b, t):
    return a + (b - a) * t

def cube_lerp(a, b, t):
    return Cube(lerp(a.x, b.x, t), 
                lerp(a.y, b.y, t),
                lerp(a.z, b.z, t))

def cube_distance(a, b):
    return int(max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z)))

def cube_round(cube: Cube):
    rx = round(cube.x)
    ry = round(cube.y)
    rz = round(cube.z)

    x_diff = abs(rx - cube.x)
    y_diff = abs(ry - cube.y)
    z_diff = abs(rz - cube.z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return Cube(rx, ry, rz)

def evenr_linedraw(a: Point, b: Point):
    a = evenr_to_cube(a)
    b = evenr_to_cube(b)
    
    N = cube_distance(a, b)
    results = []
    
    for i in range(N + 1):
        results.append(cube_to_evenr(cube_round(cube_lerp(a, b, 1.0/N * i))))

    return results
