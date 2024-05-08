import blitzen
from AoC_2019.intcode import Intcode
import re
from itertools import combinations

dont_take = {'giant electromagnet', 'molten lava', 'escape pod', 'infinite loop', 'photons'}
ALERT = 'Alert'
CHECKPOINT = 'Security Checkpoint'
NORTH, SOUTH, EAST, WEST = 'north', 'south', 'east', 'west'


def process_command(droid, command):
    if command:
        droid.input.extend([ord(i) for i in command + '\n'])
    droid.output.clear()
    droid.run()
    response = ''.join(chr(i) for i in droid.output)
    return response, droid.status


def safe_cracker(droid, inventory, check_command):
    holding = inventory.copy()
    for i in range(len(inventory)):
        for combo in combinations(inventory, i):
            combo = set(combo)
            command = ''
            for item in holding - combo:
                command += 'drop ' + item + '\n'
            for item in combo - holding:
                command += 'take ' + item + '\n'
            holding = combo
            process_command(droid, command.strip())
            response, status = process_command(droid, check_command)
            if ALERT not in response:
                return response


class Heading:
    def __init__(self):
        self.hidx = 0
        self.hlist = [EAST, NORTH, WEST, SOUTH]
        self.mod = 4

    def name(self):
        return self.hlist[self.hidx]

    def left(self):
        self.hidx += 1
        self.hidx %= self.mod

    def right(self):
        self.hidx -= 1
        self.hidx %= self.mod


def take_items(droid, response, inventory):
    items = re.findall('Items here:\n(.*)\n\n', response)
    if items:
        items = set(line[2:] for line in items[-1].split('\n'))
        for item in items:
            if item not in dont_take:
                process_command(droid, 'take ' + item)
                inventory.add(item)


def doors_set(response):
    doors = re.findall('Doors here lead:\n((?:- .*\n?)*)\n\n', response)[-1]
    doors = set(line[2:] for line in doors.split('\n'))
    return doors


def explore(droid):
    ship_map = {}
    inventory = set()
    checked_doors = set()
    heading = Heading()
    path = tuple()
    response, status = process_command(droid, "")
    while (path, heading.name()) not in checked_doors:
        checked_doors.add((path, heading.name()))

        room_name = re.findall('== (.*) ==', response)[-1]
        if room_name not in ship_map:
            ship_map[room_name] = path
        else:
            path = ship_map[room_name]

        take_items(droid, response, inventory)

        doors = doors_set(response)
        # turn left until you find an open door.
        while heading.name() not in doors:
            heading.left()

        # go through the door
        response, status = process_command(droid, heading.name())
        if ALERT in response:
            # this door was not actually open
            # there is a chance you just happen to stumble into the cockpit on the first try but oh well
            check_command = heading.name()
            heading.left()
        else:
            # turn right
            path += (heading.name(),)
            heading.right()

    return ship_map, inventory, check_command


@blitzen.run
def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    droid = Intcode(program)
    ship_map, inventory, check_command = explore(droid)
    path_to_checkpoint = '\n'.join(ship_map[CHECKPOINT])
    process_command(droid, path_to_checkpoint)
    santas_message = safe_cracker(droid, inventory, check_command)
    p1 = re.search('typing (.*) on', santas_message).group(1)
    p2 = blitzen.holiday_greeting
    return p1, p2

