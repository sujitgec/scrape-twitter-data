#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:10:39 2019

@author: suk
"""

import pandas as pd
import tweepy
import jsonpickle

# Consume:
CONSUMER_KEY    = 'SQV2GPdhj9bbOX4AVjeeTMcF8'
CONSUMER_SECRET = 'vCxpf4ModwpZtLzh0UPUNFLyKgo8MfaLGIiE3wPwnzX01adQjV'

# Access:
ACCESS_TOKEN  = '34324567-k8vtlog4hc3nInULbz0Kl1gVnxqCMlMs9tqe4jSQx'
ACCESS_SECRET = 'YZUbEUTjMGRzB2raQXHSmU3vnoYz4W8XJz03F31pXsp89'

# Setup access API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    api = tweepy.API(auth)
    return api
 
# Create API object
api = connect_to_twitter_OAuth() 

def get_save_tweets(filepath, api, query, max_tweets=100, lang='pt'):

    tweetCount = 0

    #Open file and save tweets
    with open(filepath, 'w') as f:

        # Send the query
        for tweet in tweepy.Cursor(api.search,q=query,lang=lang).items(max_tweets):         

            #Convert to JSON format
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

        #Display how many tweets we have collected
        print("Downloaded {0} tweets".format(tweetCount))
        
query = '#Haddad OR #Haddad13 OR #HaddadSim OR' \
        '#EleNao OR #EleNunca OR #Bolsonaro OR' \
        '#Bolsonaro17 OR #SomosTodosBolsonaro OR #Bolsonaro2019 OR' \
        '"haddad" OR "bolsonaro"'

# Get those tweets
get_save_tweets('tweets.json', api, query)

# Convert the json to pandas dataframe
def tweets_to_df(path):
    
    tweets = list(open('tweets_bkp.json', 'rt'))
    
    text = []
    weekday = []
    month = []
    day = []
    hour = []
    hashtag = []
    url = []
    favorite = []
    reply = []
    retweet = []
    follower = []
    following = []
    user = []
    screen_name = []

    for t in tweets:
        t = jsonpickle.decode(t)
        
        # Text
        text.append(t['text'])
        
        # Decompose date
        date = t['created_at']
        weekday.append(date.split(' ')[0])
        month.append(date.split(' ')[1])
        day.append(date.split(' ')[2])
        
        time = date.split(' ')[3].split(':')
        hour.append(time[0]) 
        
        # Has hashtag
        if len(t['entities']['hashtags']) == 0:
            hashtag.append(0)
        else:
            hashtag.append(1)
            
        # Has url
        if len(t['entities']['urls']) == 0:
            url.append(0)
        else:
            url.append(1)
            
        # Number of favs
        favorite.append(t['favorite_count'])
        
        # Is reply?
        if t['in_reply_to_status_id'] == None:
            reply.append(0)
        else:
            reply.append(1)       
        
        # Retweets count
        retweet.append(t['retweet_count'])
        
        # Followers number
        follower.append(t['user']['followers_count'])
        
        # Following number
        following.append(t['user']['friends_count'])
        
        # Add user
        user.append(t['user']['name'])

        # Add screen name
        screen_name.append(t['user']['screen_name'])
        
    d = {'text': text,
         'weekday': weekday,
         'month' : month,
         'day': day,
         'hour' : hour,
         'has_hashtag': hashtag,
         'has_url': url,
         'fav_count': favorite,
         'is_reply': reply,
         'retweet_count': retweet,
         'followers': follower,
         'following' : following,
         'user': user,
         'screen_name' : screen_name
        }
    
    return pd.DataFrame(data = d)
        
tweets_df = tweets_to_df('tweets_bkp.json')
tweets_df.head()
