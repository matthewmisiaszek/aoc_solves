import DANCER


def printdict(grid, default=' ', width=False, gridtype='cart'):
    print(strdict(grid, default, width, gridtype))


def strdict(grid, default=' ', width=False, gridtype='cart'):
    if grid:
        mins = [min((si[i] for si in grid.keys())) for i in range(2)]
        maxs = [max((si[i] for si in grid.keys())) for i in range(2)]
        if width is False:
            width = max([len(str(grid[si])) for si in grid.keys()])
        if width > 1:
            width += 1
        if gridtype == 'hexns' or gridtype == 'hexew':
            width = min(width, 2)
            hexspace = default.rjust(width // 2)
        default = default.rjust(width)
        printstr = ''
        for y in range(mins[1], maxs[1] + 1):
            if gridtype == 'hexns' or gridtype == 'hexew':
                printstr += ''.join([hexspace for _ in range(mins[1], maxs[1] - y)])
            for x in range(mins[0], maxs[0] + 1):
                if (x, y) in grid:
                    printstr += str(grid[(x, y)]).rjust(width)
                else:
                    printstr += default
            printstr += '\n'
        return printstr


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
    mins = [min((si[i] for si in grid)) for i in range(2)]
    maxs = [max((si[i] for si in grid)) for i in range(2)]
    printstr = ''
    for y in range(mins[1], maxs[1] + 1):
        if gridtype == 'hexns' or gridtype == 'hexew':
            printstr += ''.join([hexspace for i in range(mins[1], maxs[1] - y)])
        for x in range(mins[0], maxs[0] + 1):
            if (x, y) in grid:
                printstr += mark
            else:
                printstr += default
        printstr += '\n'
    return printstr


def printarray(grid, width):
    print(strarray(grid,width))


def strarray(grid, width):
    shape = grid.shape
    s = ''
    for i in range(shape[0]):
        for j in range(shape[1]):
            s += str(grid[i, j]).rjust(width)
        s += '\n'
    return s
