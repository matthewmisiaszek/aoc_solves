import blitzen

ABC = 'ABC'
XYZ = 'XYZ'
MOD = 3
FACT = 3


@blitzen.run
def main(input_string, verbose=False):
    p1, p2 = 0, 0
    for line in input_string.split('\n'):
        opp = ABC.find(line[0])
        you = XYZ.find(line[2])
        p1 += you + 1 + (you - opp + 1) % MOD * FACT
        p2 += you * FACT + 1 + (opp + you - 1) % MOD
    return p1, p2

