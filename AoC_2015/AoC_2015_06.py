import dancer
import re


def main(input_string, verbose=False):
    size = 1000
    pattern = '(.*) (\d*),(\d*) through (\d*),(\d*)'
    p1 = {(x, y): 0 for x in range(size) for y in range(size)}
    p2 = p1.copy()
    for line in input_string.split('\n'):
        command, x1, y1, x2, y2 = re.match(pattern, line).groups()
        x1, y1, x2, y2 = (int(i) for i in (x1, y1, x2, y2))
        affected = {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}
        if command == 'turn on':
            for light in affected:
                p1[light] = 1
                p2[light] += 1
        elif command == 'turn off':
            for light in affected:
                p1[light] = 0
                if p2[light] > 0:
                    p2[light] -= 1
        elif command == 'toggle':
            for light in affected:
                p1[light] = 1 - p1[light]
                p2[light] += 2
    p1 = sum(p1.values())
    p2 = sum(p2.values())
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=6, verbose=True)
