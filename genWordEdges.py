import json
from collections import Counter, defaultdict
from simTok import getAllDists, getTokenDist, getDiff, listToIds
from redditCommentdata import get
from tqdm import tqdm
import os
import functools
from multiprocessing import Pool
from p_tqdm import p_uimap
#from tqdm.contrib.concurrent import process_map
import itertools
from random import shuffle,seed
from pathlib import Path
import time

seed(9001)

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

def blackList(string):
    return "http" in string  # or "img" in string

def Worker(allWids, tokenData, widA):
    from simTok import getDiff
    edges = dict()
    for widB in allWids:
        edges[widB] = getDiff(tokenData[widA], tokenData[widB])
    return (widA, edges)

def BatchWorker(allWids, tokenData, widAs):
    from simTok import getDiff
    import time
    ret = []
    #print("P["+str(widAs[0])+"]: Start!")
    t = time.time()
    for i in range(len(widAs)):
        widA = widAs[i]
        if time.time() - t > 60:
            print("")
            print("P["+str(widAs[0])+"]: Alive(" + str(i) + "/" + str(len(widAs)) + ")!")
            t = time.time()
        edges = dict()
        #print("P["+str(widAs[0])+"]: " + str(widA))
        for widB in allWids:
            edges[widB] = getDiff(tokenData[widA], tokenData[widB])
        ret.append((widA, edges))
    #print("P["+str(widAs[0])+"]: Job Done!")
    return ret

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == '__main__':
    directory = Path.cwd() / r"data"
    allFiles = list([str(pathlibFile.resolve()) for pathlibFile in directory.glob('*.fin')])#[1:2]
    text = " ".join(list(map(get, allFiles)))

    print("Filtering")
    words = text.lower().split(" ")  #naively assumes text is continuous
    words = list(filter(None, words))
    words = list(filter(lambda x: False if hasNumbers(x) or blackList(x) or "_" in x else True, words))

    print("WordID")
    wordIdList, wordIds = listToIds(words)
    woidToWord = {y: x for x, y in wordIds.items()}

    tokenCounts = Counter(wordIdList)

    tokenData = getAllDists(wordIdList, tokenCounts, 11)
    tokenData = dict({wid: dict(dist) for wid, dist in dict(tokenData).items()})

    allData = defaultdict(lambda: dict())
    ids = wordIds.values()
    ids = list(ids)
    shuffle(ids)

    embedded = functools.partial(BatchWorker, ids, tokenData)

    #dataFragments = process_map(embedded, ids, chunksize=4)
    
    batchedWids = list(batch(ids, 100))
    dataFragments = p_uimap(embedded, batchedWids) #p_map(embedded, batchedWids)
    #pool = Pool(processes=6)
    #dataFragments = pool.imap_unordered(embedded, batchedWids)
    
    dataFragments = list(itertools.chain.from_iterable(dataFragments)) #stick the lists together

    print("DeFragmenting")
    for fragment in tqdm(dataFragments):
        allData[fragment[0]] = fragment[1]
    
    #for widA in tqdm(ids):
    #    for widB in ids:
    #        allData[widA][widB] = getDiff(tokenData[widA], tokenData[widB])

    print("SAVING EDGE")
    print(len(allData.items()))
    
    with open('WordEdges.json', 'w') as outfile:
        json.dump(allData, outfile)