from SPARQLWrapper import SPARQLWrapper, JSON


_positive_emotion = 'http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#positive-emotion'
_negative_emotion = 'http://www.gsi.dit.upm.es/ontologies/wnaffect/ns#negative-emotion'


class Tweet:
    def __init__(self, result):
        self.id = result['id']['value']
        self.url = result['url']['value']
        self._set_emotions()

    def _set_emotions(self):
        sparql = SPARQLWrapper("https://data.gesis.org/tweetscov19/sparql")
        sparql.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX sioc: <http://rdfs.org/sioc/ns#>
            PREFIX schema: <http://schema.org/>
            PREFIX onyx: <http://www.gsi.dit.upm.es/ontologies/onyx/ns#>
            
            SELECT ?emotionIntensity ?emotionCategory
            WHERE {
                ?tweet a sioc:Post ;
                    onyx:hasEmotionSet/onyx:hasEmotion ?emotion ;
                    sioc:id "%s" .
                ?emotion onyx:hasEmotionIntensity ?emotionIntensity ;
                    onyx:hasEmotionCategory ?emotionCategory .
            }
        """ % self.id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        assert len(results['results']['bindings']) == 2
        for result in results['results']['bindings']:
            if result['emotionCategory']['value'] == _positive_emotion:
                self.positive_emotion_intensity = result['emotionIntensity']['value']
            else:
                assert result['emotionCategory']['value'] == _negative_emotion
                self.negative_emotion_intensity = result['emotionIntensity']['value']

