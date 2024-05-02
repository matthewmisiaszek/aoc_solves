import blitzen


def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]


def addi(regs, a, b, c):
    regs[c] = regs[a] + b


def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]


def muli(regs, a, b, c):
    regs[c] = regs[a] * b


def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]


def bani(regs, a, b, c):
    regs[c] = regs[a] & b


def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]


def bori(regs, a, b, c):
    regs[c] = regs[a] | b


def setr(regs, a, b, c):
    regs[c] = regs[a]


def seti(regs, a, b, c):
    regs[c] = a


def gtir(regs, a, b, c):
    regs[c] = int(a > regs[b])


def gtri(regs, a, b, c):
    regs[c] = int(regs[a] > b)


def gtrr(regs, a, b, c):
    regs[c] = int(regs[a] > regs[b])


def eqir(regs, a, b, c):
    regs[c] = int(a == regs[b])


def eqri(regs, a, b, c):
    regs[c] = int(regs[a] == b)


def eqrr(regs, a, b, c):
    regs[c] = int(regs[a] == regs[b])

def execute(input_string, reg0):
    fdict = {'addr':addr, 'addi':addi, 'mulr':mulr, 'muli':muli, 'banr':banr, 'bani':bani, 'borr':borr, 'bori':bori, 'setr':setr, 'seti':seti, 'gtir':gtir, 'gtri':gtri, 'gtrr':gtrr, 'eqir':eqir, 'eqri':eqri, 'eqrr':eqrr}
    f = input_string.split('\n')
    program = [line.split() for line in f]
    program = [[line[0]]+[int(i) for i in line[1:]] for line in program]
    ip = 0
    ipr = program[0][1]
    program=program[1:]
    regs = [0]*6
    regs[0]=reg0
    old0=0
    cc=0
    while ip>=0 and ip<len(program):

        if ipr is not None:
            regs[ipr] = ip
        fun, a, b, c = program[ip]
        fdict[fun](regs,a,b,c)
        if ipr is not None:
            ip = regs[ipr]+1
        if regs[0]!=old0:
            # print(regs)
            old0 = regs[0]
            cc+=1
            if cc>1:
                return regs[3]
        # print(ip, regs)
    # print(regs)

def predict(input_string, reg0):
    z=execute(input_string, reg0)
    hist=[0]
    for i in range(1, z + 1):
        if z%i==0:
            hist.append(hist[-1] + z // i)
    return hist[-1]

def main(input_string, verbose=False):
    p1 = predict(input_string, 0)
    p2 = predict(input_string, 1)
    return p1, p2

if __name__ == "__main__":
    blitzen.run(main, year=2018, day=19, verbose=True)
