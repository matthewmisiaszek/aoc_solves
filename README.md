# Advent of Code solutions by Matt Misiaszek
My solves for Advent of Code https://adventofcode.com/

Solves in Python 3

## Running
Run a single day by running its file.  

Run multiple days using common/run_multiple.py.

cd to repo root or to directory containing file before running.

## Configuration
Several options may be set in common/config.ini including:
* Input file directory
* Input file naming convention
* Holiday greeting displayed on day 25
* Output formats

## DANCER
### Directory Augmentation and Normalized Code Execution Routine

DANCER handles several functions common to every day's code:
* Append repo root to sys.path
* Retrieve input file
* Execute main()
* Print header
* Print outputs
* Print elapsed time

## Common

Modules in common are used by solves from multiple days
