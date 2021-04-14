# Emotional Contagion

This repository contains the term project of Daniel Mau and Savhanna McLellan for COG403: Seminar in Cognitive Science , taken in winter 2021.


## Project outline
The aim of this project is to determine if emotional contagion is a predictable phenomenon within the domain of social media. 
For a full explanation of this project, see [here]() ** Add link to paper PDF

## Included Data
The data used in this project was gathered from [Twitter](https://developer.twitter.com/en/docs/twitter-api) and analyzed using [SentiStrength](http://sentistrength.wlv.ac.uk/) for overall sentiment strengths.  Training of the model can be done with Training Dataset- Sentiment.zip found in the data directory.

## Dependencies

tweepy, 
matplotlib.pyplot, 
numpy, 
scipy, 
sklearn

## Running

Data contains all the data necessary to train the model and test the model.
Helper contains all the functions necessary to scrap data from Twitter for the training and testing dataset.  (If you want to do the analysis on a different set of tweets with different users).
Model contains the Jupyter notebook used to generate the model and test the predictive accuracy of the model

If you want to get a new training and testing dataset:
1. Run get_tweet.py to get all the tweets that we need to do the analysis
2. Run sentiment.py to get the sentiment score for the tweet well as a sentiment score for the tweet environment 
Otherwise:
3. Get training/testing dataset from data
4. Generate model and prediction by running regression_models.ipynb
