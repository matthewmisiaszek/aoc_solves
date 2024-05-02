import blitzen
from AoC_2019.intcode import Intcode
from itertools import permutations


def build_amps(n_amps, program):
    inputs = [[] for _ in range(n_amps)]
    outputs = inputs[1:] + inputs[0:1]
    amps = [Intcode(program, i, o) for i, o in zip(inputs, outputs)]
    for amp1, amp2 in zip(amps, amps[1:]):
        amp1.run_after = amp2.run
    return amps


def run_amps(amps, phases):
    for amp, phase in zip(amps, phases):
        amp.load_state(ld_out=False)
        amp.input.append(phase)
    amps[0].input.append(0)
    return amps[0].run()


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    n_amps = 5
    amps = build_amps(n_amps, program)

    p1 = max(run_amps(amps, phases) for phases in permutations(range(n_amps)))

    amps[-1].run_after = amps[0].run  # rewire the amplifiers into a feedback loop

    p2 = max(run_amps(amps, phases) for phases in permutations(range(5, 5 + n_amps)))
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2019, day=7, verbose=True)
