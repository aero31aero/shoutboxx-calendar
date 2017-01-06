from datetime import datetime as dt

<<<<<<< HEAD
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
            return details
=======
#import event
#events = event.EventScraper()
#for post in posts:
#    if events.isEvent(post):
#        calendar.newEvent(events.getEvent(post))
import re
from datetime import datetime,timedelta
class EventScraper():
	def __init__(self):
		self.time = 0
		self.month = ""
		self.date = 0
		self.DateTime = 0
		self.title = ""
		self.venue = ""
		self.year = 0

	def setTitle(self,message):
		s = message
		n=len(s)
		i=0
		t = ""
		while ( i<n and (s[i]==' ' or s[i]=='!' or s[i]=='*' or s[i]=='#' ) ):
			i += 1
		if(i<n):
			while ( i<n and s[i]!='!' and s[i]!='*' and s[i]!='#' and s[i]!='.' ):
				t += s[i]
				i += 1
			self.title = t

	def getYear(self,message):
		s = message
		n = len(s)
		a = re.compile(r'(2[0-9]{3})')
		b = a.search(s)
		if b is None:
			self.year = datetime.today().year
		else:
			self.year = b.group()

	def setTime(self,message):
		s = message
		n=len(s)
		i = s.find("time")
		while( i != -1 and  s[i+4] != ':'):    #in case "time" word comes in post
			i = s.find("time",i+4)
		if i == -1 :                         # " : " after time is mandatory
			self.time = None
		else:
			time_start = i
			time_hour = 0
			time_min = 0
			while ( i<n and (ord( s[i] ) < 48 or ord( s[i] ) > 57 )):
				i=i+1
			if(i==n):
				self.time = None
			else :
				time_hour = ord(s[i])-48
				if( s[i+1] == ':' ):
					time_min = (ord(s[i+2])-48)*10 + (ord(s[i+3])-48 )
				while ( i<n and (ord( s[i] ) < 97 or ord( s[i] ) > 122 )  ):
					i=i+1
				if(i==n):
					self.time= None
				else :
					if(s[i]=='p'):
						time_hour += 12
					if(s[i] !='p' and s[i] != 'a' ):
						self.time = None
					else:
						self.time = str(datetime.strptime(str(time_hour).zfill(2)+':'+str(time_min).zfill(2),'%H:%M').time())

	def setMonth(self,date_start,message):
		new_message = message[date_start:].split(' ')
		#list_month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		list_month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
		month_yn = [i in new_message for i in list_month]
		month = 0
		for i in month_yn:
			if i is True:
				self.month = list_month[i]
				month = i+1
				break
		if month == 0:
			self.month = None
		return month

	def setDateTime(self,message):
		s = message
		n=len(s)
		date_start = 0
		i = s.find("date")
		while( i != -1 and  s[i+4] != ':'):    #in case date word comes in post
			i = s.find("date",i+4)
		if i == -1 :                         # " : " after date is mandatory
			self.date = None
		else:
			date_start = i
			while ( i<n and (ord( s[i] ) < 48 or ord( s[i] ) > 57 ) ):
				i=i+1
			if(i==n):
				self.date = None
			else:
				date_number = ord(s[i])-48
				if(ord( s[i+1] ) >= 48 or ord( s[i+1] ) <= 57 ):
					date_number *= 10
					date_number += ord(s[i+1])-48
				self.date = date_number
				month = self.setMonth(date_start,message)
				time = self.setTime(message)
				if self.time is not None and self.month is not None:
					self.getYear(message)
					self.DateTime = datetime.strptime(str(date_number)+'-'+str(month)+'-'+str(self.year)+'T'+self.time,'%d-%m-%YT%H:%M:%S')
				else:
					self.DateTime = None

	def setVenue(self,message):
		s = message
		n=len(s)
		v = ""
		i = s.find("Venue")
		while( i != -1 and s[i+5] != ':' ):    #in case "venue" word comes in post
			i = s.find("Venue",i+5)
		if(i == -1 ):                         # " : " after venue is mandatory
			self.venue = None
		else:
			i+=5;
			while ( i<n and s[i]!='!' and s[i]!='*' and s[i]!='#' and s[i]!='.' and s[i]!="\n" ):
				v+=s[i]
				i=i+1
			self.venue = v

	def isEvent(self, post):
		message = post.get('message',None)

		if message is None:
			return False

		#message = message.lower()

		self.setTitle(message)
		if(self.title is None):
			return False

		message = message.lower()
		self.setDateTime(message)
		if self.DateTime is None :
			return False
		return True

	def getEvent(self,post):
		details = {}
		if self.isEvent(post) is True:
			self.setVenue(post['message'])
			details['id'] = post['id']
			details['title'] = (self.title)
			details['datetime'] = (self.DateTime)
			#details['month'] = (self.month)
			#details['time'] = (self.time)
			details['venue'] = (self.venue)
		return details
	def getGoogleEvent(self,array):
		delta = timedelta(hours=1)
		googleevent = {}
		googleevent['summary'] = array[2]
		googleevent['description'] = "https://facebook.com/"+array[0]
		googleevent['start'] = {}
		googleevent['start']['dateTime'] = array[3].isoformat('T')+"+00:00"
		googleevent['end'] = {}
		newtime = array[3] + delta
		googleevent['end']['dateTime'] = newtime.isoformat('T')+"+00:00"
		googleevent['location'] = array[4]
		return googleevent



>>>>>>> 6a50b99a8139f5577782804d5f38192d90af6729


# TO CHECK IF WORKING.
<<<<<<< HEAD
events = EventScraper()
post = {}
post['message'] = """Hey! What is up
===
Title: This is the Title
Date: 26-01-2017
Time: 1700
Venue: G205"""
print(events.isEvent(post))
det = events.getEvent(post)
print(det)
=======
# events = EventScraper()
# post = {}
# post['message'] = """**Event Title**
# Here goes the worth much as crap description that we'll discard anyway. Important information follows below:
# ---
# Date: 27 Jan 2017
# Time: 5:30 PM
# Venue: Z103
# ---"""
# print(events.isEvent(post))
# print(events.date)
# print(events.time)
# print(events.DateTime)
# det = events.getEvent(post)
# print(det)
>>>>>>> 6a50b99a8139f5577782804d5f38192d90af6729
