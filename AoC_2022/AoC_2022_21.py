import blitzen


class Monkey:
    def __init__(self, mdict, line):
        self.mdict = mdict
        self.line = line
        self.i_wait_for = []
        self.value = None
        self.op = None
        line = line.split()
        self.name = line[0][:-1]
        self.mdict[self.name] = self
        if len(line) == 2:
            self.value = int(line[1])
        else:
            self.i_wait_for.extend([line[1], line[3]])
            self.op = line[2]

    def eval(self):
        if self.value is not None:
            return self.value
        a, b = (self.mdict[monkey].eval() for monkey in self.i_wait_for)
        match self.op:
            case '+':
                return a + b
            case '*':
                return a * b
            case '-':
                return a - b
            case '/':
                return a / b


ROOT = 'root'
HUMN = 'humn'


@blitzen.run
def main(input_string, verbose=False):
    mdict = {}
    for line in input_string.split('\n'):
        Monkey(mdict, line)
    p1 = int(mdict[ROOT].eval())
    mdict[HUMN].value = -1j
    mdict[ROOT].op = '-'
    p2 = mdict[ROOT].eval()
    p2 = int(p2.real / p2.imag)
    return p1, p2

