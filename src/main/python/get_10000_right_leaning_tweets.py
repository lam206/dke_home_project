import pickle
from Tweet import Tweet
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
regex = ''
with open('../../../input_data/right_train_regex.csv', 'r') as f:
    regex = f.readline()

right_leaning_tweets = []

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
    LIMIT 10000
""" % regex)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    right_leaning_tweets.append(Tweet(result, False))

with open('right_leaning_tweets_10000asc.pickle', 'wb') as f:
    pickle.dump(right_leaning_tweets, f)

