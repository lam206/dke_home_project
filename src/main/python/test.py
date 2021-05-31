import pickle

file = 'right_leaning_tweets.pickle'

with open(file, 'rb') as f:
    # count how many gt plds are mentioned in each tweet
    s = {}
    tweets = pickle.load(f)
    for tweet in tweets:
        id = tweet.id
        if id in s.keys():
            s[id] += 1
        else:
            s[id] = 1
    # print which tweets show more than one pld
    for k in s.keys():
        if s[k] > 1:
            print(k)

# this code reveals that no tweet has more than one gt pdl. So every training data tweet contains exactly one pld from
# the ground truth set -> makes everything easier as we can assume only one pld per tweet.
