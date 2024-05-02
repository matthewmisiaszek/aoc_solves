import blitzen
from donner import graph, spatial as sp
from donner import printer


def animate(lights, grid, neighbors, steps, stuck=None, verbose=False):
    if stuck is None:
        stuck = set()
    for step in range(steps):
        lights = {light for light in grid
                  if (light in lights and 2 <= len(lights & neighbors[light]) <= 3)
                  or len(lights & neighbors[light]) == 3}
        if stuck:
            lights.update(stuck)
    if verbose:
        printer.printset(lights)
    return lights


def main(input_string, verbose=False):
    on = '#'
    grid = graph.text_to_dict(input_string)
    lights = {light for light, state in grid.items() if state is on}
    grid = set(grid.keys())
    neighbors = {light: {light + direction for direction in sp.ENWS8} for light in grid}
    max_corner = max(grid)
    stuck = {sp.Point(), max_corner*sp.EAST, max_corner*sp.SOUTH, max_corner}
    p1 = len(animate(lights, grid, neighbors, 100, verbose=verbose))
    lights.update(stuck)
    p2 = len(animate(lights, grid, neighbors, 100, stuck, verbose=verbose))
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2015, day=18, verbose=True)
