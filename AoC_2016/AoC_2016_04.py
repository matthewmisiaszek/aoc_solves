# import string
# f=open('AoC_2016-4.in').readlines()
# sum=0
# for l in f:
#     a=l.rfind('-')
#     sectorID,checksum=l[a+1:].strip().strip(']').split('[')
#     ename=l[:a].replace('-','')
#     lfreq=[]
#     for letter in string.ascii_lowercase:
#         lfreq.append([letter,ename.count(letter)])
#     lfreq.sort(key=lambda x: x[1],reverse=True)
#     checksum1=''.join(list(x[0] for x in lfreq[:5]))
#     if checksum1==checksum:
#         sum+=int(sectorID)
# print(sum)
#
import dancer
import re
from collections import Counter
from string import ascii_lowercase as alph


class Room:
    def __init__(self, encn, id, csum):
        self.encn = encn.strip()
        self.id = int(id)
        self.csum = csum
        self.decn = None
        self.real = None
        self.decrypt()
        self.check_real()

    def check_real(self):
        ncount = Counter(self.encn.replace('-', ''))
        most_frequent = sorted(ncount.keys(), key=lambda x: (-ncount[x], x))[:5]
        self.real = ''.join(most_frequent) == self.csum

    def decrypt(self):
        lalph = len(alph)
        self.decn = ''.join(alph[(alph.find(c) + self.id) % lalph] if c != '-' else c for c in self.encn)


def main(input_string, verbose=False):
    pattern = '(\D*)-(\d*)\[(\D*)\]'
    rooms = [Room(*group) for group in re.findall(pattern, input_string)]
    p1 = sum(room.id for room in rooms if room.real)
    room_lookup = {room.decn: room.id for room in rooms}
    p2 = room_lookup['northpole-object-storage']
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=4, verbose=True)
