import dancer


def main(input_string, verbose=False):
    elves = sorted(sum(int(food) for food in elf.split('\n')) for elf in input_string.split('\n\n'))
    p1 = elves[-1]
    p2 = sum(elves[-3:])
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=1, verbose=True)
