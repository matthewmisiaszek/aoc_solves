import blitzen


def istriangle(triangle):
    return 2 * max(triangle) < sum(triangle)


@blitzen.run
def main(input_string, verbose=False):
    triangles = [[int(i) for i in line.split()] for line in input_string.split('\n')]
    p1 = sum(istriangle(triangle) for triangle in triangles)
    triangles2 = sum(zip(*triangles), ())  # transpose and append to single tuple
    triangles3 = tuple(zip(*[triangles2[i::3] for i in range(3)]))  # split by chunks of 3
    p2 = sum(istriangle(triangle) for triangle in triangles3)
    return p1, p2

