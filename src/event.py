from datetime import datetime as dt
from datetime import timedelta
class EventScraper():
	def setTitle(self,message,start):
		s = message
		flag=0
		title = None
		for ind,i in enumerate(s.split('\n')):
			if i.startswith('Title:') and ind>start:
				flag=1
				t = i[6:]
				t = t.strip()
				title = t
				break
		if flag==0:
			title = None
		return title

	def setTime(self,message,start):
		s = message
		flag=0
		timev = None
		for ind,i in enumerate(s.split('\n')):
			if i.startswith('Time:') and ind>start:
				flag=1
				t = i[5:]
				t = t.strip()
				timev = dt.strptime(t,"%H%M").time()
				break
		if flag==0:
			timev = None
		return timev

	def setDateTime(self,message,start):
		s = message
		flag = 0
		datet = None
		time = self.setTime(message,start)
		if time is not None:
			for ind,i in enumerate(s.split('\n')):
				if i.startswith('Date:') and ind>start:
					flag=1
					t = i[5:]
					t = t.strip()
					datet = dt.strptime(t+' '+str(time),"%d-%m-%Y %H:%M:%S")
					break
			if flag==0:
				datet= None
		else:
			datet = None
		return datet

	def setVenue(self,message,start):
		s = message
		flag=0
		venue = None
		for ind,i in enumerate(s.split('\n')):
			if i.startswith('Venue:') and ind>start:
				flag=1
				t = i[6:]
				t = t.strip()
				venue = t
				break
		if flag==0:
			venue = None
		return venue

	def isEventHelp(self,post):
		message = post.get('message',None)
		l=[]
		if message is None:
			l.append(False)
			l.append(0)
			return l
		else:
			s=message
			idx=0
			flag=0
			for ind,i in enumerate(s.split('\n')):
				if i == '===':
					idx=ind
					flag=1
					break
			if flag==0:
				l.append(False)
				l.append(0)
				return l
			else:
				venue = self.setVenue(message,idx)
				title = self.setTitle(message,idx)
				datetime = self.setDateTime(message,idx)
				if title is None or venue is None or datetime is None:
					l.append(False)
					l.append(0)
					return l
				else:
					l.append(True)
					l.append(idx)
					return l

	def isEvent(self,post):
		l = self.isEventHelp(post)
		if l[0]==True:
			return True
		else:
			return False

	def getEvent(self,post):
		l = self.isEventHelp(post)
		details = {}
		if(l[0]==True):
			idx=l[1]
			message = post['message']
			datetime = self.setDateTime(message,idx)
			venue = self.setVenue(message,idx)
			title = self.setTitle(message,idx)
			details['title'] = title
			details['datetime'] = datetime
			details['venue'] = venue
			details['id'] = post.get('id',None)
			return details

	def getGoogleEvent(self,array):
		ist_delta = timedelta(hours=5,minutes=30)
		delta = timedelta(hours=1)
		# print("INITTIME:",array[3])
		starttime = array[3] - ist_delta
		# print("NEWTIME:",starttime)
		googleevent = {}
		googleevent['summary'] = array[2]
		googleevent['description'] = "https://facebook.com/"+array[0]
		googleevent['start'] = {}
		googleevent['start']['dateTime'] = starttime.isoformat('T')+"+00:00"
		googleevent['end'] = {}
		endtime = starttime + delta
		googleevent['end']['dateTime'] = endtime.isoformat('T')+"+00:00"
		googleevent['location'] = array[4]
		googleevent['attendees'] = [{'email':'bits-pilani.ac.in_d17s7fo9ou7p93pntr9eghvruo@group.calendar.google.com'}]
		return googleevent



# TO CHECK IF WORKING.
# events = EventScraper()
# post = {}
# post['message'] = """Hey! What is up
# Title: This is the Title
# Date: 26-01-2017
# Time: 1700
# Venue: G205
# ==="""
# print(events.isEvent(post))
# det = events.getEvent(post)
# print(det)
