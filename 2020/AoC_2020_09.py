import DANCER
from itertools import combinations


def part1(numbers):
    for i in range(26, len(numbers)):
        num = numbers[i]
        pre = set(numbers[i - 25:i])
        while pre:
            x = pre.pop()
            y = num - x
            if y in pre:
                break
        else:
            return num


def part2(numbers, p1):
    # find all numbers > p1.  They must not be in a range that sums to p1.
    # append -1 and len(numbers) to list to create ranges of possible continuous ranges
    bigs = [-1]+[i for i, n in enumerate(numbers) if n>p1]+[len(numbers)]
    for a,b in zip(bigs[:-1],bigs[1:]): # try one range at a time
        numbers2 = numbers[a+1:b]
        for i in range(len(numbers2)):
            for j in range(i+1,len(numbers2)):
                cont_range = numbers2[i:j + 1]
                crsum = sum(cont_range)
                if crsum > p1:
                    break
                elif crsum == p1:
                    return min(cont_range) + max(cont_range)


def main(input_string, verbose=False):
    numbers = tuple(int(i) for i in input_string.split('\n'))
    p1 = part1(numbers)
    p2 = part2(numbers, p1)
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=9, verbose=True)
