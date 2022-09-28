import DANCER


def run(instructions, switch=None):
    closed = set()
    idx = 0
    accumulator = 0
    switches = {'acc': 'acc', 'jmp': 'nop', 'nop': 'jmp'}
    while idx not in closed:
        closed.add(idx)
        if idx == len(instructions):
            return True, accumulator
        else:
            op, val = instructions[idx]
            if idx == switch:
                op = switches[op]
            if op == 'acc':
                accumulator += val
                idx += 1
            elif op == 'jmp':
                idx += val
            elif op == 'nop':
                idx += 1
    return False, accumulator


def main(input_string, verbose=False):
    instructions = [line.split() for line in input_string.split('\n')]
    instructions = [(op, int(val)) for op, val in instructions]
    _, p1 = run(instructions)
    for switch in range(len(instructions)):
        if instructions[switch][0]!='acc':
            terminate, accumulator = run(instructions, switch)
            if terminate:
                break
    p2 = accumulator
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=8, verbose=True)
