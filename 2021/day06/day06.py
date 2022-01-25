class lanternFish:
    def __init__(self, file_o_fish):
        self.zero = 0
        self.reset = 7
        self.new = 9
        fishlist = [int(i) for i in open(file_o_fish).read().split(',')]
        self.schools = [fishlist.count(j) for j in range(self.new)]

    def ticks(self, n):
        for tick in range(n):
            self.schools[(self.zero + self.reset) % self.new] += self.schools[self.zero]
            self.zero = (self.zero + 1) % self.new
        return sum(self.schools)


def main(input_file='input.txt', verbose=False):
    fish = lanternFish(input_file)
    p1 = fish.ticks(80)
    p2 = fish.ticks(256 - 80)

    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
