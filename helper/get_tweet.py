import tweepy
import pickle
import datetime
import random

def get_trending_tweets(auth, woeid, output_file):

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

    # pickle.dump(list_of_tweets, open("tweets.p", "wb"))
    pickle.dump(list_of_tweets, open(output_file, "wb"))


def get_list_of_users(tweets):

    list_of_user = []

    for tweet in tweets:
        user_id = tweet.user.id
        if user_id not in list_of_user:
            list_of_user.append(user_id)

    return list_of_user


def get_inital_tweets(list_of_users, amount, output_file):

    tweet_return = {}
    index = 1

    for user in list_of_users:
        print("Going through user " + str(index) + " of  " + str(len(list_of_users)))
        index += 1
        try:
            user_id = user
            other = api.user_timeline(user_id=user_id, count=amount,
                                      include_rts=False, tweet_mode='extended')

            if user_id not in tweet_return:
                tweet_return[user_id] = {}

            tweet_return[user_id]['tweets'] = other
            #friends = api.friends_ids(user_id) - disabled due to rate limit
            #tweet_return[user_id]['friends'] = friends

        except tweepy.TweepError:
            print("error")
            continue

    pickle.dump(tweet_return, open(output_file, "wb"))
    
def get_friends_tweets(list_of_user, tweet_required, following_limit):

    # Get all tweets from friends of list_of_users
    #friend_tweets = {}
    index = 1

    for user in list_of_user:
        print("Going through user " + str(index) + " of  " + str(len(list_of_user)))
        index += 1

        # Tweets and info related to the friends of the author of tweet
        each_friend_tweet = {}

        # User info
        user_id = user
        friends = api.friends_ids(user_id)

        # Go through all the friends and get all their tweets
        f = 1
        for friend in friends[:following_limit]:
            print("Going through friends " + str(f) + " of " + str(len(friends[:following_limit])))
            f += 1
            try:
                other = api.user_timeline(user_id=friend, count=tweet_required, include_rts=False, tweet_mode='extended')
                each_friend_tweet[friend] = other
            except tweepy.TweepError:
                print("error")
                continue

        # Store information generated in dictionary
        #friend_tweets[user_id] = each_friend_tweet
        # File name generation
        file_name = str(user_id) + '.p'
        # Periodically save it
        pickle.dump(each_friend_tweet, open(file_name, "wb"))
