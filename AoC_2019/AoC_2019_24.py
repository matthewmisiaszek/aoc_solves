import dancer
from common import elementwise as ew, constants as con

BUG = '#'


def minute(bugs, neighbors):
    return {bug for bug, neigh in neighbors.items()
            if (bug in bugs and len(neigh & bugs) == 1)
            or (bug not in bugs and 1 <= len(neigh & bugs) <= 2)}


def part1(full_input):
    all_points = tuple(sorted(full_input.keys()))
    bugs = {key for key, val in full_input.items() if val is BUG}
    bio_points = {point: 2 ** i for i, point in enumerate(all_points)}
    neighbors = {bug: {ew.sum2d(bug, d) for d in con.D2D4} & bio_points.keys() for bug in bio_points.keys()}
    bio_ratings = set()
    while True:
        bio_rating = sum(bio_points[bug] for bug in bugs)
        if bio_rating in bio_ratings:
            break
        bio_ratings.add(bio_rating)
        bugs = minute(bugs, neighbors)
    return bio_rating


def neighbors2(all_points):
    yx, xx = max(all_points)
    ym, xm = yx // 2, xx // 2
    center = (ym, xm)
    size = xx - xm
    all_points.discard(center)
    neighbors = {bug: {ew.sum2d(bug, d) for d in con.D2D4} & all_points for bug in all_points}
    inside_edges = [ew.sum2d(center, d) for d in con.D2D4]
    outside_edges = [[ew.sum2d(ew.sum2d(center, d1, size), d2, pos)
                      for pos in range(-size, size + 1)]
                     for d1, d2 in zip(con.D2D4, con.D2D4[1:] + con.D2D4[0:1])]
    for iedge, oedges in zip(inside_edges, outside_edges):
        for oedge in oedges:
            neighbors[iedge].add((oedge, -1))
            neighbors[oedge].add((iedge, 1))
    return neighbors


def part2(full_input):
    bugs = {key for key, val in full_input.items() if val is BUG}
    all_points = set(full_input.keys())
    neighbors = neighbors2(all_points)
    bug_stack = [bugs]
    for _ in range(200):
        bug_stack = [set(), set()] + bug_stack + [set(), set()]
        new_stack = []
        for i in range(len(bug_stack) - 2):
            a, b, c = bug_stack[i:i + 3]
            aa = {(bug, -1) for bug in a}
            cc = {(bug, 1) for bug in c}
            bugs = aa | b | cc
            new_b = minute(bugs, neighbors)
            new_stack.append(new_b)
        bug_stack = new_stack
        while not bug_stack[0]:
            bug_stack = bug_stack[1:]
        while not bug_stack[-1]:
            bug_stack = bug_stack[:-1]
    return sum(len(bugs) for bugs in bug_stack)


def main(input_string, verbose=False):
    full_input = {(y, x): c
                  for y, line in enumerate(input_string.split('\n'))
                  for x, c in enumerate(line)}
    p1 = part1(full_input)
    p2 = part2(full_input)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=24, verbose=True)
