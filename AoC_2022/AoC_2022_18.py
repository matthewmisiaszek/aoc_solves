import blitzen
from donner import spatial


def main(input_string, verbose=False):
    cubes = {spatial.Point(*(int(i) for i in line.split(','))) for line in input_string.split('\n')}
    p1 = sum(cube+direction not in cubes for cube in cubes for direction in spatial.D3D6)
    bounds = spatial.bounds(cubes, pad=1)
    corner, _ = bounds
    queue = [corner]
    closed = {corner}
    p2 = 0
    while queue:
        curr = queue.pop()
        for d in spatial.D3D6:
            neighbor = curr + d
            if neighbor in cubes:
                p2 += 1
            elif neighbor not in closed and spatial.inbounds(neighbor, bounds):
                closed.add(neighbor)
                queue.append(neighbor)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=18, verbose=True)
