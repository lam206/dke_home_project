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
        PREFIX wna: <http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#>
        PREFIX dc: <http://www.purl.org/dc/terms/>

        SELECT DISTINCT ?tweet_id ?user_id ?likes ?positive_emotion_intensity ?negative_emotion_intensity 
                        ?mentioned_url
        WHERE {
            ?tweet a sioc:Post ;
                   sioc:id ?tweet_id ;
                   sioc:has_creator/sioc:id ?user_id ;
                   schema:interactionStatistic ?likeStatistic ;
                   onyx:hasEmotionSet ?emotions ;
                   schema:citation ?mentioned_url .
                
            FILTER REGEX (?mentioned_url, "greatamericanpolitics.com") .
            
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
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


print(len(results["results"]["bindings"]))

