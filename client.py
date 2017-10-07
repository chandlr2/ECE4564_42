import subprocess
import os
from keys import ckey,csecret,asecret,atoken
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import socket
import sys
from keys import ckey,csecret,asecret,atoken
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#consumer key, consumer secret, access token, access secret.

# https://gist.github.com/didler/2395703
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
	hashtag = int(myargs['-t'])
	myargs.pop('-b', None)
if '-z' in myargs:
	socket_size = myargs['-z']
	myargs.pop('-z', None)
if '-s' in myargs:
	host = myargs['-s']
	myargs.pop('-z', None)
if len(myargs.keys()) != 0:
	print('Invalid arguments')
	sys.exit()



class listener(StreamListener):
	print('Listening for tweets that contain: ',hashtag)
	def on_data(self, data):
		user = data.split('"screen_name":"')[1].split('","')[0]
		tweet = data.split(',"text":"')[1].split('","source')[0]
		print('New Tweet: ',tweet,' | User: ',user)
		parsed = tweet.replace(" ", "_")
		cmd_beg = 'espeak -ven+f3 -k5 -s150 '
		with open(os.devnull, 'w') as devnull:
			subprocess.run(cmd_beg + parsed, stdout=devnull, stderr=devnull, shell=True)
		if hashtag in tweet:
			tweet = tweet.replace(hashtag,"")
			s.connect((host, server_port))
			print('Conncting to server ',host,' on port',server_port)
			s.send(tweet.encode())
			print('Sending question: ',tweet)
			data_ = s.recv(socket_size)
			s.close()
			print('Received:', data_)
			#print(tweet)
		return(True)
	def on_error(self, status):
		print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[hashtag])