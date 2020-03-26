from markov import GenMarkovModel, GenMarkovChain
from deepchunk import getAllChunks, Chunkify
import numpy as np

data = ["a", "b", "c", "d"]
#data = ["a", "b", "c", "d", "a", "b", "c", "d", "a", "b", "c", "d"]
model = GenMarkovModel(data)
print(model)