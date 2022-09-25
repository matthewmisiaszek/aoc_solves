import core


def main(input_string, verbose=False):
    f = input_string.split('\n')
    open_to_close = {'(': ')', '[': ']', '{': '}', '<': '>'}
    p1scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    p2scores = {')': '1', ']': '2', '}': '3', '>': '4'}
    p1, p2scorelist = 0, []

    for line in f:
        corrupt, closers = False, []
        for c in line:
            if c in open_to_close:
                closers.append(open_to_close[c])
            else:
                if closers.pop(-1) != c:
                    p1 += p1scores[c]
                    corrupt = True
                    break
        if not corrupt:
            closers.reverse()
            p2scorelist.append(int(''.join([p2scores[c] for c in closers]), 5))
    p2scorelist.sort()
    p2 = p2scorelist[len(p2scorelist) // 2]

    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2021, day=10, verbose=True)
