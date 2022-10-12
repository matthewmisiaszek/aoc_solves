class AsmBny:
    def __init__(self, instructions, initial=None, return_reg='a'):
        if initial is None:
            initial = {}
        commands = {'cpy': self.cpy, 'inc': self.inc, 'dec': self.dec, 'jnz': self.jnz, 'tgl':self.tgl, 'out':self.out}
        self.instructions = []
        self.constants = set()
        for line in instructions.split('\n'):
            line = line.split()
            cmd = line.pop(0)
            cmd = commands[cmd]
            args = tuple(line)
            for arg in args:
                if arg not in initial:
                    if arg.lstrip('-').isdigit():
                        initial[arg] = int(arg)
                        self.constants.add(arg)
                    else:
                        initial[arg] = 0
            self.instructions.append((cmd, args))
        self.instructions = self.instructions
        self.regs = initial
        self.regs_reset = initial.copy()
        self.pointer = 0
        self.len_ins = len(self.instructions)
        self.return_reg = return_reg

    def reset(self):
        self.regs = self.regs_reset.copy()
        self.pointer=0

    def cpy(self, args):
        x, y = args
        if y not in self.constants:
            self.regs[y] = self.regs[x]

    def inc(self, args):
        x, = args
        if x not in self.constants:
            self.regs[x] += 1

    def dec(self, args):
        x, = args
        if x not in self.constants:
            self.regs[x] -= 1

    def jnz(self, args):
        x, y = args
        if self.regs[x] != 0:
            self.pointer += self.regs[y] - 1

    def run(self):
        while 0 <= self.pointer < self.len_ins:
            cmd, args = self.instructions[self.pointer]
            cmd(args)
            # print(self.pointer, self.regs)
            self.pointer += 1
        return self.regs[self.return_reg]

    def tgl(self, args):
        a, = args
        a = self.regs[a]
        if 0<=a<self.len_ins:
            cmd, args = self.instructions[a]
            if len(args)==1:
                if cmd==self.inc:
                    cmd = self.dec
                else:
                    cmd = self.inc
            elif len(args)==2:
                if cmd==self.jnz:
                    cmd = self.cpy
                else:
                    cmd=self.jnz
            self.instructions[a]=(cmd, args)

    def out(self, args):
        x, = args
        self.regs['out']+=str(self.regs[x])
        if len(self.regs['out'])==8:
            self.pointer=-2
