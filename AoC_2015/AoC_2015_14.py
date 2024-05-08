import blitzen
import re


class Reindeer:
    def __init__(self, speed, endurance, rest):
        self.speed = int(speed)
        self.endurance = int(endurance)
        self.rest = int(rest)
        self.position = 0
        self.score = 0
        self.state = 'run'
        self.remaining = self.endurance

    def tick(self):
        if self.state == 'run':
            self.position += self.speed
        self.remaining -= 1
        if self.remaining <= 0:
            if self.state == 'run':
                self.state = 'rest'
                self.remaining = self.rest
            else:
                self.state = 'run'
                self.remaining = self.endurance
        return self.position

    def inc(self):
        self.score += 1


@blitzen.run
def main(input_string, verbose=False):
    pattern = r'.* can fly (\d*) km/s for (\d*) seconds, but then must rest for (\d*) seconds.'
    reindeer = {Reindeer(speed, endurance, rest)
                for speed, endurance, rest
                in re.findall(pattern, input_string)}
    time_limit = 2503
    for _ in range(time_limit):
        lead = max(deer.tick() for deer in reindeer)
        [deer.inc() for deer in reindeer if deer.position == lead]
    p1 = lead
    p2 = max(deer.score for deer in reindeer)
    return p1, p2

