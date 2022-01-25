import time

start = time.time()

from queue import PriorityQueue


class World:
    def __init__(self):
        self.pods = 'ABCD'  # pod types
        self.floor = '.'
        self.home = 'H'
        self.target = {}
        self.closed = set()
        self.queue = PriorityQueue()
        self.home_check = {}
        self.state_list = []
        self.neighbors = {}

    def cost(self, pod):
        return 10 ** self.pods.find(pod)  # energy cost function for each pod


def main(input_file='input.txt', target_file='target.txt', p2insert='p2insert.txt', verbose=False):
    start_state = open(input_file).read().split('\n')
    target_state = open(target_file).read().split('\n')
    if verbose:
        print('Part 1 Start ======================')
    p1 = solve(start_state, target_state, verbose)
    if verbose:
        print('Part 2 Start ======================')
    p2_start_insert = open(p2insert).read().split('\n')
    start_state = start_state[:3] + p2_start_insert + start_state[3:]
    target_state = target_state[:4] + target_state[3:4] + target_state[3:]
    p2 = solve(start_state, target_state, verbose)
    if verbose:
        print('Summary ===========================')
        print('Part1: ', p1)
        print('Part2: ', p2)
    return p1, p2


def solve(start_state, target_state, verbose=True):
    world = World()  # Container to store all the variables getting passed around
    pods = digest_file(start_state, include=world.pods)
    world.target = digest_file(target_state, include=world.pods + world.floor)
    get_neighbors(world)  # create dictionary of neighboring spaces for pathfinding later
    get_home_check(world)  # create dictionary of spaces to check to see if a pod is home or not
    world.queue.put((0, tuple(pods.items()), -1))  # convert pods to tuple and add to queue
    state_list_index = 0
    while not world.queue.empty():  # search using Dijkstra's
        weight, pods, previous = world.queue.get()
        if pods not in world.closed:  # Prevent visiting same state twice
            world.closed.add(pods)
            world.state_list.append((weight, pods, previous))  # cache state for printing later
            previous = state_list_index  # record where this state was stored
            state_list_index += 1
            home_count = find_moves_burrow(weight, pods, previous, world)  # find new states to add to the queue
            if home_count == len(pods):  # if all pods are home then solve is finished
                if verbose:
                    print_steps(previous, world, target_state)
                return weight
    return False  # solve failed


def digest_file(f, include):
    grid = {}
    for y, row in enumerate(f):
        for x, c in enumerate(row):
            if c in include:
                grid[(x, y)] = c
    return grid


def get_neighbors(world):
    # make dictionary of neighbors for each space
    for space in world.target:
        world.neighbors[space] = neighbors(world.target, space)


def neighbors(grid, point):
    ret = []
    for offset in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        new_point = tuple([a + b for a, b in zip(point, offset)])
        if new_point in grid:
            ret.append(new_point)
    return ret


def get_home_check(world):
    # make dictionary of spaces to check when determining if a pod is home or not
    for space, occupant in world.target.items():
        if occupant != world.floor:
            q = [[space]]
            closed = set()
            while q:
                current = q.pop(0)
                closed.add(current[-1])
                ns = neighbors(world.target, current[-1])
                if len(ns) == 1:
                    world.home_check[space] = current[1:]
                else:
                    for n in ns:
                        if n not in closed and world.target[n] != world.floor:
                            q.append(current + [n])


def find_moves_burrow(weight, pods, previous, world):
    # find all possible moves for this state and add to queue
    home_count = 0
    pods = dict(pods)
    for pod, occupant in pods.items():  # find moves for each pod and add to queue
        home_count += find_moves_pod(pod, weight, pods, previous, world)  # home_count counts how many pods are home
    return home_count


def find_moves_pod(pod, weight, pods, previous, world):
    # find all possible moves for this pod in this state and add to queue
    occupant = pods[pod]
    if occupant == world.home:  # if marked as home, return 1 (pod is home)
        return 1
    elif home(pod, occupant, pods, world):  # if home but not marked as home...
        pods[pod] = world.home  # mark as home
        return 1  # return 1 (pod is home)
    else:  # otherwise, BFS to find valid moves
        q = [(pod, False, False, 0)]  # simple FIFO queue
        closed = set()
        while q:
            current, hall, room, distance = q.pop(0)
            if current not in closed:
                closed.add(current)
                if current not in pods or current == pod:  # if space is not occupied, continue
                    hall = hall or world.target[current] == world.floor  # have we been in the hall yet?
                    room = room or world.target[current] != world.floor  # have we been in a room yet?
                    if hall and room and len(world.neighbors[current]) < 3:
                        # if we've been in both hall and room and this isn't an intersection...
                        try_move(current, pod, distance, weight, pods, previous, world)
                    distance += 1
                    for n in world.neighbors[current]:
                        if n not in closed:
                            q.append((n, hall, room, distance))  # add new spaces to queue until blocked
    return 0  # return 0 (pod not home yet)


def try_move(move_to, move_from, distance, weight, pods, previous, world):
    # if move_to is a valid place to move the pod at move_from then do it
    occupant = pods[move_from]
    end_is_hall = world.target[move_to] == world.floor
    if end_is_hall:
        end_is_home = False
    else:
        end_is_home = home(move_to, occupant, pods, world)
    if end_is_hall or end_is_home:  # move_to must be either hall or a valid home in a room
        new_burrow = pods.copy()
        if end_is_hall:
            new_burrow[move_to] = occupant
        else:
            new_burrow[move_to] = world.home
        new_burrow.pop(move_from)
        new_key = tuple(sorted(new_burrow.items()))
        if new_key not in world.closed:
            world.queue.put((weight + distance * world.cost(occupant), new_key, previous))  # add to the queue


def home(space, occupant, pods, world):
    # check if a pod is home
    if world.target[space] != occupant:
        return False
    else:
        for key2 in world.home_check[space]:
            if not (key2 in pods and (world.home == pods[key2] or world.target[key2] == pods[key2])):
                return False  # every space in list must match the target state
    return True  # if you've made it this far then your pod is a home pod


def print_steps(previous, world, target_state):
    # create list of states that led to state "previous" then print them all out
    printlist = []
    while previous >= 0:
        weight, burrow, previous = world.state_list[previous]  # find previous state, append state to print list
        printlist.append((weight, burrow))
    printlist.reverse()
    for step, (weight, burrow) in enumerate(printlist):  # iterate through print list and print each step
        burrow = dict(burrow)
        print('Step ', step, ' Weight: ', weight)
        prints = ''
        for y, row in enumerate(target_state):
            for x, c in enumerate(row):
                key = (x, y)
                if key in burrow:
                    if burrow[key] == world.home:
                        prints += world.target[key]  # print pod letter instead of 'H' for home pods
                    else:
                        prints += burrow[key]  # print pod letter if there's a pod here
                elif key in world.target:
                    prints += world.floor  # print floor if no pod here
                else:
                    prints += target_state[y][x]  # print wall or space if not in dynamic area
            prints += '\n'
        print(prints)
    print('Finished!')


if __name__ == "__main__":
    main(verbose=True)
