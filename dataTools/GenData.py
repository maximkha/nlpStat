import argparse
import sys
from pushshiftGet import DownloadIter
from types import SimpleNamespace

def getArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Downloads only reddit comment text, no context, just text")
    parser.add_argument("-s", "--sub", required=True, help="The subreddit to scrape.")
    parser.add_argument("-o", "--output", required=True, help="Your destination output file.")
    parser.add_argument("-c", "--count", required=True, type=int, help="Number of entries")
    options = parser.parse_args(args)
    return options

args = getArgs(sys.argv[1:])
#args = SimpleNamespace(sub="nasa", count=10000, output="out.txt")

#print(args)
#print(args.count)
#print(args.output)
#print(args.sub)

gen = DownloadIter(args.sub, args.count)

chunkNum = 0
with open(args.output, 'w', encoding="utf-8") as outfile:
    for listOfText in gen:
        #print(listOfText)
        print("Writing chunk " + str(chunkNum))
        outfile.write('\n'.join(listOfText) + '\n')
        print("Wrote " + str(len(listOfText)) + " lines")
        chunkNum += 1