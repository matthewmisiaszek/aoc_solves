import time

start = time.time()


def movepod(burrow, move):
    a, b = move
    burrow[b].append(burrow[a].pop())

def movecost(burrow, move, weight, depth):
    a, b = move
    distance = abs(a - b) + depth[a] + depth[b] - len(burrow[a]) - len(burrow[b]) + 1
    cost = distance * weight[burrow[a][-1]]
    return cost

def getmoves(burrow, target):
    moves = []
    for i, room in enumerate(burrow):
        if target[i] != '' and len(room) > 0 and room.count(target[i]) < len(room):
            for j in range(i + 1, len(burrow)):
                if target[j] == '':
                    if not burrow[j]:
                        moves.append((i, j))
                    else:
                        break
            for j in range(i - 1, -1, -1):
                if target[j] == '':
                    if not burrow[j]:
                        moves.append((i, j))
                    else:
                        break
        elif target[i] == '' and room != []:
            for j in range(i + 1, len(burrow)):
                if target[j] != '':
                    if target[j] == room[-1] and burrow[j].count(target[j]) == len(burrow[j]):
                        moves.append((i, j))
                elif burrow[j]:
                    break
            for j in range(i - 1, -1, -1):
                if target[j] != '':
                    if target[j] == room[-1] and burrow[j].count(target[j]) == len(burrow[j]):
                        moves.append((i, j))
                elif burrow[j]:
                    break
    return moves

def tostring(burrow, depth, verbose):
    if verbose:
        stuff = ['' for _ in range(max(depth)+1)]
        for room,roomd in zip(burrow, depth):
            if roomd ==0:
                if room:
                    stuff[0]+=room[0]
                else:
                    stuff[0]+='.'
                for i in range(1,len(stuff)):
                    stuff[i]+=' '
            else:
                stuff[0]+='.'
                for i in range(1,len(stuff)):
                    j = roomd-i
                    if j<len(room):
                        stuff[i]+=room[j]
                    else:
                        stuff[i]+=' '
        return '\n'.join(stuff)
    else:
        return ','.join([''.join(room) for room in burrow])

def organize(burrow, target, depth, weight, verbose, cost=0, mincost=None, memo={}):
    if mincost is not None and cost >= mincost:
        return mincost, 'fail'
    elif sum([not (room.count(target[i]) == depth[i]) for i, room in enumerate(burrow)]) == 0:
        return cost, ''
    else:
        bestpath=''
        moves = getmoves(burrow, target)
        for i, j in moves:
            ncost = cost + movecost(burrow, (i, j), weight, depth)
            movepod(burrow, (i,j))
            burrow_string = tostring(burrow, depth, verbose)
            if burrow_string not in memo or memo[burrow_string] > ncost:
                memo[burrow_string] = ncost
                nmincost, path = organize(burrow, target, depth, weight, verbose, ncost, mincost)
                if mincost is None or (nmincost is not None and nmincost<mincost):
                    mincost = nmincost
                    bestpath = burrow_string+'\n\n'+path
            movepod(burrow, (j, i))
        return mincost, bestpath


def solve(start_state, verbose=True):
    burrow = [[] for _ in start_state[0]]
    alph = 'ABCD'
    for line in reversed(start_state):
        for i, c in enumerate(line):
            if c in alph:
                burrow[i].append(c)
    burrow = burrow[1:-1]
    depth = [len(i) for i in burrow]
    weight = {a: 10 ** i for i, a in enumerate(alph)}
    letter = 0
    target = []
    for room in depth:
        if room > 0:
            target.append(alph[letter])
            letter += 1
        else:
            target.append('')
    cost, path = organize(burrow, target, depth, weight, verbose)
    if verbose is True:
        print(tostring(burrow, depth, verbose)+'\n\n'+path)
        print('Cost: ',cost)
    return cost

def main(input_file='input.txt', p2insert='p2insert.txt', verbose=False):
    start_state = open(input_file).read().split('\n')
    if verbose:
        print('Part 1 Start ======================')
    p1 = solve(start_state, verbose)
    if verbose:
        print('Part 2 Start ======================')
    p2_start_insert = open(p2insert).read().split('\n')
    start_state = start_state[:3] + p2_start_insert + start_state[3:]
    p2 = solve(start_state, verbose)
    if verbose:
        print('Summary ===========================')
        print('Part1: ', p1)
        print('Part2: ', p2)
    return p1, p2

if __name__ == "__main__":
    main(verbose=False)
    print('Elapsed Time: ',time.time()-start)