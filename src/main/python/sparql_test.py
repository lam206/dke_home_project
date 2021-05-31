import tldextract
import pickle
from preprocess import get_set_of_websites
from Tweet import Tweet

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
sparql.setQuery("""
    PREFIX sioc: <http://rdfs.org/sioc/ns#>

    select distinct ?tweet
    where {
    ?tweet a sioc:Post .
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


print(len(results["results"]["bindings"]))

