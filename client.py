#The following imported libraries are used for both Twitter API, ESPEAK, and Client initialization
#To set up the twitter API I used the recommened tutorial at https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
#The first and third videos of the How to use Twitter API  v1.1 with python to stream tweets were particularly useful
#As for initializig the client I used the example provided in class (TCP Echo Client). Where I passed in the the following informaion 
#from the command line: Server IP, Server Port Number, Socket Size, and Hashtag.
#

import subprocess
import os
from clientKeys import ckey,csecret,asecret,atoken #These variables are defined in a seperate file called keys.py (these are the twitter keys)
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import socket
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# https://gist.github.com/didler/2395703 {
def getopts(argv):
	opts ={}
	while sys.argv:
		if sys.argv[0][0] == '-':
			opts[sys.argv[0]] = sys.argv[1]
		sys.argv = sys.argv[1:]
	return opts

myargs = getopts(sys.argv)
if not myargs:
	print('No arguments found')
	sys.exit()
if '-p' in myargs:
	server_port = int(myargs['-p'])
	myargs.pop('-p', None)
if '-t' in myargs:
	hashtag = myargs['-t']
	myargs.pop('-t', None)
if '-z' in myargs:
	socket_size = int(myargs['-z'])
	myargs.pop('-z', None)
if '-s' in myargs:
	host = myargs['-s']
	myargs.pop('-s', None)
if len(myargs.keys()) != 0:
	print('Invalid arguments')
	sys.exit()
# }


class listener(StreamListener):
	print('Listening for tweets that contain: ',hashtag)
	def on_data(self, data):
		user = data.split('"screen_name":"')[1].split('","')[0]
		tweet = data.split(',"text":"')[1].split('","source')[0]
		print('New Tweet: ',tweet,' | User: ',user)
		tweet = tweet.replace(hashtag,"")
		parsed = tweet.replace(" ", "_")
		#ESPEAK
		cmd_beg = 'espeak -ven+f3 -k5 -s150 '
		with open(os.devnull, 'w') as devnull:
			subprocess.run(cmd_beg + parsed, stdout=devnull, stderr=devnull, shell=True)
		s.connect((host, server_port))
		print('Conncting to server ',host,' on port',server_port)
		s.send(tweet.encode())
		print('Sending question: ',tweet)
		data_ = s.recv(socket_size)
		s.close()
		data_ = str(data_)
		data_ = data_[2:-1]
		print('Received answer:', data_)
	def on_error(self, status):
		print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[hashtag])