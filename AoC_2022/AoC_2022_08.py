import dancer
from common import graph, constants as con, elementwise as ew


def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)
    grid = {key: int(val) for key, val in grid.items()}
    visible = set()
    max_scenic = 0
    for tree, height in grid.items():
        scenic = 1
        for direction in con.D2D4:
            loc = tree
            view = 0
            while True:
                loc = ew.sum2d(loc, direction)
                if loc not in grid:
                    visible.add(tree)
                    break
                view += 1
                if grid[loc] >= height:
                    break
            scenic *= view
        max_scenic = max(max_scenic, scenic)
    p1 = len(visible)
    p2 = max_scenic
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=8, verbose=True)
