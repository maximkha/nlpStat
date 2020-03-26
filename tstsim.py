from simTok import *
from dataRedditRepo import get
import functools
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from functools import partial
import itertools
#import tqdm
from tqdm import tqdm

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
    
def wordMulti(wids, wordIdList, tokenCounts, CompDist):
    ret = []
    for wid in wids:
        ret.append(singleWord(wid, wordIdList, tokenCounts, CompDist))
    return ret

def singleWord(wid, wordIdList, tokenCounts, CompDist):
    return (wid,getDiff(CompDist, getTokenDist(wid, wordIdList, tokenCounts)))

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
tokenCounts = Counter(wordIdList)
print("Dists")
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

tokenData = getAllDists(wordIdList, tokenCounts)

searchWord = "good"
searchWoid = wordIds[searchWord]
ranked=Counter()
print("comparing")
for wid, dist in tqdm(tokenCounts.items()):
    #if wid > 1000: print(wid)
    ranked[wid] = getDiff(tokenData[searchWoid], tokenData[wid])

top20 = ranked.most_common()[:-20-1:-1]#[:-20]
#print(top20)
displayWordChart([k for k, v in top20], [v for k, v in top20], "compare " + searchWord, "diff", True)
plt.show()

