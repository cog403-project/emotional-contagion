'''
Authors: Daniel and Savhanna
April 1, 2021

get_tweets.py
Draft Code For Getting Trending Tweets from Twitter and Gathering Tweets from Friends
'''

import tweepy
import pickle
import datetime
import random


def get_tweets(auth, woeid):
  """
  Save a list of trending tweets based on woeid (i.e. georgraphical location)
  """

    # Authenticate
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True, compression=True)

    # Get list of trending topics
    list_of_trends = api.trends_place(woeid)[0]['trends']
    # list_of_canada_trends = api.trends_place(23424775)[0]['trends']
    # print(list_of_trends)

    # Get about 15 tweets from each trend (50 trends)
    # About 750 tweets
    list_of_tweets = []

    for trend in list_of_trends:
        trend_query = trend['query']
        trending_tweets = api.search(trend_query, lang='en')

        for tweet in trending_tweets:
            list_of_tweets.append(tweet)

    # Save for use later
    pickle.dump(list_of_tweets, open("tweets.p", "wb"))


def get_friend_tweets(tweets, bound, tweet_required, following_limit):
  """
  Save required information required for analysis.  tweets is a list of tweet, bound is the time requirement (e.g. one hour or 2 hour before tweet).
  tweet_required is the approximate limit for tweets gather from each friend and following_limit is the the limit on the follower that we go through
  for each friend of the original tweet
  """

    # Get all tweets generated in the last hour (hours specified by bound)
    tweets_related = []
    time_limit = datetime.timedelta(hours=bound)
    index = 1

    for tweet in tweets:
        # Information to be stored in a list - {User ID, Tweet ID, Time, Following, Tweets, Other}
        print("Going through tweet " + str(index) + " of  " + str(len(tweets)))
        index += 1
        tweet_info = {}

        # Tweets and info related to the friends of the author of tweet
        important_tweet = []
        others = []

        # Tweet info
        user_id = tweet.user.id
        tweet_id = tweet.id
        time_created = tweet.created_at
        followings = api.friends_ids(user_id)

        # Lower bound for inclusion in important tweet
        time_lower_bound = time_created - time_limit

        # Go through all the followers, get tweet_required of their tweets, if
        # it's posted within an hour of tweet, append it to important tweet
        f = 1
        for following in followings[:following_limit]:
            print("Going through friends " + str(f) + " of " + str(len(followings[:following_limit])))
            f += 1
            try:
                other = api.user_timeline(user_id=following, count=tweet_required, include_rts=False, tweet_mode='extended')
                others.append(other)

                for other_tweet in other:
                    other_tweet_created = other_tweet.created_at

                    if time_created >= other_tweet_created >= time_lower_bound:
                        important_tweet.append(other_tweet)
            except tweepy.TweepError:
                print("error")
                continue

        # Store information generated in dictionary
        tweet_info['user'] = user_id
        tweet_info['id'] = tweet_id
        tweet_info['created'] = time_created
        tweet_info['info'] = tweet
        tweet_info['other'] = others
        tweet_info['related_tweets'] = important_tweet

        tweets_related.append(tweet_info)
        # Periodically save it
        pickle.dump(tweets_related, open("temp.p", "ab"))

    # Make sure this object is available for future use
    pickle.dump(tweets_related, open("friend_tweets.p", "wb"))
