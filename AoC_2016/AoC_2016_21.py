import dancer


def scrambler(instructions, pw):
    pw = tuple(i for i in pw)
    for cmd, args in instructions:
        pw = cmd(args, pw)
    return ''.join(pw)


def swap_position(args, pw):
    x, y = min(args), max(args)
    return pw[:x] + (pw[y],) + pw[x + 1:y] + (pw[x],) + pw[y + 1:]


def swap_letter(args, pw):
    x, y = args
    x = pw.index(x)
    y = pw.index(y)
    return swap_position((x, y), pw)


def rotate(args, pw):
    x, = args
    return pw[x:] + pw[:x]


def rotate_letter(args, pw):
    x, = args
    x = pw.index(x)
    x = -x - 1 - (x >= 4)
    return rotate((x,), pw)


def rotate_letter_reverse(args, pw):
    x, = args
    x = pw.index(x)
    lpw = len(pw)
    for i in range(lpw):
        ige4 = i >= 4
        k = (2 * i + 1 + ige4) % lpw
        if k == x:
            break
    x = (i + 1 + ige4) % lpw
    return rotate((x,), pw)


def reverse(args, pw):
    x, y = args
    return pw[:x] + tuple(reversed(pw[x:y + 1])) + pw[y + 1:]


def move(args, pw):
    x, y = args
    if x < y:
        return pw[:x] + pw[x + 1:y + 1] + (pw[x],) + pw[y + 1:]
    else:
        return pw[:y] + (pw[x],) + pw[y:x] + pw[x + 1:]


def parse(input_string):
    instructions = []
    for line in input_string.split('\n'):
        line = line.split()
        if line[0] == 'swap':
            if line[1] == 'position':
                cmd = swap_position
                args = (int(line[2]), int(line[5]))
            else:
                cmd = swap_letter
                args = (line[2], line[5])
        elif line[0] == 'rotate':
            if line[1] == 'left':
                cmd = rotate
                args = (int(line[2]),)
            elif line[1] == 'right':
                cmd = rotate
                args = (-int(line[2]),)
            else:
                cmd = rotate_letter
                args = (line[6],)
        elif line[0] == 'reverse':
            cmd = reverse
            args = (int(line[2]), int(line[4]))
        elif line[0] == 'move':
            cmd = move
            args = (int(line[2]), int(line[5]))
        instructions.append((cmd, args))
    return tuple(instructions)


def unscramble(instructions):
    reverse_instructions = []
    for cmd, args in instructions:
        if cmd is rotate:
            args = (-args[0],)
        elif cmd is rotate_letter:
            cmd = rotate_letter_reverse
        elif cmd is move:
            args = (args[1], args[0])
        reverse_instructions.append((cmd, args))
    return tuple(reversed(reverse_instructions))


def main(input_string, verbose=False):
    instructions = parse(input_string)
    p1 = scrambler(instructions, 'abcdefgh')
    reverse_instructions = unscramble(instructions)
    p2 = scrambler(reverse_instructions, 'fbgdceah')
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=21, verbose=True)
