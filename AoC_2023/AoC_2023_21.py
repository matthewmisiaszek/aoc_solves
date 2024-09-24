import blitzen
from donner import graph, spatial, bfsqueue


class Garden:
    def __init__(self, input_string):
        self.garden_dict = graph.text_to_dict(input_string, exclude='#')
        self.plots = set(self.garden_dict.keys())
        self.start, self.plotsize = spatial.bounds(self.plots, pad=1)
        for self.start, char in self.garden_dict.items():
            if char == 'S':
                break
        self.delta = {}
        self.maxdelta = 0
        queue = bfsqueue.BFSQ(self.start)
        for plot, steps in queue:
            delta = steps - plot.manhattan(self.start)
            self.maxdelta = max(self.maxdelta, delta)
            relative = self.relative(plot)
            if relative in self.delta and self.delta[relative] == delta:
                continue
            self.delta[relative] = delta
            for direction in spatial.ENWS:
                new_plot = plot + direction
                if new_plot % self.plotsize in self.plots:
                    queue.add(new_plot, steps + 1)
        self.delta.update(queue.closed)
        self.plots &= set(queue.closed.keys())

    def checktile(self, tile, steps_goal):
        tile_origin = tile * self.plotsize
        tile_score = 0
        for plot in self.plots:
            plot += tile_origin
            if plot in self.delta:
                psteps = self.delta[plot]
            else:
                psteps = self.delta[self.relative(plot)] + plot.manhattan(self.start)
            tile_score += psteps <= steps_goal and psteps % 2 == steps_goal % 2
        return tile_score
    
    def relative(self, plot):
        relative_plot = plot % self.plotsize
        relative_tile = plot.__floordiv__(self.plotsize).sign()
        return relative_plot, relative_tile
    
    def part1(self, steps_goal):
        return self.checktile(spatial.Point(), steps_goal)
    
    def part2(self, steps_goal):
        even = sum(p.manhattan(self.start) % 2 == steps_goal % 2 for p in self.plots)
        odd = len(self.plots) - even if self.plotsize.x % 2 == 1 else even
        filled_radius = max(0, (steps_goal - self.maxdelta) // self.plotsize.y)
        score = even * (1 + 4 * sum(range(0, filled_radius, 2))) + odd * 4 * sum(range(1, filled_radius, 2))
        for r in range(filled_radius, steps_goal // self.plotsize.x + 2):
            for direction in spatial.ENWS:
                score += self.checktile(direction * r, steps_goal)
                score += (r - 1) * self.checktile(direction * (r - 1) + direction.left(), steps_goal)
        return score


@blitzen.run
def main(input_string, verbose=False):
    garden = Garden(input_string)
    p1 = garden.part1(64)
    p2 = garden.part2(26501365)
    return p1, p2

