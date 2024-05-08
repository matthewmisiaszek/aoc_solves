import blitzen
import string


def dance(programs, moves):
    for move in moves:
        if move[0] == 's':
            n = int(move[1:])
            programs[:] = programs[-n:] + programs[:-n]
        else:
            if move[0] == 'x':
                a, b = (int(i) for i in move[1:].split('/'))
            elif move[0] == 'p':
                a, b = (programs.index(i) for i in move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
    return ''.join(programs)


@blitzen.run
def main(input_string, verbose=False):
    programs = [i for i in string.ascii_lowercase[:16]]
    moves = input_string.split(',')
    cache = []
    c0 = dance(programs, moves)
    cache.append(c0)
    while True:
        c = dance(programs, moves)
        if c == c0:
            break
        else:
            cache.append(c)
    p1 = c0
    p2 = cache[1000000000 % len(cache) - 1]
    return p1, p2

