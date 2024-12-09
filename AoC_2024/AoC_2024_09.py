import blitzen


class Segment:
    def __init__(self, size, id):
        self.size = size
        self.id = id

    def __repr__(self):
        return f'Segment {self.id} length {self.size}'


def checksum(disk):
    position = 0
    cs = 0
    for segment in disk:
        if segment.id is not None:
            cs += segment.id * sum(range(position, position + segment.size))
        position += segment.size
    return cs


def part1(disk):
    disk_defragged = []
    for file in disk:
        if file.id is not None:
            disk_defragged.append(file)
            continue
        to_fill = file.size
        while to_fill:
            while (last := disk.pop(-1)).id is None:
                pass
            disk_defragged.append(Segment(min(to_fill, last.size), last.id))
            if last.size > to_fill:
                disk.append(Segment(last.size - to_fill, last.id))
            to_fill -= min(to_fill, last.size)
    return checksum(disk_defragged)


def part2(disk):
    for i in range(-1, -len(disk), -1):
        file = disk[i]
        if file.id is None:
            continue
        for j in range(len(disk)+i):
            sector = disk[j]
            if sector.id is None and (remainder := sector.size - file.size) >= 0:
                disk[j] = Segment(file.size, file.id)
                file.id = None
                if remainder:
                    disk.insert(j+1, Segment(remainder, None))
                break
    return checksum(disk)


@blitzen.run
def main(input_string, verbose=False):
    disk = [Segment(int(c), i // 2 if i % 2 == 0 else None) for i, c in enumerate(input_string)]
    p1 = part1(disk.copy())
    p2 = part2(disk)
    return p1, p2
