import sqlite3
from utilities import get_left_ground_truth_plds, get_right_ground_truth_plds
import tldextract


left = get_left_ground_truth_plds()
right = get_right_ground_truth_plds()


# SQLite function definition
def is_leaft_leaning(url):
    extraction = tldextract.extract(url)
    pld = extraction.domain + '.' + extraction.suffix
    if pld in left:
        return 1
    elif pld in right:
        return 0
    else:
        return -1


con = sqlite3.connect("tweetscov19_groundtruth_tweets.db")
cur = con.cursor()

con.create_function('ISLEFTLEANING', 1, is_leaft_leaning)

cur.execute('UPDATE Tweets SET left_leaning = ISLEFTLEANING(mentioned_url)')

con.commit()
con.close()