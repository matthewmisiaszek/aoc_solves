import dancer


class Computer:
    def __init__(self, instructions, reg_init=None):
        instructions = instructions.replace(',', '')
        self.regs = {'a': 0, 'b': 0}
        if reg_init is not None:
            self.regs.update(reg_init)
        self.regs_init = self.regs.copy()
        self.pointer = 0
        self.instructions = []
        funs = {'hlf': self.hlf,
                'tpl': self.tpl,
                'inc': self.inc,
                'jmp': self.jmp,
                'jie': self.jie,
                'jio': self.jio}
        for line in instructions.split('\n'):
            line = line.split()
            cmd = funs[line[0]]
            args = tuple(line[1:])
            self.instructions.append((cmd, args))

    def run(self, ret):
        while 0 <= self.pointer < len(self.instructions):
            cmd, args = self.instructions[self.pointer]
            cmd(args)
            self.pointer += 1
        return self.regs[ret]

    def reset(self, reg_init=None):
        self.pointer = 0
        self.regs = self.regs_init.copy()
        if reg_init is not None:
            self.regs.update(reg_init)

    def hlf(self, args):
        r, = args
        self.regs[r] *= .5

    def tpl(self, args):
        r, = args
        self.regs[r] *= 3

    def inc(self, args):
        r, = args
        self.regs[r] += 1

    def jmp(self, args):
        r, = args
        self.pointer += int(r) - 1

    def jie(self, args):
        r, offset = args
        if self.regs[r] % 2 == 0:
            self.jmp((offset,))

    def jio(self, args):
        r, offset = args
        if self.regs[r] == 1:
            self.jmp((offset,))


def main(input_string, verbose=False):
    computer = Computer(input_string)
    p1 = computer.run('b')
    computer.reset({'a': 1})
    p2 = computer.run('b')
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=23, verbose=True)
