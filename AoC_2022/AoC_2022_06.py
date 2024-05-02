import blitzen


def find_sequence(datastream, characters):
    for i in range(len(datastream)):
        if len(set(datastream[i:i + characters])) == characters:
            return i + characters


def main(input_string, verbose=False):
    p1 = find_sequence(input_string, 4)
    p2 = find_sequence(input_string, 14)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=6, verbose=True)
