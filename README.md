# DKE 2021 Home Project


This repository contains Leon Mlodzian's home project submission for the Data and Knowledge Engineering class 2021 at Heinrich Heine University.  
The project exercise can be completed at home, using the expertise and skill sets acquired in the DKE 2021 lectures.

The output of the evaluation script (invoked with `gradle run`) is in `gradle_run_output.txt` in the root folder. There 
one can see my model achieved an accuracy of 86%.


## Training Data

I used the local SQL database tool SQLite to store the results of SPARQL queries locally and to do data analysis on.
I stored three main tables, one for each of the following queries, which retrieve tweet, tag and user mention information,
respectively.



```
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
```

```
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
```

```
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
```
Note: ```%s``` in the `FILTER` expressions is replaced with a pld in my code.

With analysed the data and engineered two features with SQL, one based on tag mentions and one on user mentions.
I created the table TrainingData with the schema `(pld, tag_mention_feature value, user_mention_feature value, grund_truth label)`.
I labelled left_leaning sites as `1` and right-leaning sites as `0`.


## Trainig
I used the function "train()" in "src/main/python/training.py" to fetch the training data from the TrainingData table
and train a logistic regression model using sklearn (model.fit(...)). It saves the model as trained_model.pkl using pickle.


## Inference
"src/main/python/inference.py" performs inference when executed. The script is parameterised by model choice and csv
input file, which contains the plds to be classified.


## Folder Structure:
* **input_data**:  contains the training data: one CSV file listing all PLDs with left vs. right bias classification, respectively. The test data will be added to this folder. 
* **output_data**: folder that must be populated with the results of the home project. Please export all PLDs your algorithm classifies as left-biased to a file called 'left.csv' and all PLDs it classifies as right-biased to 'right.csv'. Please refer to the task description in the assignment folder for information on the format.  
* **src**: add your code here in the suitable subfolder(s) (depending on whether you use Java or Python).
* **assignment**: contains a more detailed description of the task and the required output. 


