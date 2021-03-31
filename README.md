# Emotional Contagion

This repository contains the term project of Daniel Mau and Savhanna McLellan for COG403: Seminar in Cognitive Science , taken in winter 2021.


## Project outline
The aim of this project is to determine if emotional contagion is a predictable phenomenon within the domain of social media. 
For a full explanation of this project, see [here]() ** Add link to paper PDF

## Included Data
The data used in this project was gathered from [Twitter](https://developer.twitter.com/en/docs/twitter-api) and analyzed using [SentiStrength](http://sentistrength.wlv.ac.uk/) for overall sentiment strengths.

The user network modelling in User Network.ipynb is an adaptation of the code provided [here](https://towardsdatascience.com/how-to-download-and-visualize-your-twitter-network-f009dbbf107b)

## Dependencies
To import and use Tweepy in this API, please run:
> conda install -c conda-forge tweepy

To use the Community package that performs community detection inside User Network.ipynb, please run:
> pip install python-louvain


## Running