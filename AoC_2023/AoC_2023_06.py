import dancer
import math


def ways_to_win(t, d):
    return sum(((t - h) * h > d for h in range(t)))


def main(input_string, verbose=False):
    time = [int(i) for i in input_string.split('\n')[0].split()[1:]]
    distance = [int(i) for i in input_string.split('\n')[1].split()[1:]]
    p1 = math.prod((ways_to_win(t, d) for t, d in zip(time, distance)))

    time, dist = (int(i.split(':')[1]) for i in input_string.replace(' ', '').split('\n'))
    p2 = ways_to_win(time, dist)

    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=6, verbose=True)
