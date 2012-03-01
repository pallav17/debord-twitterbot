import ConfigParser
import time
import cPickle as pickle
from random import choice

# http://code.google.com/p/python-twitter/
import twitter

class Bot:
	def __init__(self):
		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open('config.txt'))
		
		self.watching_tags = self.config.get('general', 'watch_tags').split(',')
		self.ignore_users = self.config.get('general', 'ignore_users').split(',')
		self.replies = open(self.config.get('general', 'reply_strings')).readlines()
		
		self.api = twitter.Api(consumer_key=self.config.get('general','consumer_key'),
				  consumer_secret=self.config.get('general','consumer_secret'),
				  access_token_key=self.config.get('general', 'access_token_key'),
				  access_token_secret=self.config.get('general', 'access_token_secret')
				  )
		
		self.data = self.open_savefile()
		
	def open_savefile(self):
		try:
			return pickle.load(config.get('general', 'savefile'))
		except:
			data = {'last_id': None, 'ids_replied_to': []}
			derp = open(self.config.get('general', 'savefile'), 'w')
			pickle.dump(data, derp)
			derp.close()
			return data
		
	def save_data():
		derp = open(self.config.get('general', 'savefile'), 'w')
		pickle.dump(self.data, derp)
		derp.close()
	
	def send_reply(self, tag, user, id):
		if id not in data['ids_replied_to']:
			reply = "@%s %s %s" % (u.screen_name, choice(self.replies), tag)
			new_status = self.api.PostUpdate(reply, in_reply_to_status_id=id)
			if new_status:
				self.data['ids_replied_to'] = self.data['ids_replied_to'].append(id)
				self.data['last_id'] = new_status.id
				
	def run(self):
		for tag in self.watching_tags:
			if self.data['last_id'] is not None:
				statuses = self.api.GetSearch(term=tag, since_id=self.data['last_id'])
			else:
				statuses = self.api.GetSearch(term=tag)
			
			for status in statuses:
				user = status.user
				id = status.id
				
				if user.screen_name not in self.ignore_users:
					self.send_reply(tag, user, id)
					
if __name__ == '__main__':
	bot = Bot()
	bot.run()