import tweepy
from twitter import *
from networks import Graph
from random import random

# authentication and control of Twitter API

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

# creates connection with Twitter API

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True, compression = True)

# crawls Twitter followers graph of selected user

N = 1000 # nodes limit
P = 0.25 # nodes probability

G = Graph('lovrosubelj') # selected user
G.add_node(G.get_name())
users = {G.get_name(): 0} # Twitter user -> node

todos = [G.get_name()] # unprocessed users
while todos and G.get_n() < N:
  user = todos.pop(0) # Twitter user

  try:
    for id in api.followers_ids(user): # Twitter followers
      if random() < P:
        follower = api.get_user(id).screen_name # follower name
      
        if follower not in users:
          users[follower] = G.add_node(follower) # creates node
          todos.append(follower)
        
        G.add_edge(users[user], users[follower]) # creates edge

        print("'{:s}' ← '{:s}' ({:,d})".format(user, follower, G.get_n()))

        if G.get_n() >= N:
          print()
          break
  except tweepy.TweepError as e:
    print(e)

# prints out standard information of Twitter graph

print(G)

# writes Twitter graph to file in Pajek format

Graph.write(G)
