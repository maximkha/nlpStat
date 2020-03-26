import argparse
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import statistics

def getArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Histogram of word count")
    parser.add_argument("-i", "--input", required=True, help="The input file.")
    options = parser.parse_args(args)
    return options
    
args = getArgs(sys.argv[1:])

if not Path(args.input).is_file():
    print("The input file does not exist!")
    exit()

with open(args.input) as infile:
    textList = infile.readlines()
    wordCounts = list(map(lambda x: len(list(filter(None,x.split(' ')))), textList))
    plt.hist(wordCounts, 1000)
    mean = statistics.mean(wordCounts)
    print("MEAN: " + str(mean))
    median = statistics.median(wordCounts)
    print("MEDIAN: " + str(median))
    plt.axvline(mean, linestyle='dashed', linewidth=1)
    plt.axvline(median, linestyle='solid', linewidth=1)
    plt.show()