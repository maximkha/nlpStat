from redditCommentdata import get
import functools
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import os
import sys
from functools import partial
import itertools
from tqdm import tqdm
from deepchunk import getAllChunks, Chunkify
from simTok import listToIds
import json
from markov import GenMarkovModel, GenMarkovChain
from pathlib import Path

def displayWordChart(wordIDs, data, title="search", dataTitle="count", logScale = False):
    global woidToWord
    wordNames = [woidToWord[woid] for woid in wordIDs]
    y_pos = np.arange(len(wordNames))

    plt.figure()
    
    plt.bar(y_pos, data, align='center', alpha=0.5)
    plt.xticks(y_pos, wordNames, rotation=45, ha='right')
    plt.ylabel(dataTitle)
    plt.title(title)
    
    if logScale:
        plt.yscale('log', basey=2)
    else:
        plt.yscale('linear')
    #plt.show()

# https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

def blackList(string):
    return "http" in string  # or "img" in string

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


print(sys.version)

# https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052
directory = Path.cwd() / r"data"
allFiles = list([str(pathlibFile.resolve()) for pathlibFile in directory.glob('*.fin')])#[1:2]
text = " ".join(list(map(get, allFiles)))

print("Filtering")
words = text.lower().split(" ")  #naively assumes text is continuous
words = list(filter(None, words))
words = list(filter(lambda x: False if hasNumbers(x) or blackList(x) or "_" in x else True, words))

print("WordID")
wordIdList, wordIds = listToIds(words)
woidToWord = {y:x for x,y in wordIds.items()}
print("Chunks")

tokenData = getAllChunks(wordIdList, range(0, 10))

chunky = Chunkify(wordIdList, tokenData)

"""
top20 = tokenData.most_common(20)
print(len(top20))
print(top20[0:5])
for k,v in top20:
    print("'" + " ".join(woidToWord[a] for a in k) + "':" + str(v))

jsonString = json.dumps(chunky)

text_file = open("Output.txt", "w")
text_file.write(jsonString)
text_file.close()
input("...")
"""

model = GenMarkovModel(chunky)

markoviterator = GenMarkovChain(model, chunky[0])

def genNlist(n):
    global markoviterator
    global woidToWord
    ret = ""
    for i in range(n):
        state = next(markoviterator)
        phrase = " ".join([woidToWord[wid] for wid in state])
        ret += phrase + " "
    return ret[:-1]

print(str(len(list(tokenData.items()))/len(wordIdList)))

for i in range(20):
    state = list(model.keys())[i]
    print([woidToWord[wid] for wid in state])
    print(str(tokenData[state]))

while True:
    com = input("genComm> ")
    if com == "q":
        break
    elif com == "s":
        strnum = input("StartID?")
        if not strnum.isnumeric():
            print("not int!")
            continue
        n = int(strnum)
        data = list(tokenData.items())
        if n >= len(data):
            print("input out of range")
            continue
        state, count = data[n]
        print([woidToWord[wid] for wid in state])
        markoviterator = GenMarkovChain(model, state)
    elif com == "p":
        strnum = input("CHID?")
        if not strnum.isnumeric():
            print("not int!")
            continue
        n = int(strnum)
        data = list(tokenData.items())
        if n >= len(data):
            print("input out of range")
            continue
        state, count = data[n]
        print([woidToWord[wid] for wid in state])
    elif com == "f":
        strinput = input("INPT?")
        strwords = strinput.lower().split(" ")  #naively assumes text is continuous
        strwords = list(filter(None, strwords))
        strwords = list(filter(lambda x: False if hasNumbers(x) or blackList(x) or "_" in x else True, strwords))
        fail = False
        strwordIds = []
        for word in strwords:
            if word not in wordIds:
                print("Couldn't find word '" + word + "' in corpus!")
                fail = True
                break
            strwordIds.append(wordIds[word])
        if fail:
            continue
        strchunks = Chunkify(strwordIds, tokenData)
        print(strchunks)
        if len(strchunks) == 0:
            print("No chunks!")
            continue
        print("Last chunk: " + str([woidToWord[wid] for wid in strchunks[-1]]))
        print("All chunk: " + str([woidToWord[wid] for state in strchunks for wid in state]))
        indx = list(tokenData.keys()).index(strchunks[-1])
        print("Last chunk ID:" + str(indx))
    elif com == "r":
        markoviterator = GenMarkovChain(model, chunky[0])
    elif not com.isnumeric():
        print("not int!")
        continue
    else:
        n = int(com)
        print(genNlist(n))