import blitzen


def find_sequence(datastream, characters):
    for i in range(len(datastream)):
        if len(set(datastream[i:i + characters])) == characters:
            return i + characters


@blitzen.run
def main(input_string, verbose=False):
    p1 = find_sequence(input_string, 4)
    p2 = find_sequence(input_string, 14)
    return p1, p2

