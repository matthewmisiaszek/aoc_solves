#  This file is a helper file to add parent directory to path and grab the aoc_input function
import sys
sys.path.append('..')


def aoc_input(year, day):
    from common.aoc_input import aoc_input as common_aoc_input
    return common_aoc_input(year, day)