import tldextract
import pickle
from preprocess import get_set_of_websites
from Tweet import Tweet

from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
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
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

left_leaning_websites = get_set_of_websites('../../../input_data/left_train.csv')
right_leaning_websites = get_set_of_websites('../../../input_data/right_train.csv')
left_leaning_tweets = []
right_leaning_tweets = []

for result in results["results"]["bindings"]:
    url = result["url"]["value"]
    ext = tldextract.extract(url)
    pld = ext.domain + '.' + ext.suffix
    if pld in left_leaning_websites:
        left_leaning_tweets.append(Tweet(result))
    if pld in right_leaning_websites:
        right_leaning_tweets.append(Tweet(result))

with open('left_leaning_tweets.pickle', 'wb') as f:
    pickle.dump(left_leaning_tweets, f)
with open('right_leaning_tweets.pickle', 'wb') as f:
    pickle.dump(right_leaning_tweets, f)

