import blitzen
import re
from itertools import combinations


class Gate:
    def __init__(self, a, op, b, gates):
        self.ins = {a, b}
        self.op = op
        self.gates = gates
        self.val = None

    def eval(self):
        if self.val is None:
            a, b = (self.gates[i].eval() for i in self.ins)
            match self.op:
                case 'AND':
                    self.val = a & b
                case 'OR':
                    self.val = a | b
                case 'XOR':
                    self.val = a ^ b
        return self.val


class Const:
    def __init__(self, val):
        self.ins = ()
        self.val = val

    def eval(self):
        return self.val


def check_gates(gates):
    reverse_gates = {gate: {} for gate in gates}  # allow looking gates up by their inputs
    known = set()  # gates that definitely have the correct outputs
    for name, gate in gates.items():
        if gate.ins == ():  # consider constants as known
            known.add(name)
    for name, gate in gates.items():
        for i in gate.ins:
            reverse_gates[i][gate.op] = name
    # find half adder for first bit
    XOR0 = reverse_gates['x00']['XOR']
    if XOR0 == 'z00':
        known.add(XOR0)
    AND0 = reverse_gates['x00']['AND']
    carry = AND0
    for bit in range(1, 45):
        XOR1 = reverse_gates[f'x{bit:02}']['XOR']  # XOR for first half adder takes input from xBB (and yBB)
        if 'XOR' not in reverse_gates[XOR1]:
            continue  # no second XOR, something is wrong, move to next bit
        XOR2 = reverse_gates[XOR1]['XOR']  # XOR connected to XOR1 must be second half adder XOR
        z = f'z{bit:02}'
        if XOR2 != z:
            continue  # if this second XOR doesn't output to correct z, something is wrong, continue
        known.update({XOR1, XOR2})  # everything looks good so far, consider these outputs 'known'
        if gates[XOR2].ins == {XOR1, carry}:
            known.add(carry)  # carry bit is the second input for XOR2, it's also known now
        AND1 = reverse_gates[f'x{bit:02}']['AND']  # AND for first half adder
        if 'AND' not in reverse_gates[XOR1]:
            continue  # second half adder AND not found, something is wrong, move to next bit
        AND2 = reverse_gates[XOR1]['AND']  # get AND for second half adder
        if 'OR' not in reverse_gates[AND1]:
            continue  # OR is not found, something is wrong, move to next bit
        OR = reverse_gates[AND1]['OR']
        if gates[OR].ins != {AND1, AND2}:  # OR should take AND1, AND2 as inputs
            continue  # if not, something is wrong, move to next bit
        known.update({AND1, AND2})  # these outputs are considered known
        carry = OR  # OR is the carry in for the next bit
    return set(gates) - known  # return unknown (all gates not in known)


@blitzen.run
def main(input_string, verbose=False):
    gates = {}
    for a, op, b, out in re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', input_string):
        gates[out] = Gate(a, op, b, gates)
    for name, val in re.findall(r'([xy]\d{2}): ([01])', input_string):
        gates[name] = Const(int(val))
    p1 = sum(gates[f'z{i:02}'].eval() * 2 ** i for i in range(46))
    swaps = set()
    for _ in range(4):  # perform 4 swaps
        unknown = check_gates(gates)  # all gates not yet confirmed to have the right outputs
        for a, b in combinations(unknown, 2):  # try every combination of two gates
            gates[a], gates[b] = gates[b], gates[a]  # swap outputs of those two gates
            revised_unknown = check_gates(gates)  # check for unknowns.
            if a not in revised_unknown and b not in revised_unknown:  # Are these gates no longer unknown?
                swaps.update({a, b})  # Great! That worked.  Note the swap and move forward.
                break
            gates[a], gates[b] = gates[b], gates[a]  # no, that didn't help.  undo the swap and keep looking
    p2 = ','.join(sorted(swaps))
    return p1, p2
