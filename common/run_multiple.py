import os.path

import dancer
import importlib
import time
from configparser import ConfigParser
import os

SAVE = 'save'
CHECK = 'check'


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


def main():
    config = ConfigParser()
    config.read(dancer.root_path + '/common/config.ini')
    columns = config['table']['columns'].split(',')
    column_widths = [int(i) for i in config['table']['column_widths'].split(',')]
    widths = {column: width for column, width in zip(columns, column_widths)}
    separator = ' | '
    column_header = separator.join((column.center(widths[column]) for column in columns))
    line = '-' * len(column_header)
    file_format = config['files']['solution_format']
    file_variables = config['files']['solution_variables'].split(',')

    print('Select years and days to run.')
    print('Press return to run all.')
    print('Enter years as four digit numbers and days as 2 digit numbers.')
    print('You may enter ranges as min-max or individual values separated by commas.')
    print('Years and days are joined by colon :')
    print('Multiple year-day combinations may be separated by semicolon ;')
    print('Example: 2020:1-15;2020-2021:1-4,6-8')
    user_input = input('Input here: ')
    print(user_input)

    save_outputs = SAVE in user_input
    user_input = user_input.replace(SAVE, '')
    check_outputs = CHECK in user_input
    user_input = user_input.replace(CHECK, '')
    user_input = user_input.strip()
    input_path = config['files']['input_directory']
    input_path = os.path.expandvars(input_path)
    input_path = os.path.expanduser(input_path)
    output_path = input_path + 'outputs.ini'
    outputs = ConfigParser()
    if os.path.exists(output_path):
        outputs.read(output_path)

    for group in user_input.split(';'):
        if ':' in group:
            years, days = (getranges(i) for i in group.split(':'))
        else:
            years = getranges(group)
            days = []
        if not years:
            years = list(range(2015, 2023))
        if not days:
            days = list(range(1, 26))
        start_time_all = time.time()
        for year in years:
            # sys.path.append('../{:04d}'.format(year))
            print(line)
            print('{:04d}'.format(year).center(len(column_header)))
            print(line)
            print(column_header)
            print(line)
            for day in days:
                data = {'year': year, 'day': day}
                yearst, dayst = str(year), str(day)
                vars = [data[var] for var in file_variables]
                start = time.time()
                solve = importlib.import_module(file_format.format(*vars))
                try:
                    strip = solve.STRIP
                except:
                    strip = True
                p1, p2 = solve.main(input_string=dancer.aoc_input(year, day, strip=strip), verbose=False)
                elapsed_time = '{:.3f}'.format(time.time() - start)
                data = {'Day': day, 'Part 1': p1, 'Part 2': p2, 'Time (s)': elapsed_time}
                data_str = {key: str(val) for key, val in data.items()}
                row = {key: val if len(val) <= widths[key] else '--' for key, val in data_str.items()}
                extra = [key + ':\n' + data_str[key] for key in columns if len(data_str[key]) > widths[key]]
                printstr = separator.join((row[key].rjust(widths[key]) for key in columns))
                if check_outputs:
                    if yearst in outputs and dayst in outputs[yearst]:
                        saved = outputs[yearst][dayst]
                        if str((p1, p2)) == saved:
                            printstr+= ' Pass'
                        else:
                            printstr += ' Fail'
                    else:
                        printstr+=' No Data'
                if save_outputs:
                    if yearst not in outputs:
                        outputs.add_section(yearst)
                    outputs.set(yearst, dayst, str((p1, p2)))
                print(printstr)
                if extra:
                    print('\n'.join(extra))
        print('Total Time: ', time.time() - start_time_all)
        if save_outputs:
            with open(output_path, 'w') as outputfile:
                outputs.write(outputfile)

if __name__ == '__main__':
    main()
