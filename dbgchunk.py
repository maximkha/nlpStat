from deepchunk import getAllChunks, Chunkify
from markov import GenMarkovModel, GenMarkovChain, GetLinkTo

data = ["a", "b", "e", "d", "a", "b", "c", "d", "a", "b", "c", "d", "a", "b", "c", "d"]
chunks = getAllChunks(data, range(2))
print(chunks)
chunked = Chunkify(data, chunks)
print(chunked)
model = GenMarkovModel(chunked)
print(model)
generator = GenMarkovChain(model, chunked[0])
tst = []
tst.append(next(generator))
tst.append(next(generator))
tst.append(next(generator))
tst.append(next(generator))

tst.append(next(generator))
tst.append(next(generator))
tst.append(next(generator))
tst.append(next(generator))
print(tst)