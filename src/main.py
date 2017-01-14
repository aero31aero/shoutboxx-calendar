#! /usr/bin/env python3
import post
import database
import cal
import event
from config import config

import os

def run():
	apitoken = config['facebook_token']
	groupid = config['groupid']
	client_secrets='client_secret.json'
	db = database.DatabaseHandler(
		config['mysql']['hostname'],
		config['mysql']['username'],
		config['mysql']['password'],
		config['mysql']['databasename'])
	db.setupDatabase()
	calendar = cal.GoogleCalendar(client_secrets)
	# calendar.newEvent(event)
	evt = event.EventScraper()
	facebook = post.FacebookHandler(apitoken,groupid)
	allposts = facebook.scrape(db.getLatestPostTime())
	print(len(allposts))
	for eachpost in allposts:
		try:
			db.insertPost(eachpost)
			if evt.isEvent(eachpost) == True:
				print(eachpost['from']['name']+"\n\t"+eachpost['message'])
				newevent = evt.getEvent(eachpost)
				db.insertEvent(newevent)


		except KeyError as e:
			# swallow the exception
			print(type(e))
			print(e)
			# pass
	unpublished_events = db.getToBeUploadedPosts()
	print(len(unpublished_events))
	for eachevent in unpublished_events:
		postedevent = calendar.newEvent(evt.getGoogleEvent(eachevent))
		print(postedevent)
		if postedevent['uploaded'] == True:
			db.markAsUploaded(postedevent)
run()
