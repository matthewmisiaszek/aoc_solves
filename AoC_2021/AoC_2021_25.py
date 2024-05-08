import blitzen


@blitzen.run
def main(input_string, verbose=False):
    seafloor, motion, step = input_string.split('\n'), True, 0
    bx, by = (len(seafloor[0]), len(seafloor))
    herds = [{(x, y) for y, line in enumerate(seafloor) for x, c in enumerate(line) if c == v} for v in '>v']
    moves = [{(x, y): ((x + (1 - d)) % bx, (y + d) % by) for x in range(bx) for y in range(by)} for d in range(2)]
    while motion:
        step, motion = step + 1, False
        for i, (herd, move) in enumerate(zip(herds, moves)):
            herd = {move[cuc] if move[cuc] not in herd and move[cuc] not in herds[1 - i] else cuc for cuc in herd}
            motion, herds[i] = motion or herd != herds[i], herd
    p1=step
    p2=blitzen.holiday_greeting
    return p1,p2
