import blitzen
import math


class Module:
    def __init__(self, line, button):
        self.button = button
        fname, outputs = line.split(' -> ')
        self.type = fname[0]
        self.name = fname[self.type != 'b':]
        self.outputs = tuple(outputs.split(', '))
        self.button.mdict[self.name] = self
        self.state = False
        self.memory = {}
        self.freqs = {}

    def rollup(self):
        for module in self.outputs:
            if module in self.button.mdict:
                self.button.mdict[module].memory[self.name] = False

    def pulse(self, sender, high):
        self.button.pulsecount[high] += 1
        self.memory[sender] = high
        if high and sender not in self.freqs:
            self.freqs[sender] = self.button.pushcount
        if self.type == '%':
            if high:
                return
            self.state = not self.state
        elif self.type == '&':
            self.state = not all(self.memory.values())
        elif self.type == 'b':
            self.state = high
        for output in self.outputs:
            self.button.queue.append((self.name, output, self.state))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name


class Button:
    def __init__(self):
        self.queue = []
        self.qi = 0
        self.pushcount = 0
        self.mdict = {}
        self.pulsecount = [0, 0]

    def push(self):
        self.pushcount += 1
        self.queue.append(('button', 'broadcaster', False))
        while self.qi < len(self.queue):
            sender, receiver, high = self.queue[self.qi]
            self.mdict[receiver].pulse(sender, high)
            self.qi += 1

    def __hash__(self):
        return hash('button')


def main(input_string, verbose=False):
    button = Button()
    for line in input_string.split('\n'):
        Module(line, button)
    rx = Module('%rx -> ', button)
    for module in button.mdict.values():
        module.rollup()
    for _ in range(1000):
        button.push()
    p1 = button.pulsecount[0] * button.pulsecount[1]
    rx_parent = button.mdict[tuple(rx.memory.keys())[0]]
    while set(rx_parent.memory) - set(rx_parent.freqs):
        button.push()
    p2 = math.lcm(*rx_parent.freqs.values())
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=20, verbose=True)
