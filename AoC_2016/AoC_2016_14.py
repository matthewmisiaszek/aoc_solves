# import hashlib
# chars='abcdefghijklmnopqrstuvwxyz1234567890'
#
# salt='qzyelonm'
# #salt='abc'
# potentialkeys={}
# keys=[]
# keys1=[]
# i=0
#
# def hashfun(seed):
#     ret=seed
#     for i in range(2017):
#         ret = hashlib.md5((ret).encode('utf-8')).hexdigest()
#     return ret
#
# while len(keys)<64 or len(potentialkeys)>0:
#     hash=hashfun(salt+str(i))
#     first = len(hash)
#     for ch in chars:
#         hf = hash.find(ch + ch + ch)
#         if hf!=-1 and len(keys)<=64 and hf<=first:
#             potentialkeys[i]=ch
#             first=hf
#         if hash.find(ch+ch+ch+ch+ch)!=-1:
#             for key in potentialkeys.keys():
#                 if potentialkeys[key]==ch and i>key and key+1000>=i and not key in keys:
#                     keys1.append([key,i,ch])
#                     keys.append(key)
#                     print(key)
#     todelete=[]
#     for key in potentialkeys.keys():
#         if key<i-1000:
#             todelete.append(key)
#     for key in todelete:
#         del potentialkeys[key]
#     i+=1
# keys.sort()#key=lambda x: x[0])
# keys1.sort(key=lambda x: x[0])
# print(keys)
#
# for key in keys1:
#     hash1=hashlib.md5((salt+str(key[0])).encode('utf-8')).hexdigest()
#     hash2 = hashlib.md5((salt+str(key[1])).encode('utf-8')).hexdigest()
#     print(key[2],key[0],hash1,key[1],hash2)
# print(len(keys))
# print(keys[63])
#
# #Part 1:
# #15629 high
# #15218 high
# #14937 low
import dancer
# from string import hexdigits
from common.misc import md5hash


def stretch(seed):
    ret = seed
    for _ in range(2017):
        ret = md5hash(ret)
    return ret


def generate(salt, hashfun, want):
    potential_keys = set()
    idx = -1
    nkeys, keys = 0, []
    hexdigits = '0123456789abcdef'
    while potential_keys or nkeys < want:
        idx += 1
        hash_i = hashfun(salt + str(idx))
        triples = []
        for c in hexdigits:
            if c * 5 in hash_i:
                limit = idx - 1000
                for jdx, c2 in tuple(potential_keys):
                    if jdx >= limit:
                        if c2 == c:
                            keys.append(jdx)
                            nkeys += 1
                            potential_keys.discard((jdx, c2))
                    else:
                        potential_keys.discard((jdx, c2))
                triples.append((hash_i.find(c*3), c))
            elif nkeys < want and c * 3 in hash_i:
                triples.append((hash_i.find(c*3), c))
        if triples and nkeys < want:
            _, c = min(triples)
            potential_keys.add((idx, c))

    keys.sort()
    return keys[want - 1]


def main(input_string, verbose=False):
    p1 = generate(salt=input_string, hashfun=md5hash, want=64)
    p2 = generate(salt=input_string, hashfun=stretch, want=64)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=14, verbose=True)
