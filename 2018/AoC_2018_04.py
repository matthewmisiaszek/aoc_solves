import core


def main(input_string, verbose=False):
    f = input_string.split('\n')
    f.sort()

    guards = {}
    for stamp in f:
        stamp1 = stamp[19:].split()
        if stamp1[0] == 'Guard':
            guard = stamp1[1]
            if not guard in guards.keys():
                guards[guard] = {}
        elif stamp1[0] == 'wakes':
            wake = int(stamp[15:17])
            for i in range(sleep, wake):
                if i in guards[guard].keys():
                    guards[guard][i] += 1
                else:
                    guards[guard][i] = 1
        elif stamp1[0] == 'falls':
            sleep = int(stamp[15:17])

    p1max = 0
    p2max = 0

    for guard in guards.keys():
        guardsleep = 0
        guardminutes = 0
        for minute in guards[guard].keys():
            minutei = guards[guard][minute]
            guardsleep += minutei
            if minutei > guardminutes:
                guardmaxminute = minute
                guardminutes = minutei
        if guardminutes > p2max:
            p2max = guardminutes
            p2guard = guard
            p2minute = guardmaxminute
        if guardsleep > p1max:
            p1guard = guard
            p1minute = guardmaxminute
            p1max = guardsleep

    p1 = int(p1guard[1:]) * p1minute
    p2 = int(p2guard[1:]) * p2minute

    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2018, day=4, verbose=True)
