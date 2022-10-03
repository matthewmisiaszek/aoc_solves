import dancer
import string
from collections import deque


def program(instructions, pid=0, queues=None, sent=None, part1=False):
    registers = {c: 0 for c in string.ascii_lowercase}
    registers['p'] = pid
    i = 0
    mulcount = 0
    while 0 <= i < len(instructions):
        instruction = instructions[i]
        cmd = instruction[0]
        x = instruction[1]
        if cmd == 'snd':
            if part1:
                registers['snd'] = registers[x]
            else:
                queues[pid].append(registers[x])
                sent[pid] += 1
        elif cmd == 'rcv':
            if part1:
                if registers[x] > 0:
                    yield registers['snd']
            else:
                for tf in (True, False):
                    if queues[1 - pid]:
                        registers[x] = queues[1 - pid].popleft()
                        break
                    else:
                        yield tf
        else:
            y = instruction[2]
            if y not in string.ascii_lowercase:
                y = int(y)
            else:
                y = registers[y]
            if cmd == 'set':
                registers[x] = y
            elif cmd == 'add':
                registers[x] += y
            elif cmd == 'sub':
                registers[x] -= y
            elif cmd == 'mul':
                registers[x] *= y
                mulcount += 1
            elif cmd == 'mod':
                registers[x] %= y
            elif cmd == 'jgz':
                if x not in string.ascii_lowercase:
                    x = int(x)
                else:
                    x = registers[x]
                if x > 0:
                    i += y - 1
            elif cmd == 'jnz':
                if x not in string.ascii_lowercase:
                    x = int(x)
                else:
                    x = registers[x]
                if x != 0:
                    i += y - 1
        i += 1
    yield mulcount


def part2(instructions):
    queues = [deque(), deque()]
    sent = [0, 0]
    programs = [program(instructions, i, queues, sent) for i in (0, 1)]
    while all(next(p) for p in programs):
        pass
    return sent[1]


def main(input_string, verbose=False):
    instructions = tuple(line.split() for line in input_string.split('\n'))
    p1 = next(program(instructions, part1=True))
    p2 = part2(instructions)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=18, verbose=True)
