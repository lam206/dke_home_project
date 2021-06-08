import tldextract
import pickle
from preprocess import get_set_of_websites
from Tweet import Tweet
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
tweets_left = True
offset = 0
regex = ''
with open('../../../input_data/left_train_regex.csv', 'r') as f:
    regex = f.readline()

left_leaning_tweets = []

while tweets_left:
    print(offset)
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX sioc: <http://rdfs.org/sioc/ns#>
        PREFIX schema: <http://schema.org/>
        PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
    
        SELECT DISTINCT ?id ?url 
        WHERE {
            ?tweet a sioc:Post ;
                schema:citation ?url ;
                sioc:id ?id .
            FILTER REGEX (?url, "%s") .
        }
        ORDER BY ASC (?id)
        LIMIT 10000
        OFFSET %d
    """ % (regex, offset))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        left_leaning_tweets.append(Tweet(result))

    if len(results["results"]["bindings"]) < 10000:
        tweets_left = False
    else:
        offset += 10000

with open('left_leaning_tweets.pickle', 'wb') as f:
    pickle.dump(left_leaning_tweets, f)

