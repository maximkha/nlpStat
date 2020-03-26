from collections import defaultdict
from collections import Counter
from tqdm import tqdm
from math import sqrt

def bayesian(BAndA, a, b):
    return (BAndA * a) / b

def clamp(a, amin, amax):
    return min(amax,max(amin, a))

def getTokensLeft(start, n, tokens):
    return tokens[clamp(start - n, 0, len(tokens)):clamp(start, 0, len(tokens))]

def getTokensRight(start, n, tokens):
    return tokens[clamp(start, 0, len(tokens)):clamp(start + n, 0, len(tokens))]

def listToIds(list):
    d = defaultdict(lambda: len(d))
    return ([d[x] for x in list], d)

def getDiff(a, b):
    #diff = Counter()
    #diff = Counter({key: abs(b.get(key, 0) - value) for key, value in a.items()}) #a - b
    #return sum([abs(b.get(key, 0) - value) for key, value in a.items()]) #sum(diff.values())
    return sqrt(sum([(b.get(key, 0) - value)**2 for key, value in a.items()]))
    #return sqrt(sum([abs(b.get(key, 0) - value) for key, value in a.items()]))

def getTokenDist(tokenID, tokens, tokenCounts, n=10):
    #tokenCounts = Counter(tokens)
    ret = []
    for indx in range(len(tokens)):
        if tokens[indx] != tokenID:
            continue
        ret.extend(getTokensLeft(indx, n, tokens))
        #ret.extend(getTokensRight(indx, n, tokens))

    retCount = Counter(ret)
    retCountSum = sum(retCount.values())
    tokenCountsSum = sum(tokenCounts.values())
    for token in retCount.keys():
        retCount[token] = bayesian(retCount[token]/retCountSum, tokenCounts[tokenID]/tokenCountsSum, tokenCounts[token]/tokenCountsSum)
    return retCount

# https://stackoverflow.com/questions/26367812/appending-to-list-in-python-dictionary
def getAllDists(tokens, tokenCounts, n=10):
    dat = defaultdict(list)
    tokenCountsSum = sum(tokenCounts.values())
    for indx in range(len(tokens)):
        dat[tokens[indx]].extend(getTokensLeft(indx, n, tokens))
        dat[tokens[indx]].extend(getTokensRight(indx, n, tokens))
    ret = defaultdict(Counter)
    for wid, data in tqdm(dat.items()):
        ret[wid] = Counter(data)
        retSum = sum(ret[wid].values())
        for token in ret[wid].keys():
            ret[wid][token] = bayesian(ret[wid][token] / retSum, tokenCounts[wid] / tokenCountsSum, tokenCounts[token] / tokenCountsSum)
    return ret