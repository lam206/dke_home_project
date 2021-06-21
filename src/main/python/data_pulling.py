from SPARQLWrapper import SPARQLWrapper, JSON
import sqlite3
from utilities import get_plds_from_file, get_all_ground_truth_plds

left_and_right_plds = get_all_ground_truth_plds()  #get_plds_from_file('../../../input_data/input_data_test.csv')
sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")


def query_tweets(pld):
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
        'CREATE TABLE IF NOT EXISTS TestTweets (tweet_id int, user_id text, datetime datetime, likes int, '
        'positive_emotion_intensity float, negative_emotion_intensity float, mentioned_url text)')
    for tweet in tweets:
        cur.execute('INSERT INTO TestTweets VALUES (%s, \"%s\", \"%s\", %s, %s, %s, \"%s\")'
                    % (tweet["tweet_id"], tweet["user_id"], tweet["datetime"], tweet["likes"],
                       tweet["positive_emotion_intensity"], tweet["negative_emotion_intensity"],
                       tweet["mentioned_url"]))
    con.commit()
    con.close()


def extract_main_table(from_pld):
    cont = True if from_pld == None else False
    for pld in left_and_right_plds:
        if cont == True:
            print(pld)
            results = query_tweets(pld)
            tweets = extract_tweets(results)
            store_tweets(tweets)
        elif pld == from_pld:  # this has to be the most recent url whose results where stored successfully
            cont = True


def query_tags(pld):
    sparql.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX sioc: <http://rdfs.org/sioc/ns#>
            PREFIX sioc_t: <http://rdfs.org/sioc/types#>
            PREFIX schema: <http://schema.org/>
            PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
            PREFIX wna: <http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#>
            PREFIX dc: <http://purl.org/dc/terms/>

            SELECT DISTINCT ?tweet_id ?tag_label
            WHERE {
                ?tweet a sioc:Post ;
                       sioc:id ?tweet_id ;
                       schema:citation ?mentioned_url .

                FILTER REGEX (?mentioned_url, "%s") .
                
                ?tweet schema:mentions ?tag .
                ?tag a sioc_t:Tag ;
                     rdfs:label ?tag_label .
            }
            LIMIT 10000
        """ % pld)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


# restart extract at pld "from_pld". If wanna start fres set it to None.
def extract_tags(results):
    tags = []
    for result in results['results']['bindings']:
        tag = {
            "tweet_id": result['tweet_id']['value'],
            "tag_label": result['tag_label']['value']
        }
        tags.append(tag)
    return tags


def store_tags(tags):
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS TestTags (tweet_id int, tag_label text)')
    for tag in tags:
        cur.execute('INSERT INTO TestTags VALUES (%s, \"%s\")' % (tag["tweet_id"], tag["tag_label"]))
    con.commit()
    con.close()


def extract_tags_table(from_pld):
    cont = True if from_pld == None else False
    for pld in left_and_right_plds:
        if cont == True:
            print(pld)
            results = query_tags(pld)
            tags = extract_tags(results)
            store_tags(tags)
        elif pld == from_pld:  # this has to be the most recent url whose results where stored successfully
            cont = True


def query_entities(pld):
    sparql.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX sioc: <http://rdfs.org/sioc/ns#>
            PREFIX sioc_t: <http://rdfs.org/sioc/types#>
            PREFIX schema: <http://schema.org/>
            PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
            PREFIX wna: <http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#>
            PREFIX dc: <http://purl.org/dc/terms/>

            SELECT DISTINCT ?tweet_id ?user
            WHERE {
                ?tweet a sioc:Post ;
                       sioc:id ?tweet_id ;
                       schema:citation ?mentioned_url .

                FILTER REGEX (?mentioned_url, "%s") .

                ?tweet schema:mentions ?user_account .
                ?user_account a sioc:UserAccount ;
                     sioc:name ?user .
            }
            LIMIT 10000
        """ % pld)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def extract_entities(results):
    entities = []
    for result in results['results']['bindings']:
        entity = {
            "tweet_id": result['tweet_id']['value'],
            "user": result['user']['value'].lower()
        }
        entities.append(entity)
    return entities


def store_entities(entities):
    con = sqlite3.connect('tweetscov19_groundtruth_tweets.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Entities (tweet_id int, user text)')
    for entity in entities:
        cur.execute('INSERT INTO Entities VALUES (%s, \"%s\")' % (entity["tweet_id"], entity["user"]))
    con.commit()
    con.close()


def extract_entities_table(from_pld):
    cont = True if from_pld == None else False
    for pld in left_and_right_plds:
        if cont == True:
            print(pld)
            results = query_entities(pld)
            entities = extract_entities(results)
            store_entities(entities)
        elif pld == from_pld:  # this has to be the most recent url whose results where stored successfully
            cont = True


if __name__ == '__main__':
    #extract_main_table('heritage.org')
    extract_entities_table(None)
    #extract_accounts_table()
    #extract_tags_table(None)


