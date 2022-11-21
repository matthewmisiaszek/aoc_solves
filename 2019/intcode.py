from collections import defaultdict


class Intcode:
    def __init__(self, program, inputs=None, outputs=None):
        self.prgm = defaultdict(int)
        self.prgm.update({key: val for key, val in enumerate(program)})
        self.pntr = 0
        self.status = 1  # 0: halted, -1: awaiting input, 1: running normally
        self.rb = 0

        if inputs is None:
            inputs = []
        self.input = inputs
        if outputs is None:
            outputs = []
        self.output = outputs

        self.run_after = None

        # reset state
        self.prgm_reset = {}
        self.input_reset = {}
        self.output_reset = {}
        self.pntr_reset = {}
        self.status_reset = {}
        self.rb_reset = {}
        self.save_state()

    def save_state(self, key=0, sv_prgm=True, sv_in=True, sv_out=True, sv_pntr=True, sv_stat=True, sv_rb=True):
        if sv_prgm:
            self.prgm_reset[key] = self.prgm.copy()
        if sv_in:
            self.input_reset[key] = self.input.copy()
        if sv_out:
            self.output_reset[key] = self.output.copy()
        if sv_pntr:
            self.pntr_reset[key] = self.pntr
        if sv_stat:
            self.status_reset[key] = self.status
        if sv_rb:
            self.rb_reset[key] = self.rb

    def load_state(self, key=0, ld_prgm=True, ld_in=True, ld_out=True, ld_pntr=True, ld_stat=True, ld_rb=True):
        if ld_prgm:
            self.prgm = self.prgm_reset[key].copy()
        if ld_in:
            self.input.clear()
            self.input.extend(self.input_reset[key])
        if ld_out:
            self.output.clear()
            self.output.extend(self.output_reset[key])
        if ld_pntr:
            self.pntr = self.pntr_reset[key]
        if ld_stat:
            self.status = self.status_reset[key]
        if ld_rb:
            self.rb = self.rb_reset[key]

    def get(self, n_in, n_out):
        instruction = self.prgm[self.pntr]
        pmodes = instruction // 100
        for i in range(n_in + n_out):
            j = self.pntr + 1 + i
            v = self.prgm[j]
            mode = pmodes % 10
            pmodes //= 10
            is_in = i < n_in  # is it an input?
            match mode, is_in:
                case 0, True:
                    yield self.prgm[v]
                case 1, True:
                    yield v
                case 2, True:
                    yield self.prgm[v + self.rb]
                case 0, False:
                    yield v
                case 2, False:
                    yield v + self.rb
                case _:  # error
                    print('mode error: ', mode)
                    self.err()
        self.pntr += n_in + n_out + 1

    def run(self, in_app=None):
        if in_app is not None:
            self.input.append(in_app)
        if self.status != 0:  # if not halted...
            self.status = 1
            while self.status == 1:
                instruction = self.prgm[self.pntr]
                op = instruction % 100
                match op:
                    case 1:  # add
                        a, b, c = self.get(2, 1)
                        self.prgm[c] = a + b
                    case 2:  # multiply
                        a, b, c = self.get(2, 1)
                        self.prgm[c] = a * b
                    case 3:  # input
                        if self.input:
                            a, = self.get(0, 1)
                            self.prgm[a] = self.input.pop(0)
                        else:
                            self.status = -1
                    case 4:  # output
                        a, = self.get(1, 0)
                        self.output.append(a)
                    case 5:  # jump if true
                        a, b = self.get(2, 0)
                        if a != 0:
                            self.pntr = b
                    case 6:  # jump if false
                        a, b = self.get(2, 0)
                        if a == 0:
                            self.pntr = b
                    case 7:  # less than
                        a, b, c = self.get(2, 1)
                        self.prgm[c] = int(a < b)
                    case 8:  # equals
                        a, b, c = self.get(2, 1)
                        self.prgm[c] = int(a == b)
                    case 9:  # relative base offset
                        a, = self.get(1, 0)
                        self.rb += a
                    case 99:  # halt
                        self.status = 0
                    case _:  # error
                        self.err()
            if self.run_after is not None:
                ret = self.run_after()
                if ret is not None:
                    return ret
        if self.output:
            return self.output[-1]

    def err(self):
        print('error: invalid op code:', self.prgm[self.pntr])
        print('pointer: ', self.pntr)
        print('ilist: ', self.prgm)
