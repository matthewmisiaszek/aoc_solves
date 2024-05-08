import blitzen
import donner.spatial as sp


def distance(loc):
    a, b = loc.x, loc.y
    return (abs(a) + abs(b) + abs(a + b)) // 2


@blitzen.run
def main(input_string, verbose=False):
    input_string = input_string
    path = input_string.split(',')
    loc = sp.Point()
    max_distance = 0
    for step in path:
        loc += sp.NAMES_HEX_S[step]
        max_distance = max(max_distance, distance(loc))
    p1 = distance(loc)
    p2 = max_distance
    return p1, p2

