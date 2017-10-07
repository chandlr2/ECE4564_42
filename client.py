from keys import ckey,csecret,asecret,atoken
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import socket
import sys


host = sys.argv[1]
#print(host)
port = 5803
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


from keys import ckey,csecret,asecret,atoken
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#consumer key, consumer secret, access token, access secret.



class listener(StreamListener):

	def on_data(self, data):
		hashtag = "#ECE4564T31"
		tweet = data.split(',"text":"')[1].split('","source')[0]
		if hashtag in tweet:
			tweet = tweet.replace(hashtag,"")
			s.connect((host, port))
			s.send(tweet.encode())
			data_ = s.recv(size)
			s.close()
			print('Received:', data_)
			print(tweet)
		return(True)
	def on_error(self, status):
		print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#ECE4564T31"])