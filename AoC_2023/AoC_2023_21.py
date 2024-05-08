import blitzen
from donner import graph, spatial


class Garden:
    def __init__(self, input_string):
        self.garden_dict = graph.text_to_dict(input_string, exclude='#')
        self.plots = set(self.garden_dict.keys())
        _, self.plotsize = spatial.bounds(self.plots, pad=1)
        self.plotsize += spatial.Point(0, 0, 1)
        for plot, char in self.garden_dict.items():
            if char == 'S':
                self.start = plot
        self.delta_infinity = {}
        self.delta_local = {}
        self.maxdelta = 1
        self.steps = 0
        self.last_delta = {spatial.Point(): 0}
        self.deltaprint = {}
        perimeter = {self.start}
        while max(self.last_delta.values()) >= self.steps - 1:
            perimeter = set().union(
                *(self.getdelta(plot) for plot in perimeter)
                )
            self.steps += 1

    def getdelta(self, plot):
        if plot in self.delta_local:
            return ()
        delta = self.steps - plot.manhattan(self.start)
        infinity_key = self.relative(plot)
        relative_plot, relative_direction = infinity_key
        if (relative_direction in self.last_delta 
            and self.steps - self.last_delta[relative_direction] > 1):
            
            return ()
        if (infinity_key not in self.delta_infinity 
            or self.delta_infinity[infinity_key] != delta):
            self.delta_infinity[infinity_key] = delta
            self.maxdelta = max(self.maxdelta, delta)
            self.last_delta[relative_direction] = self.steps
            self.deltaprint[plot] = delta
        self.delta_local[plot] = delta
        new_plots = ()
        for direction in spatial.ENWS:
            new_plot = plot + direction
            if new_plot % self.plotsize in self.plots:
                new_plots += (new_plot,)
        return new_plots
    
    def checktile(self, tile, steps_goal):
        tile_origin = tile * self.plotsize
        tile_score = 0
        for plot in self.plots:
            if plot not in self.delta_local:
                continue
            plot += tile_origin
            if plot in self.delta_local:
                pdelta = self.delta_local[plot]
            else:
                pdelta = self.delta_infinity[self.relative(plot)]
            psteps = plot.manhattan(self.start) + pdelta
            if psteps % 2 == steps_goal % 2  and psteps <= steps_goal:
                tile_score += 1
        return tile_score
    
    def relative(self, plot):
        relative_plot = plot % self.plotsize
        relative_tile = plot.__floordiv__(self.plotsize).sign()
        return relative_plot, relative_tile
    
    def part1(self, steps_goal):
        return self.checktile(spatial.Point(), steps_goal)
    
    def part2(self, steps_goal):
        pmodcount = [
            sum((p.manhattan(self.start) + i) % 2 == steps_goal % 2 
                for p in self.plots if p in self.delta_local) 
            for i in (0, 1)
            ]
        filled_radius = (steps_goal - self.maxdelta) // self.plotsize.y
        score = 0
        if filled_radius >= 0:
            score += pmodcount[0]
        for i in (0, 1):
            score += sum(range(i, filled_radius, 2)) * 4 * pmodcount[i]
        filled_radius = max(0, filled_radius)
        for r in range(filled_radius, steps_goal // self.plotsize.x + 2):
            if r == 0:
                score += self.checktile(spatial.Point(), steps_goal)
            if r > 0:
                for direction in spatial.ENWS:
                    score += self.checktile(direction * r, steps_goal)
            if r > 1:
                for direction in spatial.ENWS_CORNERS:
                    c = 1
                    while True:
                        a_tile = spatial.Point(r - c, c)
                        a_score, b_score = (
                            self.checktile(tile * direction, steps_goal) 
                            for tile in (a_tile, a_tile.transpose())
                            )
                        if a_score == b_score:
                            score += (r - 2 * c + 1) * a_score
                            break
                        else:
                            score += a_score + b_score
                            c += 1
        return score


@blitzen.run
def main(input_string, verbose=False):
    garden = Garden(input_string)
    p1 = garden.part1(64)
    p2 = garden.part2(26501365)
    return p1, p2

