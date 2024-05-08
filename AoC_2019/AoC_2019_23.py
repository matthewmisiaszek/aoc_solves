import blitzen
from AoC_2019.intcode import Intcode

N_COMP = 50
NAT = 255


@blitzen.run
def main(input_string, verbose=False):
    software = [int(i) for i in input_string.split(',')]
    packet_queues = {i: [i] for i in range(N_COMP)}
    packet_queues[NAT] = []
    computers = [Intcode(software, packet_queues[i]) for i in range(N_COMP)]
    last_y = None
    while True:
        idle = True
        for computer in computers:
            if not computer.input:
                computer.input.append(-1)
            else:
                idle = False
            computer.run()
            while computer.output:
                idle = False
                a, x, y = computer.output[:3]
                del computer.output[:3]
                packet_queues[a].extend([x, y])
        if idle:
            x, y = packet_queues[NAT][-2:]
            if y == last_y:
                break
            last_y = y
            packet_queues[0].extend([x, y])
    p1 = packet_queues[NAT][1]
    p2 = y
    return p1, p2

