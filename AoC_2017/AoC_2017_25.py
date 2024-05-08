import blitzen
import re


@blitzen.run
def main(input_string, verbose=False):
    initial_pattern = 'Begin in state (.).\nPerform a diagnostic checksum after (.*) steps.'
    state_pattern = 'In state (.):\n' \
                    '  If the current value is (.):\n' \
                    '    - Write the value (.).\n' \
                    '    - Move one slot to the (right|left).\n' \
                    '    - Continue with state (.).\n' \
                    '  If the current value is (.):\n' \
                    '    - Write the value (.).\n' \
                    '    - Move one slot to the (right|left).\n' \
                    '    - Continue with state (.).'
    states = {}
    moves = {'right': 1, 'left': -1}
    for state, c1, v1, m1, s1, c2, v2, m2, s2 in re.findall(state_pattern, input_string):
        c1, v1, c2, v2 = (int(i) for i in (c1, v1, c2, v2))
        m1, m2 = (moves[i] for i in (m1, m2))
        states[state] = {c1: (v1, m1, s1), c2: (v2, m2, s2)}
    ((state, steps),) = re.findall(initial_pattern, input_string)
    tape = set()
    idx = 0
    steps = int(steps)
    for i in range(steps):
        val, move, state = states[state][idx in tape]
        if val:
            tape.add(idx)
        else:
            tape.discard(idx)
        idx += move
    p1 = len(tape)
    p2 = blitzen.holiday_greeting
    return p1, p2

