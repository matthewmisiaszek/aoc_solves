import dancer


class Instruction:
    def __init__(self, string):
        reg, inc, val, _, creg, op, cval = string.split()
        self.reg = reg
        self.val = int(val) if inc == 'inc' else -int(val)
        self.creg = creg
        self.op = op
        self.cval = int(cval)

    def execute(self, registers):
        if self.comp(registers):
            reg = self.reg
            if reg not in registers:
                registers[reg] = 0
            registers[self.reg] += self.val

    def comp(self, registers):
        creg = self.creg
        if creg not in registers:
            registers[creg] = 0
        if self.op == '>':
            return registers[creg] > self.cval
        elif self.op == '>=':
            return registers[creg] >= self.cval
        elif self.op == '==':
            return registers[creg] == self.cval
        elif self.op == '<=':
            return registers[creg] <= self.cval
        elif self.op == '<':
            return registers[creg] < self.cval
        elif self.op == '!=':
            return registers[creg] != self.cval
        else:
            return False


def main(input_string, verbose=False):
    instructions = [Instruction(line) for line in input_string.split('\n')]
    registers = {}
    maxreg = 0
    for instruction in instructions:
        instruction.execute(registers)
        maxreg = max(maxreg, *registers.values())
    p1 = max(registers.values())
    p2 = maxreg
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=8, verbose=True)
