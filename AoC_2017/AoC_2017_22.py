import blitzen
from donner import printer
from donner import graph, spatial as sp


def simulate(grid, start, states, turns, bursts, verbose=False):
    infection_count = 0
    loc = start
    direction = sp.NORTH
    for burst in range(bursts):
        if loc not in grid:
            grid[loc] = clean
        turn = turns[grid[loc]]
        if turn == right:
            direction = direction.right()
        elif turn == left:
            direction = direction.left()
        elif turn == back:
            direction *= -1
        new_state = states[grid[loc]]
        if new_state == infected:
            infection_count += 1
        grid[loc] = new_state
        loc += direction
    if verbose:
        printer.printdict(grid)
        print('')
    return infection_count


def main(input_string, verbose=False):
    grid = graph.text_to_dict(input_string)
    start = sp.Point(len(input_string.split('\n')[0]) // 2, len(input_string.split('\n')) // 2)

    states = {infected: clean,
              clean: infected}
    turns = {infected: right,
             clean: left}
    bursts = 10000
    p1 = simulate(grid.copy(), start, states, turns, bursts, verbose)

    states = {clean: weakened,
              weakened: infected,
              infected: flagged,
              flagged: clean}
    turns = {clean: left,
             weakened: None,
             infected: right,
             flagged: back}
    bursts = 10000000
    p2 = simulate(grid.copy(), start, states, turns, bursts, verbose)
    return p1, p2


infected = '#'
clean = '.'
weakened = 'W'
flagged = 'F'
right = 'right'
left = 'left'
back = 'back'

if __name__ == "__main__":
    blitzen.run(main, year=2017, day=22, verbose=True)
