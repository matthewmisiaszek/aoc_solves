import dancer
import common.constants as con
import common.elementwise as ew


def distance(loc):
    a, b = loc
    return (abs(a) + abs(b) + abs(a + b)) // 2


def main(input_string, verbose=False):
    input_string = input_string.upper()
    path = input_string.split(',')
    loc = con.origin2
    max_distance = 0
    for step in path:
        loc = ew.sum2d(loc, con.HEX_N[step])
        max_distance = max(max_distance, distance(loc))
    p1 = distance(loc)
    p2 = max_distance
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=11, verbose=True)
