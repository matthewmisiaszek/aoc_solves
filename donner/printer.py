import blitzen
from donner import spatial
import re


def printdict(grid, default=' ', width=False, gridtype='cart'):
    print(strdict(grid, default, width, gridtype))


def strdict(grid, default=' ', width=False, gridtype='cart'):
    if not grid:
        return ''
    # convert tuple points to spatial points just in case
    grid = {point if isinstance(point, spatial.Point) else spatial.Point(point): value for point, value in grid.items()}
    nb, xb = spatial.bounds(grid)
    if width is False:
        width = max([len(str(si)) for si in grid.values()])
    if width > 1:
        width += 1
    if gridtype == 'hexns' or gridtype == 'hexew':
        width = min(width, 2)
        hexspace = default.rjust(width // 2)
    default = default.rjust(width)
    printstr = ''
    for y in range(nb.y, xb.y + 1):
        if gridtype == 'hexns' or gridtype == 'hexew':
            printstr += ''.join([hexspace for _ in range(nb.y, xb.y - y)])
        for x in range(nb.x, xb.x + 1):
            point = spatial.Point(x, y)
            if point in grid:
                printstr += str(grid[point]).rjust(width)
            else:
                printstr += default
        printstr += '\n'
    return printstr[:-1]


def printset(grid, default=' ', mark='#', width=False, gridtype='cart'):
    print(strset(grid, default, mark, width, gridtype))


def strset(grid, default=' ', mark='#', width=False, gridtype='cart'):
    if not grid:
        return ''
    global hexspace
    if width is False:
        width = max(len(default), len(mark))
    if gridtype == 'hexns' or gridtype == 'hexew':
        width = min(width, 2)
        hexspace = default.rjust(width // 2)
    mark = mark.rjust(width)
    default = default.rjust(width)
    # convert tuple points to spatial points just in case
    grid = {point if isinstance(point, spatial.Point) else spatial.Point(point)for point in grid}
    nb, xb = spatial.bounds(grid)
    printstr = ''
    for y in range(nb.y, xb.y + 1):
        if gridtype == 'hexns' or gridtype == 'hexew':
            printstr += ''.join([hexspace for i in range(nb.y, xb.y - y)])
        for x in range(nb.x, xb.x + 1):
            if spatial.Point(x, y) in grid:
                printstr += mark
            else:
                printstr += default
        printstr += '\n'
    return printstr[:-1]


def printarray(grid, width):
    print(strarray(grid,width))


def strarray(grid, width):
    shape = grid.shape
    s = ''
    for i in range(shape[0]):
        for j in range(shape[1]):
            s += str(grid[i, j]).rjust(width)
        s += '\n'
    return s[:-1]


def _makechars():
    ASCII_ALPH_6 = """
.....##..###...##..####.####..##..#..#.###...##.#..#.#.....##..###..###...###.#..#.#...#.####
....#..#.#..#.#..#.#....#....#..#.#..#..#.....#.#.#..#....#..#.#..#.#..#.#....#..#.#...#....#
....#..#.###..#....###..###..#....####..#.....#.##...#....#..#.#..#.#..#.#....#..#..#.#....#.
....####.#..#.#....#....#....#.##.#..#..#.....#.#.#..#....#..#.###..###...##..#..#...#....#..
....#..#.#..#.#..#.#....#....#..#.#..#..#..#..#.#.#..#....#..#.#....#.#.....#.#..#...#...#...
....#..#.###...##..####.#.....###.#..#.###..##..#..#.####..##..#....#..#.###...##....#...####
    """
    LETTERS_6 = 'ABCEFGHIJKLOPRSUYZ'

    ASCII_ALPH_10 = """
......##...#####...####..######.######..####..#....#....###.#....#.#......#....#.#####..#####..#....#.######
.....#..#..#....#.#....#.#......#......#....#.#....#.....#..#...#..#......##...#.#....#.#....#.#....#......#
....#....#.#....#.#......#......#......#......#....#.....#..#..#...#......##...#.#....#.#....#..#..#.......#
....#....#.#....#.#......#......#......#......#....#.....#..#.#....#......#.#..#.#....#.#....#..#..#......#.
....#....#.#####..#......#####..#####..#......######.....#..##.....#......#.#..#.#####..#####....##......#..
....######.#....#.#......#......#......#..###.#....#.....#..##.....#......#..#.#.#......#..#.....##.....#...
....#....#.#....#.#......#......#......#....#.#....#.....#..#.#....#......#..#.#.#......#...#...#..#...#....
....#....#.#....#.#......#......#......#....#.#....#.#...#..#..#...#......#...##.#......#...#...#..#..#.....
....#....#.#....#.#....#.#......#......#...##.#....#.#...#..#...#..#......#...##.#......#....#.#....#.#.....
....#....#.#####...####..######.#.......###.#.#....#..###...#....#.######.#....#.#......#....#.#....#.######
    """
    LETTERS_10 = 'ABCEFGHJKLNPRXZ'

    chars = {}
    for ascii, letters in ((ASCII_ALPH_6, LETTERS_6), (ASCII_ALPH_10, LETTERS_10)):
        grid = {spatial.Point(y, x) for y, line in enumerate(ascii.strip().split('\n')) for x, c in enumerate(line) if c == '#'}
        printstr = strset(grid)
        for letter, char in zip(letters, re.split(r'\n\s*\n', printstr)):
            chars[char] = letter
    return chars


CHARS = _makechars()


def ocr(s: str, mark='#'):
    grid = {spatial.Point(y, x) for y, line in enumerate(s.split('\n')) for x, c in enumerate(line) if c is mark}
    printstr = strset(grid)
    return ''.join(CHARS[char] if char in CHARS else '_' for char in re.split(r'\n\s*\n', printstr))