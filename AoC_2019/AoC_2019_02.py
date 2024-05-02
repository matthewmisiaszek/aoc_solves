import blitzen
from itertools import product
from AoC_2019.intcode import Intcode


def gravity_assist(computer, noun, verb):
    computer.load_state()
    computer.prgm[1] = noun
    computer.prgm[2] = verb
    computer.run()
    return computer.prgm[0]


def main(input_string, verbose=False):
    ilist = [int(i) for i in input_string.split(',')]
    computer = Intcode(ilist)
    p1 = gravity_assist(computer, 12, 2)
    for noun, verb in product(range(100), range(100)):
        if gravity_assist(computer, noun, verb) == 19690720:
            break
    p2 = 100 * noun + verb
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=2, verbose=True)
