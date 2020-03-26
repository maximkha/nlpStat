import csv

#DEPRECATED
# data from: https://github.com/linanqiu/reddit-dataset
def get(name):
    print("Getting: " + name)
    lines = [l.rstrip() for l in open(name)]
    reader = csv.reader(lines, skipinitialspace=True)
    text = ""
    for r in reader:
        text += r[1]
    return text