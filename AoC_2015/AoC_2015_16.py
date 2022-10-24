# YOU HAVE SELECTED MFCSAM AS THE COMPUTER'S DEFAULT VOICE
import dancer


def who_is_sue(ticker, sues, gt=None, ft=None):
    # who sees who sew whose new socks, sir?
    if gt is None:
        gt = set()
    if ft is None:
        ft = set()
    for sue, things in sues.items():
        for key in things.keys() & ticker.keys():
            if key in gt:
                if things[key] <= ticker[key]:
                    break
            elif key in ft:
                if things[key] >= ticker[key]:
                    break
            elif things[key] != ticker[key]:
                break
        else:
            break
    return sue


def parse(input_string):
    table = input_string.maketrans(':,', '  ')
    input_string = input_string.translate(table)
    ticker = dancer.root_path + '/AoC_2015/ticker_tape.txt'
    ticker = [line.split(': ') for line in open(ticker).read().split('\n')]
    ticker = {key: int(val) for key, val in ticker}

    sues = {}
    for line in input_string.split('\n'):
        line = line.split()
        n = int(line[1])
        keys = line[2::2]
        vals = [int(i) for i in line[3::2]]
        sues[n] = {key: val for key, val in zip(keys, vals)}
    return sues, ticker


def main(input_string, verbose=False):
    sues, ticker = parse(input_string)
    p1 = who_is_sue(ticker, sues)
    gt = {'cats', 'trees'}
    ft = {'pomeranians', 'goldfish'}
    p2 = who_is_sue(ticker, sues, gt, ft)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=16, verbose=True)
