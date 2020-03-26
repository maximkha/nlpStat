from pathlib import Path
import argparse
from random import shuffle
import sys

def getArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Repeats file lines and shuffles")
    parser.add_argument("-i", "--input", required=True, help="The input file.")
    parser.add_argument("-c", "--count", required=True, type=int, help="The number of times to repeat each line")
    parser.add_argument("-o", "--output", required=True, help="Your destination output file.")
    options = parser.parse_args(args)
    return options
    
args = getArgs(sys.argv[1:])

if not Path(args.input).is_file():
    print("The input file does not exist!")
    exit()

with open(args.input) as inputFile:
    with open(args.output, 'w', encoding="utf-8") as outputFile:
        lines = inputFile.readlines()
        lines = lines * args.count
        shuffle(lines)
        outputFile.writelines(lines)