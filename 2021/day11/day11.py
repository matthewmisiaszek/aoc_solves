class Garden:
    def __init__(self, inputstr):
        self.octopi, self.flash = {}, []
        self.steps, self.flashes, self.flashpoint = 0, 0, 9
        for octopussy, line in enumerate(inputstr):
            for octopusx, c in enumerate(line):
                self.octopi[(octopusx, octopussy)] = int(c)
        self.octolist = tuple(self.octopi.keys())
        self.octofriends = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    def increment(self, octopus):
        if octopus in self.octopi:
            if self.octopi[octopus] >= self.flashpoint:
                self.flash.append(octopus)
                self.octopi.pop(octopus)
            else:
                self.octopi[octopus] += 1

    def step(self):
        self.flash, o = [], 0
        for octopus in self.octolist:
            self.increment(octopus)
        while o < len(self.flash):
            for offset in self.octofriends:
                self.increment((tuple(map(sum, zip(self.flash[o], offset)))))
            o += 1
        self.flashes += len(self.flash)
        for octopus in self.flash:
            self.octopi[octopus] = 0
        self.steps += 1


def main(input_file='input.txt', verbose=False):
    f = open(input_file).read().split('\n')
    garden = Garden(f)
    for i in range(100):
        garden.step()
    p1 = garden.flashes
    while len(garden.flash) < len(garden.octolist):
        garden.step()
    p2 = garden.steps
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)
