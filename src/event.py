#Usage-

#import event
#events = event.EventScraper()
#for post in posts:
#    if events.isEvent(post):
#        calendar.newEvent(events.getEvent(post))
from datetime import datetime
class EventScraper():
    def __init__(self):
        self.date = 0
        self.month = ""
        self.time = 0
        self.title = ""
        self.venue = ""

    def setTitle(self,message):
        s = message
        n=len(s)
        i=0
        while ( i<n and (s[i]==' ' or s[i]=='!' or s[i]=='*' or s[i]=='#' ) ):
            i += 1
        if(i<n):
            while ( i<n and s[i]!='!' and s[i]!='*' and s[i]!='#' and s[i]!='.' ):
                self.title += s[i]
                i += 1

    def setTime(self,message):
        s = message
        n=len(s)
        i = s.find("time")
        while( i != -1 and  s[i+4] != ':'):    #in case "time" word comes in post
            i = s.find("time",i+4)
        if(i == -1 ):                         # " : " after time is mandatory
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


    def setDateAndMonth(self,message):
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
                self.setMonth(date_start,message)

    def setVenue(self,message):
        s = message
        n=len(s)
        v = ""
        i = s.find("venue")
        while( i != -1 and s[i+5] != ':' ):    #in case "venue" word comes in post
            i = s.find("venue",i+5)
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

        message = message.lower()

        if len(self.title)==0:
            self.setTitle(message)
            if(self.title is None):
                return False
      
        self.setDateAndMonth(message)
        if(self.date is None):
            return False

        self.setTime(message)
        if(self.time is None):
            return False

        return True

    def getEvent(self,post):
        details = {}
        if self.isEvent(post) is True:
            self.setVenue(post['message'])
            details['title'] = (self.title)
            details['date'] = (self.date)
            details['month'] = (self.month)
            details['time'] = (self.time)
            details['venue'] = (self.venue)
            return details

# TO CHECK IF WORKING.
events = EventScraper()
post = {}
post['message'] = """**Event Title**
Here goes the worth much as crap description that we'll discard anyway. Important information follows below:
---
Date: 27 Jan 2017
Time: 5:30 PM
Venue: Z103
---"""
print(events.isEvent(post))
det = events.getEvent(post)
print(det)
