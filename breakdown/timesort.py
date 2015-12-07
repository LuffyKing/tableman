
import re

def timesort(timetabledict,timecolumn,dytw,row):#function for getting the dictionary that contains the times,days and courses

    pattern=re.compile(r'(\S+)([AP]M)')#pattern to find the first time in the textblock from the user(the times are gotten in the following format ('11:30','AM'))
    pattern1=re.compile(r'(\d+)')#pattern to get the first two digits in a timeslot(i.e. the 11 from 11:30 AM)

    for i in xrange(1,len(timecolumn)):#iterates over the list of times from 7AM to 12PM
        rowtime={}#a dictionary for specific timeslots in the timecolumn list, it holds all the courses taking place at a timeslot for the week
        for j in dytw:#iterate dytw to get days
            daylist=timetabledict[j]#list of courses taking place on day j
            for k in daylist:#iterate over daylist to get an individual textblock
                try:

                    timeslot=re.search(pattern,k)#gets the time from the textblock
                except:
                    pass
                if timeslot:#if the search is successful this allows the statements below to run

                    if int(timecolumn[i].split()[0])==int(re.search(pattern1,timeslot.groups()[0]).group()) and int(timecolumn[i].split()[1])==int(re.findall(pattern1,timeslot.groups()[0])[1]) and timecolumn[i].split(' ')[2] in timeslot.groups()[1]:
                        #the first statement checks first two digits ,the second is to check the second two digits and the last is to check whether the AM or PM matches
                        rowtime[j]=k#assigns the textblock to the dictionary rowtime with the day of the week as the key and the textblock as the value



        row[timecolumn[i]]=rowtime#this is a dictionary that takes the rowtime dictionary as the value and a timeslot as the key
    return row