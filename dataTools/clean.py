import re
import argparse
import sys
from pathlib import Path

removedFilter = re.compile(r"\[removed\]")
deletedFilter = re.compile(r"\[deleted\]")
linkCapture = re.compile(r"\[(.*?)\]\((.*?)\)")
urlInStr = re.compile(r"https?://[^\s]+")
numInWord = re.compile(r"\w*\d\w")
nonStandardChar = re.compile(r"[^\w\s\.?!]")
moreTwoSpaces = re.compile(r"[ ]{2,}")
AllFilters = [removedFilter, deletedFilter, linkCapture, urlInStr, numInWord, nonStandardChar]
#botTest = re.compile(r"I am a bot and this action was performed automatically", re.IGNORECASE)
botTest = re.compile(r"I am a bot", re.IGNORECASE)

def getArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Filters reddit comment text.")
    parser.add_argument("-i", "--input", required=True, help="The input file.")
    parser.add_argument("-o", "--output", required=True, help="Your destination output file.")
    options = parser.parse_args(args)
    return options
    
args = getArgs(sys.argv[1:])

def filterText(text):
    global AllFilters
    cText = text
    for filter in AllFilters:
        cText = filter.sub('', cText)
    return cText

if not Path(args.input).is_file():
    print("The input file does not exist!")
    exit()

removePunct = re.compile(r"[.?!]")
removeComma = re.compile(r"[,]")

cnt = 1
kept = 1
with open(args.input) as infile:
    with open(args.output, 'w', encoding="utf-8") as outfile:
        line = infile.readline()
        while line:
            #print("Line {}: {}".format(cnt, line.strip()))
            #urlInStr.findall()
            line = infile.readline()
            #replace '.','?','!' with ' '
            #check comma replacement
            line = removePunct.sub(' ', line)
            line = removeComma.sub(' ', line)
            line = moreTwoSpaces.sub(' ', line)
            processedText = filterText(line)
            cnt += 1

            if bool(botTest.search(line)):
                continue
            if len(processedText.strip()) == 0:
                continue
            kept += 1
            outfile.write(processedText)  # already has the newline from old file
print("Processed " + str(cnt) + " lines (" + str(cnt-kept) + " removed).")