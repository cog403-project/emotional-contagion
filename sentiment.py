import subprocess
import shlex
import os.path
import sys
import pickle
import datetime

# Helper Functions
def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "'"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8")
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")
    return stdout_text + " " + sentiString

def get_list_of_users(tweets):

    list_of_user = []

    for tweet in tweets:
        user_id = tweet.user.id
        if user_id not in list_of_user:
            list_of_user.append(user_id)

    return list_of_user


def get_related_tweet(tweets, end_time, time_bound):
    time_limit = datetime.timedelta(hours=time_bound)
    lower_bound = end_time - time_limit
    tweet_return = {}

    for user in tweets:

        friend_tweets = tweets[user]

        for tweet in friend_tweets:

            tweet_created = tweet.created_at

            if end_time >= tweet_created >= lower_bound:
                tweet_id = tweet.id
                tweet_return[tweet_id] = tweet

    return tweet_return
    
if __name__ == '__main__':

    SentiStrengthLocation = ""  # The location of SentiStrength on your computer
    SentiStrengthLanguageFolder = ""  # The location of the unzipped SentiStrength data files on your computer

    if not os.path.isfile(SentiStrengthLocation):
        print("SentiStrength not found at: ", SentiStrengthLocation)
    if not os.path.isdir(SentiStrengthLanguageFolder):
        print("SentiStrength data folder not found at: ",
              SentiStrengthLanguageFolder)

    # Location of ".p" files, , e.g. C:/Documents/Tweets/
    directory = ""
    
    # ONLY NEEDED IF USING CONVERT FUNCTION
    test_directory = ""
    
    # Location where you want to store the file for sentiment analysis, e.g. C:/Documents/Sentiment/
    sent_directory = ""

    # Load your initial tweet - REMEMBER TO SPECIFIC FILE LOCATION
    initial_tweets = pickle.load(open(
        "",
        "rb"))

    # If you have file that you have analyzed, load it, comment it out if you do not have a data_analyzed.p file
    # already_analyzed = pickle.load(open("data_analyzed.p", "rb"))
    
    skip = []
    
    # Comment it out if not needed
    #for uid in already_analyzed:
    #    skip.append(uid)

    print(skip)

    data_analyzed = pickle.load(open("data_analyzed.p", "rb"))
    index = 1
    
    # Analyze the tweet sentiment
    for t in initial_tweets:
        print(
            'Analyzing user ' + str(index) + " of " + str(len(initial_tweets)))
        index += 1

        if t not in skip:

            sentiment_for_tweet = {}
            average_sentiment_for_tweet = {}

            user_i = t
            save_file_s = sent_directory + str(user_i) + '_sent.p'
            save_file_a = sent_directory + str(user_i) + '_avg.p'

            tweets = initial_tweets[t]
            print("Analyzing " + str(len(tweets['tweets'])) + " tweets")

            for tweet in tweets['tweets']:
                # print(tweet)
                # Tweet info
                user_id = tweet.user.id
                tweet_id = tweet.id
                time_created = tweet.created_at
                tweet_text = tweet.full_text
                file_name = directory + str(user_id) + '.p'

                # Sentiment for original tweet
                sentiment = RateSentiment(tweet_text)[:4].split()
                sentiment = [int(sentiment[0]), int(sentiment[1])]
                combined = sentiment[0] + sentiment[1]
                sentiment_for_tweet[tweet_id] = {'sentiment': sentiment}
                sentiment_for_tweet[tweet_id]['combined'] = combined
                sentiment_for_tweet[tweet_id]['user'] = user_id

                average_sentiment_for_tweet[tweet_id] = {'sentiment': sentiment}
                average_sentiment_for_tweet[tweet_id]['combined'] = combined

                if os.path.exists(file_name):
                    friend_tweets = pickle.load(open(file_name, "rb"))
                    if len(friend_tweets) < 1000:
                        if user_id not in data_analyzed:
                            data_analyzed[user_id] = []

                        data_analyzed[user_id].append(tweet_id)
                        related_friend_tweets = get_related_tweet(friend_tweets,
                                                                  time_created, 1)

                        if 'friend' not in sentiment_for_tweet[tweet_id]:
                            sentiment_for_tweet[tweet_id]['friend'] = {}

                        total_sentiment = []
                        print("Analyzing " + str(
                            len(related_friend_tweets)) + " related tweets")

                        if len(related_friend_tweets) > 0:
                            for f in related_friend_tweets:
                                f_tweet = related_friend_tweets[f]
                                f_tweet_id = f_tweet.id
                                f_tweet_text = f_tweet.full_text

                                f_sentiment = RateSentiment(f_tweet_text)[:4].split()
                                f_sentiment = [int(f_sentiment[0]), int(f_sentiment[1])]
                                f_combined = f_sentiment[0] + f_sentiment[1]
                                total_sentiment.append(f_combined)

                                sentiment_for_tweet[tweet_id]['friend'][f_tweet_id] = {
                                    'sentiment': sentiment}
                                sentiment_for_tweet[tweet_id]['friend'][f_tweet_id][
                                    'combined'] = f_combined


                            average_s = sum(total_sentiment) / len(total_sentiment)
                            average_sentiment_for_tweet[tweet_id]['friend'] = average_s

            pickle.dump(sentiment_for_tweet, open(save_file_s, "wb"))
            pickle.dump(average_sentiment_for_tweet, open(save_file_a, "wb"))
            pickle.dump(data_analyzed, open("data_analyzed_1.p", "wb"))
