import dancer
from common import spatial


def printdict(grid, default=' ', width=False, gridtype='cart'):
    print(strdict(grid, default, width, gridtype))


def strdict(grid, default=' ', width=False, gridtype='cart'):
    if grid:
        # convert tuple points to spatial points just in case
        grid = {spatial.Point(point): value for point, value in grid.items()}
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
    global hexspace
    if width is False:
        width = max(len(default), len(mark))
    if gridtype == 'hexns' or gridtype == 'hexew':
        width = min(width, 2)
        hexspace = default.rjust(width // 2)
    mark = mark.rjust(width)
    default = default.rjust(width)
    # convert tuple points to spatial points just in case
    grid = {spatial.Point(point)for point in grid}
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
