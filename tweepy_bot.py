import emoji
import tweepy
import requests
import sys
import time 
import os

from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tweepy Bot for Kiss Ebooks
@kiss_ebooks
Comes with no Warranty whatsoever!
Feel free to use and share!!!
You will need your own API keys to make this script work.
Go to https://developer.twitter.com/en/apps and get your API keys for the script to work
Replace where indicated by any of your favorite method
Check the tweepy documentation for more information on how to use tweepy
including how and where to replace the API keys
http://docs.tweepy.org/en/latest/

"""
 
__author__ = 'Edgardo Santiago'
__version__ = '0.2.8'
__status__ = 'Development'
 
# Maintenance stuff:
#   Things to do:
#   use regex to search for emojis
#     regex = re.compile(r'\d+(.*?)(?:\u263a|\U0001f645)')
#     RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
#   use regex to search for skin color emoji
#   Save all on a list and/or create a database
#   Integrate generated text and autopost for a determined period of time
  
# Setting up tweepy, USE YOUR OWN KEYS!!!
# You will need the api keys to run this script
# Please refer to the tweepy documentation on how to get your own api keys 
auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api = tweepy.API(auth)
 
# tweepyBot class
class tweepyBot(object):
    def __init__(self):
        print('*****Welcome to the Tweepy Bot!*****')
        print('************MAIN MENU**************')  
        print()
        choice = input(
            '''
A: Get the information on a user
B: Post a tweet
C: Get tweets from my timeline
D: Do a keyword search
E: Get the trending topics
F: Show Friends
G: Batch Delete
H: Single Delete
Q: Quit/Log Out

Please enter your choice: 
''')

        if choice=='A' or choice =='a':
            self._get_user_info()
 
        elif choice=='B' or choice =='b':
            self._update_tweets()
 
        elif choice=='C' or choice =='c':
            self._get_tweets()
 
        elif choice=='D' or choice=='d':
            self._keyword_search()
           
        elif choice=='E' or choice=='e':
           self._get_trending()
        
        elif choice=='F' or choice=='f':
            self._show_friends()
        
        elif choice=='G' or choice=='g':
            self._batch_delete()
        
        elif choice=='H' or choice=='h':
            self._single_delete()

        elif choice=='Q' or choice=='q':
            sys.exit()

        else:
            print('You must only select either [A-H] or Q.')
            time.sleep(1)
            print('Good Bye!')
            sys.exit()
               
# Get and print my tweets
    def _get_tweets(self, *args, **kwargs):
        try:
            myTimeLine = api.home_timeline()            
            for item in myTimeLine:
                print(item.text)
        except Exception as e:
            print(e)
        finally:
            return myTimeLine

# Get the information of a user
    def _get_user_info(self, *args, **kwargs):
        userName = str(input('What is the user name? '))
        try:
            user = api.get_user(userName)
            user_info = {
            'screen_name': user.screen_name,
            'location': user.location,
            'user_id': user.id,
            'description': user.description
            }
            print(
                'user info = ',
                user_info['screen_name'],
                user_info['location'],
                'user id = ',
                user_info['user_id'],
                'user description = ',
                user_info['description'])           
        except Exception as e:
            print(e)
        finally:
            print('Done!')
 
# Do a Keyword Search
    def _keyword_search(self, *args, **kwargs):
        keyword = str(input('What do you want to search? '))
        try:
            api_search = api.search(q=keyword, lang='en', rpp=10)
            tweets = [item.text for item in api_search]
            tweets_user_names = [item.user.name for item in api_search]
            for tweet,user in zip(tweets,tweets_user_names):
                print(user+':'+tweet)
        except Exception as e:
            print(e)
        finally:  
         print('Done!')
       
# Getting the trending topics
    def _get_trending(self, *args, **kwargs):
        try:
            trending = api.trends_place(1)
            for trend in trending[0]['trends']:
                print(trend['name'])
        except Exception as e:
            print(e)
        finally:  
         print('Done!')

# Pagination
    def _show_friends(self, *args, **kwargs):
        for friend in tweepy.Cursor(api.friends).items():
            print(friend._json['name'])
 
# Update the tweets
    def _update_tweets(self, *args, **kwargs):
        string = str(input('What do you want to tweet? '))
        try:
            api.update_status(string)
        except Exception as e:
            print(e)
        finally:
            print(string)

# Batch delete 
    def _batch_delete(self, *args, **kwargs):
        print('Are you sure you want to BATCH_DELETE?:')
        print('There is no turning back')
        do_delete = input(str('Enter yes to delete: ').lower())
        if do_delete == 'yes' or do_delete == 'y':
            for status in tweepy.Cursor(api.user_timeline).items():
                try:
                    api.destroy_status(status.id)
                    print('Deleted: ', status.id)
                except:
                    print('Failed to delete:', status.id)
        else:
            print('Did not delete...')


# Single delete
    def _single_delete(self, *args, **kwargs):
        item_list = []
        def add_element(dict,key,value):
            if key not in dict:
                dict[key] = []
                dict[key].append(value)
        for item in tweepy.Cursor(api.user_timeline).items():
            item_list.append(list(['ID:',item.id, item._json['text'], item._json['user']['name']]))
            print(item_list)
        #api.destroy_status(item_list[1][1])
        
    	    
def main():
    tweepyBot()

if __name__ == "__main__":
    main()