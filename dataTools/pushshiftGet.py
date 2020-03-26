from psaw import PushshiftAPI

def Download(subreddit="all", count=1000):
    api = PushshiftAPI()
    gen = api.search_comments(subreddit=subreddit)
    retCache = []
    while len(retCache) < count:
        retCache.extend(list(next(gen)))
    return retCache

def DownloadIter(subreddit="all", count=500):
    api = PushshiftAPI()
    gen = api.search_comments(subreddit=subreddit, return_batch=True)
    cnum = 0
    while cnum < count:
        data = list(next(gen))
        cnum += len(data)
        #yield list(map(lambda x: x.body.encode("utf-8"), data))
        #"".join(s.split())
        #yield list(map(lambda x: x.body.encode('ascii', 'ignore').decode('ascii').replace('\n', ' ').replace('\r', ''), data))
        yield list(map(lambda x: x.body.encode('ascii', 'ignore').decode('ascii').replace('\n', ' ').replace('\r', ''), data))