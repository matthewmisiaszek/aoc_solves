# Advent of Code solutions by Matt Misiaszek
My solves for Advent of Code https://adventofcode.com/

Solves in Python 3

## Running
Run a single day by running its file `py AoC_20XX/AoC_20XX_XX.py`.  

Run multiple days using donner/run_multiple.py.  
Enter ranges of years and days as `20XX-20XX:XX-XX` with multiple ranges separated by space.  
The flag `-s` will save outputs for later comparison.

cd to repo root or to directory containing file before running.

## Configuration
A config file is saved to `~/.cache/aoc_blitzen/config.ini`
Several options may be set including:
* Input file directory
* Input file naming convention
* Holiday greeting displayed on day 25
* Output formats

## BLITZEN
### Boilerplate Library for Inputs, Timing, and Zealous Execution Normalization

Blitzen handles several functions common to every day's code:
* Append repo root to sys.path
* Retrieve input file
* Execute main()
* Print header
* Print outputs
* Print elapsed time

## DONNER
### Directory of Naughty and Nice modules for Easy code Reuse
 
Modules in donner are used by solves from multiple days
