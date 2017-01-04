s= "*****Talk for Chemical and Mechanical students***** A gentle reminder to all the Chemical and mechanical students for the talk on 3D printing of metals by Prof. Upadrasta Ramamurty, CSIR- Shanti Sharp Bhatnagar award recipient and one of the notable researchers in Material Science. Venue: Seminar Hall, G-block . Date: 24 Nov Time: 4pm"
s = s.lower()
add = 1  #add=1 if i need to add this to my calendar
n= len(s)


# main specifications
# title in ** ** or ## ## or !! !!
# colon immediately  afte "date" , "time" and "venue" 
# time_format - 7 pm , 7:50 pm , 9am etc.. NOT 2300 , 23:00 etc.. in short 12hr format 
# need a '.' or new line after venue has ended

############################################################################
#date(number and month)
#time
#venue
#title
#############################################################################
#get date start point 

i = s.find("date")
while( i != -1 and  s[i+4] != ':'):    #in case date word comes in post 
    i = s.find("date",i+4)
if(i == -1 ):                         # " : " after date is mandatory
    add=0
date_start = i

#if(add==1):
#print (i)
#print (add)
##########################################################################

#########################################################################
#get the number first- date_number

if(add==1):
    while ( i<n and (ord( s[i] ) < 48 or ord( s[i] ) > 57 ) ):
        i=i+1
    if(i==n):
        add=0
    else :
        date_number = ord(s[i])-48
        if(ord( s[i+1] ) >= 48 or ord( s[i+1] ) <= 57 ):
            date_number *=10
            date_number += ord(s[i+1])-48

#if(add==1):
#print (date_number)
####################################################################  

######################################################################
#get the month
if(add==1):
    j = s.find("jan",date_start)
    if( j != -1 ) :
        month = 1
    else :
        j = s.find("feb",date_start)
        if( j != -1 ) :
            month = 2
        else :
            j = s.find("mar",date_start)
            if( j != -1 ) :
                month = 3
            else :
                j = s.find("apr",date_start)
                if( j != -1 ) :
                    month = 4
                else :
                    j = s.find("may",date_start)
                    if( j != -1 ) :
                        month = 5
                    else :
                        j = s.find("jun",date_start)
                        if( j != -1 ) :
                            month = 6
                        else :
                            j = s.find("jul",date_start)
                            if( j != -1 ) :
                                month = 7
                            else :
                                j = s.find("aug",date_start)
                                if( j != -1 ) :
                                    month = 8
                                else :
                                    j = s.find("sep",date_start)
                                    if( j != -1 ) :
                                        month = 9
                                    else :
                                        j = s.find("oct",date_start)
                                        if( j != -1 ) :
                                            month = 10
                                        else :
                                            j = s.find("nov",date_start)
                                            if( j != -1 ) :
                                                month = 11
                                            else :
                                                j = s.find("dec",date_start)
                                                if( j != -1 ) :
                                                    month = 12
                                                else :
                                                    add=0
#if(add==1):
#print(month)
##################################################################################################

###################################################################################################
#get the time  start point

i = s.find("time")
while( i != -1 and  s[i+4] != ':'):    #in case "time" word comes in post 
    i = s.find("time",i+4)
if(i == -1 ):                         # " : " after time is mandatory
    add=0
time_start = i

#if(add==1):
#print (i)
#print (add)
############################################################################################

##########################################################################################
#get time- time_hour - time_min - am/pm 
time_min =0
if(add==1):
    while ( i<n and (ord( s[i] ) < 48 or ord( s[i] ) > 57 )):
        i=i+1
    if(i==n):
        add=0
    else :
        time_hour = ord(s[i])-48
        if( s[i+1] == ':' ):
            time_min = (ord(s[i+2])-48)*10 + (ord(s[i+3])-48 )

#get am/pm
pm=0
if(add==1):
    while ( i<n and (ord( s[i] ) < 97 or ord( s[i] ) > 122 )  ):
        i=i+1
    if(i==n):
        add=0
    else :
        if(s[i]=='p'):
            pm=1
        if(s[i] !='p' and s[i] != 'a' ):
            add=0



#if(add==1)
#print("hour " , time_hour)
#print("minute " , time_min)
#print(pm)

###############################################################################################

###############################################################################################
#get venue

venue = ""
i = s.find("venue")
while( i != -1 and s[i+5] != ':' ):    #in case "venue" word comes in post 
    i = s.find("venue",i+5)
if(i == -1 ):                         # " : " after venue is mandatory
    add=0
venue_start = i
i+=5;

if(add==1):
    while ( i<n and s[i]!='!' and s[i]!='*' and s[i]!='#' and s[i]!='.' and s[i]!="\n" ):
        venue+=s[i]
        i=i+1

#if(add==1):
#print("venue" , venue)
    
################################################################################################
#get title

title=""
if(add==1):
    i=0
    while ( i<n and (s[i]==' ' or s[i]=='!' or s[i]=='*' or s[i]=='#' ) ):
        i+=1
    if(i==n):
        add=0
    else :
        while ( i<n and s[i]!='!' and s[i]!='*' and s[i]!='#' and s[i]!='.' ):
            title+=s[i]
            i+=1


##############################################################################################


if(add==1):
    print ("date-" , date_number)
    print("month-" , month)
    print("hour-" , time_hour)
    print("minute- " , time_min)
    print(pm)
    print("venue-" , venue)
    print("title-" , title)       


