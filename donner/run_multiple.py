import os.path
import subprocess
import blitzen
import time
import os
import argparse
import re
import multiprocessing
import json


def getranges(s):
    if s == '':
        return []
    ret = []
    for item in s.split(','):
        item = [int(i) for i in item.split('-')]
        if len(item) == 1:
            ret += item
        else:
            n = item[0]
            x = item[-1]
            ret += list(range(n, x + 1))
    return ret


def get_args():
    parser = argparse.ArgumentParser(description='AoC Run Multiple Argument Parser')
    parser.add_argument('ranges', nargs='*', default='2015-2024:1-25')
    parser.add_argument('-m', action='store_true')  # man
    parser.add_argument('-t', action='store_true')  # times_only
    return parser.parse_args()


def man():
    print("""Input ranges of years and days to run in combinations of year1-yearn:day1-dayn.
            Single value ranges are also allowed such as 2019:11 or 2017:2-6.
            Separate ranges with a space.  2019:5 2020:6-10
            Use -s flag to save results for future comparison.""")


def make_header(config, widths):
    table_format = config['table']['format']
    column_header = table_format.format(**{
        'day': 'Day', 'p1': 'Part 1', 'p2': 'Part 2', 'time': 'Time', 'p1chk': 'P1 Pass', 'p2chk': 'P2 Pass'
    })
    header_format = f'{{year:^{len(column_header)}}}'
    line = table_format.format(**{k: '-' * v for k, v in widths.items()})
    return '\n'.join((header_format, line, column_header, line))


def parse_group(group):
    if ':' in group:
        years, days = (getranges(i) for i in group.split(':'))
    else:
        years = getranges(group)
        days = []
    if not years:
        years = list(range(2015, 2025))
    if not days:
        days = list(range(1, 26))
    return years, days


def run_day(year, day, config):
    data = {'year': year, 'day': day}
    if day == 0:
        return data
    file = os.path.join(blitzen.root_path, blitzen.config['files']['solution_format'].format(**data))
    py = config['python']['call']
    capture = subprocess.run([py, file, '-q', '-json'], capture_output=True)
    if capture.stderr:
        print(capture.stderr)
    stdout = str(capture.stdout.decode('utf-8'))
    stdout = stdout.replace('\r', '')
    data = json.loads(stdout)
    return data


def print_day(data, config, widths):
    extra = []
    for key in widths:
        val = data[key]
        if isinstance(val, str) and ('\n' in val or len(val) > widths[key]):
            data[key] = '---'
            extra.append(val)
    print(config['table']['format'].format(**data))
    if extra:
        print('\n'.join(extra))


def main():
    args = get_args()
    if args.m:
        man()
        return
    config = blitzen.config
    n_cores = multiprocessing.cpu_count()
    if args.t:
        config['table']['format'] = re.sub(r' *\{(p1|p2|check)(:<\d*)?} *', '', config['table']['format'])
        config['table']['format'] = re.sub(r'\|+', '|', config['table']['format'])
        n_cores = 1
    pool = multiprocessing.Pool(n_cores)
    widths = {a: int(b) for a, b in re.findall(r'{(\w+):[<>^](\d+)', config['table']['format'])}
    full_header = make_header(config, widths)
    groups = args.ranges if isinstance(args.ranges, list) else [args.ranges]
    for group in groups:
        print(group)
        queue = []
        years, days = parse_group(group)
        start_time_all = time.time()
        for year in years:
            queue.append(pool.apply_async(run_day, (year, 0, config)))
            for day in days:
                blitzen.fetch(year, day)
                queue.append(pool.apply_async(run_day, (year, day, config)))
        for result in queue:
            result.wait()
            data = result.get()
            if data['day'] == 0:
                print(full_header.format(**data))
                continue
            data['time'] = config['table']['time_format'].format(**data)
            print_day(data, config, widths)
        print()
        print('Total Time: ', time.time() - start_time_all)


if __name__ == '__main__':
    main()
