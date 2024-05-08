import blitzen


def look_n_say(sequence, iterations):
    for _ in range(iterations):
        new_seq = ''
        count = 0
        letter = sequence[0]
        for c in sequence + '_':
            if c == letter:
                count += 1
            else:
                new_seq += str(count) + letter
                letter = c
                count = 1
        sequence = new_seq
    return sequence


@blitzen.run
def main(input_string, verbose=False):
    p1 = len(look_n_say(input_string, 40))
    p2 = len(look_n_say(input_string, 50))
    return p1, p2

