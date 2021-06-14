from SPARQLWrapper import SPARQLWrapper, JSON
import sqlite3
from utilities import get_all_ground_truth_plds

left_and_right_plds = get_all_ground_truth_plds()
sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")


def sparql_query(pld):
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX sioc: <http://rdfs.org/sioc/ns#>
        PREFIX schema: <http://schema.org/>
        PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
        PREFIX wna: <http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#>
        PREFIX dc: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?tweet_id ?user_id ?datetime ?likes ?positive_emotion_intensity ?negative_emotion_intensity 
                        ?mentioned_url
        WHERE {
            ?tweet a sioc:Post ;
                   sioc:id ?tweet_id ;
                   sioc:has_creator/sioc:id ?user_id ;
                   dc:created ?datetime ;
                   schema:interactionStatistic ?likeStatistic ;
                   onyx:hasEmotionSet ?emotions ;
                   schema:citation ?mentioned_url .

            FILTER REGEX (?mentioned_url, "%s") .

            ?likeStatistic schema:interactionType schema:LikeAction ;
                           schema:userInteractionCount ?likes .

            ?emotions onyx:hasEmotion ?em1 .
            ?emotions onyx:hasEmotion ?em2 .
            ?em1 onyx:hasEmotionCategory wna:positive-emotion ;
                 onyx:hasEmotionIntensity ?positive_emotion_intensity .
            ?em2 onyx:hasEmotionCategory wna:negative-emotion ;
                 onyx:hasEmotionIntensity ?negative_emotion_intensity .
        }
        LIMIT 10000
    """ % pld)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def extract_tweets(results):
    tweets = []
    for result in results['results']['bindings']:
        pos = result['positive_emotion_intensity']['value']
        neg = result['negative_emotion_intensity']['value']
        tweet = {
            "tweet_id": result['tweet_id']['value'],
            "user_id": result['user_id']['value'],
            "datetime": result['datetime']['value'],
            "likes": result['likes']['value'],
            "positive_emotion_intensity": "0.0" if pos == "NAN" else pos,
            "negative_emotion_intensity": "0.0" if neg == "NAN" else neg,
            "mentioned_url": result['mentioned_url']['value']
        }
        tweets.append(tweet)
    return tweets


def store_tweets(tweets):
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Tweets (tweet_id int, user_id text, datetime datetime, likes int, '
        'positive_emotion_intensity float, negative_emotion_intensity float, mentioned_url text)')
    for tweet in tweets:
        cur.execute('INSERT INTO Tweets VALUES (%s, \"%s\", \"%s\", %s, %s, %s, \"%s\")'
                    % (tweet["tweet_id"], tweet["user_id"], tweet["datetime"], tweet["likes"],
                       tweet["positive_emotion_intensity"], tweet["negative_emotion_intensity"],
                       tweet["mentioned_url"]))
    con.commit()
    con.close()


def extract_main_table():
    cont = False
    for pld in left_and_right_plds:
        if cont == True:
            print(pld)
            results = sparql_query(pld)
            tweets = extract_tweets(results)
            store_tweets(tweets)
        elif pld == 'prospect.org':  # this has to be the most recent url whose results where stored successfully
            cont = True


def extract_entities_table():
    return


def extract_accounts_table():
    return


def extract_tags_table():
    return


if __name__ == '__main__':
    extract_main_table()
    '''extract_entities_table()
    extract_accounts_table()
    extract_tags_table()'''


