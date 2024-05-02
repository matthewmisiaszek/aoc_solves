import blitzen
from AoC_2019.intcode import Intcode


def operate_droid(droid, program, verbose):
    droid.load_state()
    droid.input.extend([ord(i) for i in program])
    droid.run()
    if verbose:
        print(''.join(chr(i) for i in droid.output[:-1]))
    return droid.output[-1]


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    spring_droid = Intcode(program)
    program = open(blitzen.root_path + '/AoC_2019/spring_droid_mk1').read()
    p1 = operate_droid(spring_droid, program, verbose)
    program = open(blitzen.root_path + '/AoC_2019/spring_droid_mk2').read()
    p2 = operate_droid(spring_droid, program, verbose)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=21, verbose=True)
