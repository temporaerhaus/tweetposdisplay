import tweepy
import serial
from time import sleep
import re
import os

ser = serial.Serial('COM3')  # open serial port
ser.write("\x1F\x11\x14".encode())
blankBeginning = "                    "

# Populate your twitter API details as environment variables
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

search_text = ["verschwoerhaus", "jhacktulm"]

while True:
    for t in search_text:

        search_result = api.search(q = t, tweet_mode='extended')
        for i in search_result:
            if hasattr(i, 'retweeted_status'):
                i = i.retweeted_status
            if not '@' is i.full_text[0]:
                #print(i)
                ser.write(("\x10\x00@"+i.user.screen_name).encode())

                text = blankBeginning+i.full_text+blankBeginning

                text = text.replace('\n', ' ').replace('\r', '')
                text = re.sub(
                    r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                    '', text)

                for x in range(0,len(text)-18):
                    ser.write("\x10\x14".encode())
                    ser.write(text[x : x+20].encode('cp850','ignore'))
                    sleep(0.2)

                ser.write("\x1F\x11\x14".encode())
                sleep(1)

ser.close()
