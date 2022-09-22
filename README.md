# Advent of Code solutions by Matt Misiaszek
My solves for Advent of Code https://adventofcode.com/

Solves in Python 3

# Running
## Run all in a year
cd to `<year>`

`python run_year.py`

Answers for each day will print along with elapsed time

## Run individual day
cd to `<year>\<day>`

`python day__.py`

## Run day from import
`import day__`

function `main` will return tuple of (Part 1, Part 2)

## Input files not included!
Location of input files must be specified in `common/paths.cfg`.

Specify location as `input: <path>`

Default location is `~/.cache/aoc/`

Input file convention is `'root/{:04d}/{:02d}_in'.format(year, day)`

## Choose your seasonal greeting
Day 25 Part 2 will return a seasonal greeting stored in common/seasonal_greeting.txt

The default greeting is Merry Christmas.  If you prefer another, please modify this file.
