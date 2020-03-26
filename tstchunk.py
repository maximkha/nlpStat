from dataRedditRepo import get
import functools
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import os
import sys
from functools import partial
import itertools
#import tqdm
from tqdm import tqdm
from deepchunk import getAllChunks, Chunkify
from simTok import listToIds
import json
from markov import GenMarkovModel, GenMarkovChain

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
directory = r'C:\Users\maxim\Desktop\js\WordFlow\redditData'
allFiles = list(map(lambda x: directory + "\\" + x, filter(lambda x: '.csv' in x, os.listdir(directory))))[0:5]
text = " ".join(list(map(get, allFiles)))
#text = get(r"C:\Users\maxim\Desktop\js\WordFlow\redditData\learning_space.csv")

print("Filtering")
words = text.lower().split(" ")  #naively assumes text is continuous
words = list(filter(None, words))
words = list(filter(lambda x: False if hasNumbers(x) or blackList(x) or "_" in x else True, words))

print("WordID")
wordIdList, wordIds = listToIds(words)
woidToWord = {y:x for x,y in wordIds.items()}
#woid = wordIds[word.lower()]
print("Chunks")
"""
RESgood = getTokenChunks(wordIds["good"], wordIdList, tokenCounts)
displayWordChart([itm[0] for itm in RESgood.most_common(20)], [itm[1] for itm in RESgood.most_common(20)], "good")

RESbad = getTokenChunks(wordIds["bad"], wordIdList, tokenCounts)
displayWordChart([itm[0] for itm in RESbad.most_common(20)], [itm[1] for itm in RESbad.most_common(20)], "bad")

RESother = getTokenChunks(wordIds["other"], wordIdList, tokenCounts)
displayWordChart([itm[0] for itm in RESother.most_common(20)], [itm[1] for itm in RESother.most_common(20)], "other")

RESwhy = getTokenChunks(wordIds["why"], wordIdList, tokenCounts)
displayWordChart([itm[0] for itm in RESwhy.most_common(20)], [itm[1] for itm in RESwhy.most_common(20)], "why")

displayWordChart([wordIds[a] for a in ["bad", "other", "why"]], [getDiff(RESgood, b) for b in [RESbad, RESother, RESwhy]], "compare good", "diff", True)
"""

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