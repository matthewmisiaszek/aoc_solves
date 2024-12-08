import blitzen
# credit to @mina@berlin.social for the idea of working backwards and eliminating operator combinations that don't work.


def fadd(a, b):
    return b - a


def fmul(a, b):
    if b % a == 0:
        return b // a
    return False


def fconc(a, b):
    a, b = str(a), str(b)
    la = len(a)
    if b[-la:] == a:
        ret = b[:-la]
        return int(ret) if ret else 0
    return False


def recursive_safety_check(id, vals, operators):
    if len(vals) == 1:
        return vals[0] == id
    for operator in operators:
        new_id = operator(vals[-1], id)
        if new_id and recursive_safety_check(new_id, vals[:-1], operators):
            return True
    return False


def safety_check(calibrations, operators):
    calibration_result = 0
    for id, vals in calibrations:
        if recursive_safety_check(id, vals, operators):
            calibration_result += id
    return calibration_result


@blitzen.run
def main(input_string, verbose=False):
    calibrations = [line.split(': ') for line in input_string.split('\n')]
    calibrations = [(int(id), [int(i) for i in vals.split()]) for id, vals in calibrations]
    p1 = safety_check(calibrations, (fadd, fmul))
    p2 = safety_check(calibrations, (fadd, fmul, fconc))
    return p1, p2

