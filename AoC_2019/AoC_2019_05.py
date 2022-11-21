import dancer
from AoC_2019.intcode import Intcode


def main(input_string, verbose=False):
    ilist = [int(i) for i in input_string.split(',')]
    computer = Intcode(ilist, inputs=[1])
    p1 = computer.run()
    computer.load_state()
    computer.input = [5]
    p2 = computer.run()
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=5, verbose=True)
