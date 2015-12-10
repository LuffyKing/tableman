from icalendar import Calendar,Event,Alarm
from datetime import datetime
import re
import datetime as dt
import os
def icsfilemaker(data):
	cal=Calendar()
	cal.add('version','2.0')
	cal.add('prodid','-//cal test//studybuddy.com//')
	daterule=dt.datetime.now()#this is needed just to initialize the vevent
	pattern=re.compile(r'(\S+)([AP]M)')#pattern to find the first time in the textblock from the user(the times are gotten in the following format ('11:30','AM'))
	pattern1=re.compile(r'(\d+)')#pattern to get the first two digits in a timeslot(i.e. the 11 from 11:30 )
	daysrc=['MO','TU','WE','TH','FR','SA','SU']#lists of days for BYDAY
	pattern2=re.compile(r'(\S+)\s+(\S+)\s+([AP]M)')#pattern to get the time in the following format 11 00 AM
	for i in xrange(1,len(data)):#iterating over the data list
		for j in xrange(1,len(data[0])):
			if data[i][j]!='' and not(data[i][j].isspace()) and  data[i][j]!='place':#only interact with textblocks i.e.non-empty elements of the list

				if re.findall(pattern,data[i][j]):#if search is successful assign the timeslot


					timeslot=re.findall(pattern,data[i][j])#gets the time from the textblock

				elif re.findall(pattern2,data[i][j]):#if search is successful assign the timeslot and reformat each element of the timeslot list to (11:30,AM) just as above
					timeslot=re.findall(pattern2,data[i][j])
					count=0
					for a in timeslot:
						timeslot[count]=('%d:%s'%(int(a[0]),a[1]),a[2])
						count=count+1




				if len(timeslot)==2:#if it has the start and end times proceed forward

					minutes=int(re.findall(pattern1,timeslot[0][0])[1])#get the min 30 from 11:30
					nlsplit=data[i][j].split('\n')#split the text at \n since x\nx\nx\nx for each textblock


					dur=dt.datetime.strptime('%s%s'%(timeslot[1][0],timeslot[1][1]), "%I:%M%p")-dt.datetime.strptime('%s%s'%(timeslot[0][0],timeslot[0][1]), "%I:%M%p")#get the duration of each event in 24 hours time
					hour=dt.datetime.strptime('%s%s'%(timeslot[0][0],timeslot[0][1]), "%I:%M%p").hour# get the hour of the start time in 24 hours eg 11 from 11:30
					event=Event()#creating an event instance
					alarm=Alarm()#creating an alarm instance
					event.add('dtstart',daterule)#adding the start date
					event.add('exdate',daterule)#excluding the start date
					event.add('rrule',{'FREQ':'WEEKLY','BYDAY':daysrc[j-1],'BYHOUR':hour,'BYMINUTE':minutes,'BYSECOND':0,'UNTIL':datetime(2015,12,30,23,59,59)})#generate weekly events for each text block until 30 of December
					event.add('summary','%s\r\n%s'%(nlsplit[0],nlsplit[1]))#adds a title for each text block
					alarm['trigger']='-PT30M'#triggers 30 mins before 3 times at 10 min intervals and displays the message in the description
					alarm['repeat']=3
					alarm['duration']='PT10M'
					alarm['action']='DISPLAY'
					alarm['Description']='Time for %s %s'%(nlsplit[0],nlsplit[1])#Time for SWFR 3MX3 Lecture
					event.add_component(alarm)#adds the alarm to the event
					if 'AM' not in nlsplit[len(nlsplit)-1] and 'PM' not in nlsplit[len(nlsplit)-1] and ':'  not in nlsplit[len(nlsplit)-1]:#adds the location which should be the last sentence, if it is not the last sentence it is not added
						event.add('location',nlsplit[len(nlsplit)-1])

					event['duration']='PT%dH%dM'%(int(dur.total_seconds()//3600),int((dur.total_seconds()//60)%60))#calculates the duration from the dur variable which is a timedelta object, using total seconds between the start and end times for a textblock and simple math the hours and minuts are derived

					cal.add_component(event)

	file=open(os.path.expanduser("~/Desktop/cal.ics"),'w+')#creates the ics file
	file.write(cal.to_ical())
	file.close()