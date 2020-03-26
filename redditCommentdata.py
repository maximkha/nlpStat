# data generated in data folder.

def get(name):
    lines = []
    print("Getting: " + name)
    with open(name) as f:
        lines = f.readlines()
    return " ".join(list(map(lambda x: x.strip(), lines)))