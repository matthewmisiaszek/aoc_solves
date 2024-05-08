import blitzen
from donner import graph, spatial


@blitzen.run
def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)
    grid = {key: int(val) for key, val in grid.items()}
    visible = set()
    max_scenic = 0
    for tree, height in grid.items():
        scenic = 1
        for direction in spatial.ENWS:
            loc = tree
            view = 0
            while True:
                loc += direction
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

