import blitzen
import re


class StrangeDevice:
    def __init__(self, input_string, overrides=None):
        a, b, c, prog = re.match(r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([\d,]+)', input_string).groups()
        self.progs = prog
        self.regs = {k: int(v) for k, v in zip('ABC', (a, b, c))}
        if overrides is not None:
            self.regs.update(overrides)
        self.prog = tuple(int(i) for i in prog.split(','))
        self.pointer = 0
        self.output = []
        self.instructions = [
            self.adv, self.bxl, self.bst, self.jnz,
            self.bxc, self.out, self.bdv, self.cdv,
        ]
        while 0 <= self.pointer < len(self.prog) - 1:

            f, o = self.prog[self.pointer: self.pointer + 2]
            self.instructions[f](o)
            self.pointer += 2
        self.result = ','.join(str(i) for i in self.output)

    def combo(self, o):
        match o:
            # Combo operands 0 through 3 represent literal values 0 through 3.
            case o if 0 <= o <= 3:
                return o
            # Combo operand 4 represents the value of register A.
            case 4:
                return self.regs['A']
            # Combo operand 5 represents the value of register B.
            case 5:
                return self.regs['B']
            # Combo operand 6 represents the value of register C.
            case 6:
                return self.regs['C']
            # Combo operand 7 is reserved and will not appear in valid programs.
            case 7:
                raise Exception('Combo operand 7 is reserved and will not appear in valid programs.')

    # The eight instructions are as follows:
    def adv(self, o):
        """ The adv instruction (opcode 0) performs division.

        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then written to the A register.
        """
        self.regs['A'] = self.regs['A'] // (2 ** self.combo(o))

    def bxl(self, o):
        """ The bxl instruction (opcode 1)

        calculates the bitwise XOR of register B and the instruction's literal operand,
        then stores the result in register B.
        """
        self.regs['B'] = self.regs['B'] ^ o

    def bst(self, o):
        """ The bst instruction (opcode 2)

        calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
        then writes that value to the B register.
        """
        self.regs['B'] = self.combo(o) % 8

    def jnz(self, o):
        """ The jnz instruction (opcode 3)

        does nothing if the A register is 0.
        However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand;
        if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
        """
        if self.regs['A'] != 0:
            self.pointer = o - 2

    def bxc(self, o):
        """ The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,

        then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.regs['B'] = self.regs['B'] ^ self.regs['C']

    def out(self, o):
        """ The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.

        (If a program outputs multiple values, they are separated by commas.)
        """
        self.output.append(self.combo(o) % 8)

    def bdv(self, o):
        """ The bdv instruction (opcode 6)

        works exactly like the adv instruction except that the result is stored in the B register.
        (The numerator is still read from the A register.)
        """
        self.regs['B'] = self.regs['A'] // (2 ** self.combo(o))

    def cdv(self, o):
        """ The cdv instruction (opcode 7)

        works exactly like the adv instruction except that the result is stored in the C register.
        (The numerator is still read from the A register.)
        """
        self.regs['C'] = self.regs['A'] // (2 ** self.combo(o))


@blitzen.run
def main(input_string, verbose=False):
    s = StrangeDevice(input_string)
    p1 = s.result
    q = {(a:=0, s.prog)}  # you could also do this recursively...
    while q:
        a, prog = min(q) # a: initial value reg a: prog: the piece of the program still to be matched
        q.discard((a, prog))
        if not prog:
            # full match achieved! break
            break
        for n in range(8):
            # what should the next 3 bits be to yield the next value in the program?
            s = StrangeDevice(input_string, {'A': a * 8 + n})
            if s.output[0] == prog[-1]:
                # these 3 bits work... move on to the next 3
                q.add((a*8+n, prog[:-1]))
    p2 = a
    return p1, p2
