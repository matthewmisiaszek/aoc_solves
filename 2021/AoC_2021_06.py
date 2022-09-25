import core


class lanternFish:
    def __init__(self, file_o_fish):
        self.zero = 0
        self.reset = 7
        self.new = 9
        fishlist = [int(i) for i in file_o_fish.split(',')]
        self.schools = [fishlist.count(j) for j in range(self.new)]

    def ticks(self, n):
        for tick in range(n):
            self.schools[(self.zero + self.reset) % self.new] += self.schools[self.zero]
            self.zero = (self.zero + 1) % self.new
        return sum(self.schools)


def main(input_string, verbose=False):
    fish = lanternFish(input_string)
    p1 = fish.ticks(80)
    p2 = fish.ticks(256 - 80)

    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2021, day=6, verbose=True)
