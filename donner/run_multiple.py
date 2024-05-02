import os.path
import subprocess
import blitzen
import time
from configparser import ConfigParser
import os
import argparse


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
    parser.add_argument('ranges', nargs='*', default='2015-2023:1-25')
    parser.add_argument('-s', action='store_true')  # save results
    parser.add_argument('-m', action='store_true')  # man
    return parser.parse_args()


def man():
    print("""Input ranges of years and days to run in combinations of year1-yearn:day1-dayn.
            Single value ranges are also allowed such as 2019:11 or 2017:2-6.
            Separate ranges with a space.  2019:5 2020:6-10
            Use -s flag to save results for future comparison.""")


def make_header(config):
    table_format = config['table']['format']
    header_format = config['table']['header_format']
    column_header = table_format.format(**{
        'day': 'Day', 'p1': 'Part 1', 'p2': 'Part 2', 'time': 'Time', 'check': 'Check'
    })
    line = '-' * len(column_header)
    return '\n'.join((line, header_format, line, column_header, line))


def get_outputs(output_path):
    outputs = ConfigParser()
    if os.path.exists(output_path):
        outputs.read(output_path)
    if 'format' not in outputs:
        outputs.add_section('format')
    if 'format' not in outputs['format']:
        outputs.set('format', 'format', '({p1}, {p2})')
    return outputs


def parse_group(group):
    if ':' in group:
        years, days = (getranges(i) for i in group.split(':'))
    else:
        years = getranges(group)
        days = []
    if not years:
        years = list(range(2015, 2024))
    if not days:
        days = list(range(1, 26))
    return years, days


def run_day(year, day, config):
    data = {'year': year, 'day': day}
    file = os.path.join(blitzen.root_path, blitzen.config['files']['solution_format'].format(**data))
    start = time.time()
    py = config['python']['call']
    capture = subprocess.run([py, file, '-q'], capture_output=True)
    if capture.stderr:
        print(capture.stderr)
    stdout = str(capture.stdout.decode('utf-8'))
    stdout = stdout.replace('\r', '')
    elapsed_time = config['table']['time_format'].format(time=time.time() - start)
    extract = blitzen.extract(config['dayprint']['format'], stdout)
    extract['time'] = elapsed_time
    return extract


def check_day(extract, outputs, save):
    yearst, dayst = str(extract['year']), str(extract['day'])
    outval = outputs['format']['format'].format(**extract).replace('\n', '\\n')
    if yearst in outputs and dayst in outputs[yearst]:
        saved = outputs[yearst][dayst]
        if outval == saved:
            extract['check'] = 'Pass'
        else:
            extract['check'] = 'Fail'
            print('expected:', saved)
    else:
        extract['check'] = 'NA'
    if save:
        if yearst not in outputs:
            outputs.add_section(yearst)
        outputs.set(yearst, dayst, outval)


def print_day(extract, config):
    extra = []
    for key, val in extract.items():
        if '\n' in val or len(val) > int(config['table']['max_len']):
            extract[key] = '---'
            extra.append(val)
    print(config['table']['format'].format(**extract))
    if extra:
        print('\n'.join(extra))


def main():
    args = get_args()
    if args.m:
        man()
        return

    config = blitzen.config
    full_header = make_header(config)
    output_path = os.path.join(blitzen.configpath, 'outputs.ini')
    outputs = get_outputs(output_path)

    groups = args.ranges if isinstance(args.ranges, list) else [args.ranges]
    for group in groups:
        print(group)
        years, days = parse_group(group)
        start_time_all = time.time()
        for year in years:
            print(full_header.format(**{'year':year}))
            for day in days:
                extract = run_day(year, day, config)
                check_day(extract, outputs, args.s)
                print_day(extract, config)
            print()
        print('Total Time: ', time.time() - start_time_all)
        if args.s:
            with open(output_path, 'w') as outputfile:
                outputs.write(outputfile)


if __name__ == '__main__':
    main()
