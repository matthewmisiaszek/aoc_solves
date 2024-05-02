class AsmBny:
    def __init__(self, instructions, initial=None, return_reg='a'):
        if initial is None:
            initial = {}
        commands = {'cpy': self.cpy, 'inc': self.inc,
                    'dec': self.dec, 'jnz': self.jnz,
                    'tgl': self.tgl, 'out': self.out}
        self.instructions = []
        for line in instructions.split('\n'):
            line = line.split()
            cmd = line.pop(0)
            cmd = commands[cmd]
            args = []
            for arg in line:
                if arg.lstrip('-').isdigit():
                    args.append(int(arg))
                    args.append(True)
                else:
                    args.append(arg)
                    args.append(False)
                    if arg not in initial:
                        initial[arg] = 0
            self.instructions.append((cmd, tuple(args)))
        self.regs = initial
        self.regs_reset = initial.copy()
        self.pointer = 0
        self.len_ins = len(self.instructions)
        self.return_reg = return_reg
        self.hist = set()

    def reset(self):
        self.regs = self.regs_reset.copy()
        self.pointer = 0
        self.hist = set()

    def cpy(self, args):
        x, xi, y, yi = args
        if not yi:
            if not xi:
                x = self.regs[x]
            self.regs[y] = x

    def inc(self, args):
        x, xi = args
        if not xi:
            self.regs[x] += 1

    def dec(self, args):
        x, xi = args
        if not xi:
            self.regs[x] -= 1

    def jnz(self, args):
        x, xi, y, yi = args
        if not xi:
            x = self.regs[x]
        if x != 0:
            if not yi:
                y = self.regs[y]
            self.pointer += y - 1

    def run(self):
        while 0 <= self.pointer < self.len_ins:
            cmd, args = self.instructions[self.pointer]
            cmd(args)
            # print(self.pointer, self.regs)
            self.pointer += 1
        return self.regs[self.return_reg]

    def tgl(self, args):
        x, xi = args
        if not xi:
            x = self.regs[x]
        x += self.pointer
        if 0 <= x < self.len_ins:
            cmd, args = self.instructions[x]
            if cmd == self.inc:
                cmd = self.dec
            elif cmd == self.jnz:
                cmd = self.cpy
            elif cmd == self.cpy:
                cmd = self.jnz
            elif cmd in {self.dec, self.tgl}:
                cmd = self.inc
            self.instructions[x] = (cmd, args)

    def out(self, args):
        x, xi = args
        if not xi:
            x = self.regs[x]
        if x == len(self.hist) % 2:
            rhist = tuple(sorted(self.regs.items()))
            if rhist in self.hist:
                self.regs['out'] = True
                self.pointer = -2
            else:
                self.hist.add(rhist)
        else:
            self.regs['out'] = False
            self.pointer = -2
