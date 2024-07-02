import blitzen
from donner import graph, spatial as sp


@blitzen.run
def main(input_string, verbose=False):
    field = graph.text_to_dict(input_string)
    trees = {k for k, v in field.items() if v == '|'}
    yards = {k for k, v in field.items() if v == '#'}
    field = set(field.keys())
    neighbors = {k: {k + d for d in sp.ENWS8} & field for k in field}
    history_list = []
    history_dict = {}
    while True:
        new_trees = set()
        new_yards = set()
        for k, n in neighbors.items():
            if k in trees:  # An acre filled with trees
                if len(n & yards) >= 3:  # if three or more adjacent acres were lumberyards.
                    new_yards.add(k)  # will become a lumberyard
                else:
                    new_trees.add(k)  # Otherwise, nothing happens.
            elif k in yards:  # An acre containing a lumberyard
                # if it was adjacent to at least one other lumberyard and at least one acre containing trees
                if len(n & trees) >= 1 and len(n & yards) >= 1:
                    new_yards.add(k)  # will remain a lumberyard
                # Otherwise, it becomes open
            else:  # An open acre
                if len(n & trees) >= 3:  # if three or more adjacent acres contained trees
                    new_trees.add(k)  # will become filled with trees
                # Otherwise, nothing happens.
        trees = new_trees
        yards = new_yards
        score = len(trees) * len(yards)
        history_key = (trees, yards)
        if score in history_dict and history_dict[score] == history_key:
            break
        history_dict[score] = history_key
        history_list.append(score)
    x = list(reversed(history_list)).index(score) + 1
    p2 = history_list[-x + (1000000000 - 1 - len(history_list)) % x]
    p1 = history_list[9]
    return p1, p2
