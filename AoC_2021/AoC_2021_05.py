import dancer


class ventClass:
    def __init__(self):
        self.points = {}
        self.intersections = 0

    def add(self, point):
        if point not in self.points:
            self.points[point] = 0
        self.points[point] += 1
        if self.points[point] == 2:
            self.intersections += 1


def solve(f, diagonal=False):
    vents = ventClass()
    dims = range(2)
    for l in f:
        p1, p2 = [tuple([int(i) for i in p.split(',')]) for p in l.split(' -> ')]
        if diagonal or p1[0] == p2[0] or p1[1] == p2[1]:
            diff = tuple([p2[i] - p1[i] for i in dims])
            span = max([abs(diff[i]) for i in dims])
            inc = tuple([diff[i] // span for i in dims])
            end = tuple([p2[i] + inc[i] for i in dims])
            point = p1
            while point != end:
                vents.add(point)
                point = tuple([point[i] + inc[i] for i in dims])
    return vents.intersections


def main(input_string, verbose=False):
    f = input_string.split('\n')
    p1 = solve(f)
    p2 = solve(f, True)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2021, day=5, verbose=True)
