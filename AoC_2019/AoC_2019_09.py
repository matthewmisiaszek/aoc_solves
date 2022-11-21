import dancer
from AoC_2019.intcode import Intcode


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    computer = Intcode(program, [1, 2])
    p1 = computer.run()
    computer.load_state(ld_in=False)
    p2 = computer.run()
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=9, verbose=True)
