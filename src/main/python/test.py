import sqlite3
from utilities import get_left_ground_truth_plds, get_right_ground_truth_plds
import tldextract
import re
import pickle


'''def regex(regex, string):
    match = re.search(regex, string)
    if match != None:
        return 1
    else:
        return 0


con = sqlite3.connect("tweetscov19_groundtruth_tweets.db")
cur = con.cursor()

con.create_function('REGEXP', 2, regex)

cur.execute('SELECT mentioned_url FROM TestTweets JOIN TestTags WHERE mentioned_url REGEXP ".*yesmagazine.org.*"')
for tup in cur.fetchall():
    print(tup)

con.commit()
con.close()'''



"""def pld(url):
    extraction = tldextract.extract(url)
    pld = extraction.domain + '.' + extraction.suffix
    return pld

con = sqlite3.connect("tweetscov19_groundtruth_tweets.db")
cur = con.cursor()

con.create_function('PLD', 1, pld)

cur.execute('''SELECT PLD(mentioned_url), sum(factor) 
            FROM Tweets 
            JOIN Tags ON Tweets.tweet_id = Tags.tweet_id
            JOIN factors ON factors.tag_label = Tags.tag_label
            GROUP BY PLD(mentioned_url) 
            ORDER BY count(*)''')
cur.execute('''SELECT PLD(mentioned_url), sum(factor) 
            FROM Tweets 
            JOIN Entities ON Tweets.tweet_id = Entities.tweet_id
            JOIN factors_users ON factors_users.user = Entities.user
            GROUP BY PLD(mentioned_url) 
            ORDER BY count(*)''')
for tup in cur.fetchall():
    print(tup)

con.commit()
con.close()"""

'''select count(*), positive_emotion_intensity < 1, negative_emotion_intensity < 1
from Tweets
where left_leaning = 0
group by positive_emotion_intensity < 1, negative_emotion_intensity < 1'''

with open('trained_model.pkl', 'rb') as f:
    estimator = pickle.load(f)
    coefficients = estimator.coef_
    intercept = estimator.intercept_
    print(coefficients)
    print(intercept)

