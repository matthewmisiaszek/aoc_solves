import dancer
from common import elementwise as ew, constants as con
# from common import printer


def animate(lights, grid, neighbors, steps, stuck=None, verbose=False):
    if stuck is None:
        stuck = set()
    for step in range(steps):
        lights = {light for light in grid
                  if (light in lights and 2 <= len(lights & neighbors[light]) <= 3)
                  or len(lights & neighbors[light]) == 3}
        if stuck:
            lights.update(stuck)
        # if verbose:
        #     printer.printset(lights)
    return lights


def main(input_string, verbose=False):
    on = '#'

    grid = {(x, y): c
            for y, line in enumerate(input_string.split('\n'))
            for x, c in enumerate(line)}

    lights = {light for light, state in grid.items() if state is on}

    grid = set(grid.keys())

    neighbors = {light: {ew.sum2d(light, direction)
                         for direction in con.D2D8}
                 for light in grid}

    max_corner = max(grid)
    max_x, max_y = max_corner
    stuck = {(0, 0), (max_x, 0), (0, max_y), max_corner}

    p1 = len(animate(lights, grid, neighbors, 100, verbose=verbose))
    p2 = len(animate(lights, grid, neighbors, 100, stuck, verbose=verbose))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=18, verbose=True)
