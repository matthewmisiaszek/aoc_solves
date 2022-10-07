# from common import common
#
#
# def strtolist(s):
#     s=s.split('/')
#     ret=[]
#     for si in s:
#         reti=[]
#         for sii in si:
#             reti.append(sii)
#         ret.append(reti)
#     return ret
#
# def listtostr(l):
#     s=''
#     for li in l:
#         for lii in li:
#             s+=lii
#         s+='/'
#     return s[:-1]
#
# def rotate(l):
#     ret=[]
#     for i in range(len(l[0])):
#         reti=[]
#         for j in range(len(l)):
#             reti.append(l[j][len(l)-1-i])
#         ret.append(reti)
#     return ret
#
# def flip(l):
#     ret=[]
#     for i in range(len(l)):
#         ret.append(l[len(l)-i-1])
#     return ret
#
# def chunk(l):
#     dim=len(l)
#     if dim%2==0:
#         div=2
#     else:
#         div=3
#     ret=[]
#     for i in range(int(dim/div)):
#         reti=[]
#         for j in range(int(dim/div)):
#             retj=[]
#             for ii in range(div):
#                 retj.append(l[i*div+ii][j*div:(j+1)*div])
#             reti.append(retj)
#         ret.append(reti)
#     return ret
#
# def join(l):
#     ret=[]
#     for li in l:
#         for ii in range(len(li[0])):
#             reti=[]
#             for lj in li:
#                 reti+=lj[ii]
#             ret.append(reti)
#     return ret
#
# f=open('2017-21.in').read().split('\n')
# rules={}
# transforms=((0,0),(1,0),(1,0),(1,0),(1,1),(1,0),(1,0),(1,0))
# for l in f:
#     l= common.delstrp(l, '=>')
#     key=strtolist(l[0])
#     val=strtolist(l[1])
#     for transform in transforms:
#         if transform[0] == 1:
#             key = rotate(key)
#         if transform[1] == 1:
#             key = flip(key)
#         skey = listtostr(key)
#         rules[skey]=val
# #print(rules)
#
# image='.#./..#/###'
# image=strtolist(image)
# images=[]
# for iteration in range(18):
#     print('\rCalculating iteration ',iteration,end='')
#     image=chunk(image)
#     for i in range(len(image)):
#         for j in range(len(image[0])):
#             image[i][j]=rules[listtostr(image[i][j])]
#     image=join(image)
#     images.append(listtostr(image).count('#'))
# print('\rCalculation complete')
# print('Part 1: ',images[4])
# print('Part 2: ',images[-1])
# # s=''
# # for l in image:
# #     s+=''.join(l)+'\n'
# # print(s)
#
import dancer
# from common import printer


def parse_pattern(pattern, mark, cr):
    return tuple(tuple(c == mark for c in line) for line in pattern.split(cr))


def transform(key):
    transpose = {4}
    vflip = {1, 3, 5, 7}
    hflip = {2, 6}
    yield key
    for t in range(8):
        if t in vflip:
            key = tuple(reversed(key))
            yield key
        elif t in transpose:
            key = tuple(zip(*key))
            yield key
        elif t in hflip:
            key = tuple(tuple(reversed(line)) for line in key)
            yield key


def main(input_string, verbose=False):
    p1, p2 = 5, 18
    cr = '/'
    mark = '#'
    start_pattern = '.#./..#/###'
    image = parse_pattern(start_pattern, mark, cr)
    rules = {}
    history = [0]
    for line in input_string.split('\n'):
        key, val = (parse_pattern(i, mark, cr) for i in line.split(' => '))
        for key in transform(key):
            rules[key] = val
    for iteration in range(max(p1, p2)):
        if len(image) % 2 == 0:
            size = 2
        else:
            size = 3
        chunks = {}
        nchunks = len(image) // size
        for y in range(nchunks):
            for x in range(nchunks):
                chunks[(x, y)] = rules[tuple(line[x * size:(x + 1) * size] for line in image[y * size:(y + 1) * size])]
        size += 1
        image = tuple(sum((chunks[(x, y)][r] for x in range(nchunks)), ()) for y in range(nchunks) for r in range(size))
        history.append(sum(sum(line) for line in image))
    p1 = history[p1]
    p2 = history[p2]
    # if verbose:
    #     on_set = {(x, y) for x in range(len(image)) for y in range(len(image)) if image[y][x]}
    #     printer.printset(on_set)
    #     print('')
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=21, verbose=True)
