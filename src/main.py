#! /usr/bin/env python3
import post
import database
import cal
import event

import os

def run():
	apitoken = os.environ['FACEPY_TOKEN']
	groupid = '300189226756572'
	client_secrets='client_secret.json'

	# event = {
 #    'summary': 'Test Event',
 #    'location': 'BITS Pilani, Hyderabad Campus',
 #    'description': 'Insert random stuff here',
 #    'start': {
 #        'dateTime': '2017-01-06T20:15:00+05:30',
 #        'timeZone': 'Asia/Kolkata',
 #    },
 #    'end': {
 #        'dateTime': '2017-01-06T20:30:00+05:30',
 #        'timeZone': 'Asia/Kolkata',
 #    },
 #    'reminders': {
 #        'useDefault': False,
 #        'overrides': [
 #        {'method': 'email', 'minutes': 60},
 #        {'method': 'popup', 'minutes': 60},
 #      ],
 #    },
 #  }

	db = database.DatabaseHandler("localhost","root","root","sbxcal")
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
		calendar.newEvent(evt.getGoogleEvent(eachevent))
run()
