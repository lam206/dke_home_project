import sqlite3
import tldextract
from sklearn.linear_model import LogisticRegression
import pickle


def pld(url):
    extraction = tldextract.extract(url)
    pld = extraction.domain + '.' + extraction.suffix
    return pld


def make_training_dataset():
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    con.create_function('PLD', 1, pld)
    cur.execute(''' CREATE TABLE plds_tag_factor_sums AS
                    SELECT PLD(mentioned_url) AS pld, sum(factor) AS tag_factor_sum, left_leaning
                    FROM Tweets 
                    JOIN Tags ON Tweets.tweet_id = Tags.tweet_id
                    JOIN factors ON factors.tag_label = Tags.tag_label
                    WHERE left_leaning = 1 or left_leaning = 0
                    GROUP BY PLD(mentioned_url)
                ''')
    cur.execute(''' CREATE TABLE plds_user_factor_sums AS
                    SELECT PLD(mentioned_url) AS pld, sum(factor) AS user_factor_sum, left_leaning
                    FROM Tweets 
                    JOIN Entities ON Tweets.tweet_id = Entities.tweet_id
                    JOIN factors_users ON factors_users.user = Entities.user
                    WHERE left_leaning = 1 or left_leaning = 0
                    GROUP BY PLD(mentioned_url)
                ''')
    cur.execute(''' CREATE TABLE TrainingData AS
                    SELECT plds_tag_factor_sums.pld, tag_factor_sum, user_factor_sum, plds_tag_factor_sums.left_leaning AS left_leaning
                    FROM plds_tag_factor_sums 
                    JOIN plds_user_factor_sums ON plds_user_factor_sums.pld = plds_tag_factor_sums.pld
                ''')
    con.commit()
    con.close()


def train():
    model = LogisticRegression(multi_class='ovr')
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    cur.execute('''
                    SELECT tag_factor_sum, user_factor_sum, left_leaning
                    FROM TrainingData
                ''')
    X_train = []
    y_train = []
    for tup in cur.fetchall():
        X_train.append([tup[0], tup[1]])
        y_train.append(tup[2])
    con.commit()
    con.close()
    model.fit(X_train, y_train)
    with open('trained_model.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    train()