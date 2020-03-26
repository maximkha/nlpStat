from collections import Counter
from tqdm import tqdm

def getAllChunks(tokens, ns=range(10)):#n=10):
    chunkCounts = Counter()
    for indx in tqdm(range(len(tokens))):
        #print("on: " + str(tokens[indx]))
        for cn in ns:
            #print(str(indx + 1))
            if indx < cn:
                continue
            ##tokenChunk = tokens[indx-cn-1:indx]
            #print(len(tokens[indx-cn:indx + 1]))
            ##chunkCounts[tuple(tokenChunk)] += 1 #(1/(cn+1))
            chunkCounts[tuple(tokens[indx-cn:indx + 1])] += 1
            #print(chunkCounts[tuple(tokenChunk)])
    return chunkCounts

def Chunkify(tokens, deepTokens):
    resTokens = []
    ctok = []
    for i in range(len(tokens)):  #tqdm(range(len(tokens))):
        #print("on: " + str(tokens[i]))
        ctok.append(tokens[i])
        #print(str(deepTokens[tuple(ctok)]))
        if deepTokens[tuple(ctok)] < 2:
            ctok.pop()
            resTokens.append(tuple(ctok))
            ctok = []
            ctok.append(tokens[i])
    resTokens.append(tuple(ctok))
    return resTokens