from collections import defaultdict, Counter
import random
from tqdm import tqdm

def GenMarkovModel(stateList):
    transitionList = defaultdict(Counter)
    for i in tqdm(range(1, len(stateList))):
        transitionList[stateList[i - 1]][stateList[i]] += 1
    #turn the counts into probability
    for source, dist in transitionList.items():
        totalCount = sum(count for dest, count in dist.items())
        for dest, count in dist.items():
            transitionList[source][dest] = count / totalCount
    return transitionList

#warning this is an infinte iterator
def GenMarkovChain(transitionList, start):
    cState = start
    while True:
        yield cState
        #Error comp code
        if len(transitionList[cState].items()) == 0:
            #trace
            print(cState)
            print(transitionList[cState])
            print(GetLinkTo(transitionList, cState))
            raise StopIteration
        choices, weights = zip(*[(dest, prob) for dest, prob in transitionList[cState].items()])
        #print(choices)
        #print(weights)
        #print(list(weights))
        #print(list([list(tup) for tup in choices]))
        nState = random.choices(choices, weights = weights)[0]
        cState = nState

def GetLinkTo(transitionList, state, p = False):
    ret = []
    for source, dist in transitionList.items():
        if state in dist:
            if p:
                ret.append((source, dist[state]))
            else:
                ret.append(source)
    return ret