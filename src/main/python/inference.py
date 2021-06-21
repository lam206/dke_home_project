from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
from utilities import get_plds_from_file
from data_pulling import query_tweets, query_tags, extract_tweets, extract_tags, query_entities, extract_entities
import sqlite3
import pickle


def nonMLmodel(factor_sum):
    k = - 50 / np.log(1/9)  # stretch constant to get logistic function with 0.9 confidence at a factor_sum 50.
    return 1 / (1 + np.exp(- factor_sum / k))


def logistic_regression_model(features):
    with open('trained_model.pkl', 'rb') as f:
        estimator = pickle.load(f)
        prediction = estimator.predict([features])
        return prediction[0]


def is_desired_val(desired_vals):
    def h(val):
        if val in desired_vals:
            return True
        else:
            return False
    return h


# for all tags find the factor in 'factors' table and sum
def factor_sum(tags):
    total = 0
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    tag_labels = [tag['tag_label'] for tag in tags]
    con.create_function('ISDESIREDTAG', 1, is_desired_val(tag_labels))
    cur.execute('SELECT factor FROM factors WHERE ISDESIREDTAG(tag_label)')
    for tup in cur.fetchall():
        factor = tup[0]
        if factor > 2 or factor < - 2:
            total += factor
    con.commit()
    con.close()
    return total

def tag_factor_sum(tags):
    total = 0
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    tag_labels = [tag['tag_label'] for tag in tags]
    con.create_function('ISDESIREDVAL', 1, is_desired_val(tag_labels))
    cur.execute('SELECT factor FROM factors WHERE ISDESIREDVAL(tag_label)')
    for tup in cur.fetchall():
        factor = tup[0]
        if factor > 1 or factor < - 1:
            total += factor
    con.commit()
    con.close()
    return total

def user_factor_sum(users):
    total = 0
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    users = [user['user'] for user in users]
    con.create_function('ISDESIREDVAL', 1, is_desired_val(users))
    cur.execute('SELECT factor FROM factors_users WHERE ISDESIREDVAL(user)')
    for tup in cur.fetchall():
        factor = tup[0]
        if factor > 1 or factor < - 1:
            total += factor
    con.commit()
    con.close()
    return total


def nonMLfeatures(tweets, tags, users):
    return tag_factor_sum(tags)


def logistic_regression_featues(tweets, tags, users):
    return [tag_factor_sum(tags), user_factor_sum(users)]


if __name__ == '__main__':
    # data parameters
    sparqlwrapper = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
    input_filename = 'input_data_test'
    last_succesful_pld = None  # Should be none if starting afresh

    # model parameters
    model_name = 'logistic_regression'
    model = logistic_regression_model
    extract_features = logistic_regression_featues

    # code
    input_csv_file = '../../../input_data/' + input_filename + '.csv'
    output_left = '../../../output_data/left.csv'
    output_right = '../../../output_data/right.csv'
    plds = get_plds_from_file(input_csv_file)
    cont = True if last_succesful_pld is None else False
    with (open(output_right, "w")) as right_out:
        with (open(output_left, 'w')) as left_out:
            for pld in plds:
                if cont:
                    print(pld)
                    results_Tweets = query_tweets(pld)
                    results_Tags = query_tags(pld)
                    results_Users = query_entities(pld)
                    tweets = extract_tweets(results_Tweets)
                    tags = extract_tags(results_Tags)
                    users = extract_entities(results_Users)
                    features = extract_features(tweets, tags, users)
                    prediction = model(features)  # 1 is left-leaning, 0 is right-leaning
                    if (prediction > 0.5):
                        left_out.write(pld + ', %.2f\n' % prediction)
                        left_out.flush()
                    else:
                        right_out.write(pld + ', %.2f\n' % (1 - prediction))
                        right_out.flush()
                elif pld == last_succesful_pld:
                    cont = True


