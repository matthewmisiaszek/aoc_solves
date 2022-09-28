import core
import re
from collections import Counter

def main(input_string, verbose=False):
    pattern = '#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)'
    claims_re = re.findall(pattern, input_string)
    claims_tup = tuple(tuple(int(i) for i in claim) for claim in claims_re)
    claims_range = {cid:((left, left+width),(top, top+height))
                    for cid, left, top, width, height in claims_tup}
    claims_set = {cid:set((x,y)
                          for x in range(xn,xx)
                          for y in range(yn,yx))
                  for cid, ((xn,xx),(yn,yx)) in claims_range.items()}
    claimed = sum([tuple(claim) for claim in claims_set.values()],())
    claim_count = Counter(claimed)
    double_claimed = {point for point,count in claim_count.items() if count>1}
    p1 = len(double_claimed)
    p2 = {cid for cid,claim in claims_set.items() if  not claim & double_claimed}.pop()
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2018, day=3, verbose=True)
