import time as timing
starttime=timing.time()
from icalendar import Calendar,Event,Alarm
from datetime import datetime
import re
import numpy as np
import cv2
from PIL import Image
from PIL import ImageFilter
import pytesseract
from operator import itemgetter
import datetime as dt
from prototypeguis import TextCorrectionGUI
from prototypeguis import UserGUI
#the above are the guis for textcorrection and table adjustments
import random
import enchant
import os



if not os.path.exists((os.path.expanduser("~/Desktop/blaze"))):
    os.mkdir(os.path.expanduser("~/Desktop/blaze"))


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
					alarm['duration']=10
					alarm['action']='Display'
					alarm['Description']='Time for %s %s'%(nlsplit[0],nlsplit[1])#Time for SWFR 3MX3 Lecture
					event.add_component(alarm)#adds the alarm to the event
					if 'AM' not in nlsplit[len(nlsplit)-1] and 'PM' not in nlsplit[len(nlsplit)-1] and ':'  not in nlsplit[len(nlsplit)-1]:#adds the location which should be the last sentence, if it is not the last sentence it is not added
						event.add('location',nlsplit[len(nlsplit)-1])
				
					event['duration']='PT%dH%dM'%(int(dur.total_seconds()//3600),int((dur.total_seconds()//60)%60))#calculates the duration from the dur variable which is a timedelta object, using total seconds between the start and end times for a textblock and simple math the hours and minuts are derived

					cal.add_component(event)

	file=open(os.path.expanduser("~/Desktop/cal.ics"),'w+')#creates the ics file
	file.write(cal.to_ical())
	file.close()
  
def timesort(cleanneddict,timecolumn,dytw,row):#function for getting the dictionary that contains the times,days and courses
    
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
                        
                

        row[timecolumn[i]]=rowtime#this is a dictionary that takes the rowtime dictionary as the value and atimeslot as the key
    return row
  
def ccchecker(dictionary):
    try:
        #the goal is to make sure all the course codes are correct
        pattern=re.compile(r'\d\w+')#pattern to get the the course codes
        pwl=enchant.request_pwl_dict("/Users/damola/Desktop/  ")#coursecodes spellcheck
        for i in dictionary:#iterates over the dictionary
            count=0
            for j in dictionary[i]:#iterates over the dictionary values for the key i
                
                
                if re.search(pattern,j):#checks if the search is valid then allows the code below to run
                    pin=re.search(pattern,j)#assigns the variable pin to the coursecode
                    if len(pin.group())>=4:#checks if it has the appropriate amount of characters
                        dictionary[i][count]=j.replace(j[pin.span()[0]:pin.span()[1]],pwl.suggest(pin.group())[0])#replaces the coursecode with a corrected version
                count=count+1
        return dictionary
    except:
        print 'CCCHECKER did not work'
        return dictionary
def timecheck(dictionary):#this checks the times
    try:
        pattern=re.compile(r'(\S+)([AP]M)')#pattern to find the first time in the textblock from the user(the times are gotten in the following format ('11:30','AM')) 
        pattern1=re.compile(r'(\w+):(\w+)')#pattern to group the time codes from the textblock into  for example (11,30) 
        pwl=enchant.request_pwl_dict(os.path.expanduser("~/Desktop/timecodes.txt"))#loads the timecode spellcheck
        for i in dictionary:#iterates over the dictionary
            count=0
            for j in dictionary[i]:#iterates over the dictionary values for the key i
                    if re.search(pattern,j):#checks if the search is valid then allows the code below to run
                            length=re.findall(pattern,j)#finds all the times in the textblock 
                            if len(length)==1:#if the AM or PM are not spelt correctly this corrects it
                                AMPM=length[0][1]
                                
                                listoftimes=re.findall(pattern1,j)
                                listoftimes1=listoftimes[0][1]
                                listoftimes2=listoftimes[1][1]
                                time1=pwl.suggest(listoftimes1)
                                time2=pwl.suggest(listoftimes2)
                                if len(time1)==2:
                                    for k in time1:
                                        if AMPM in k:
                                            index=time1.index(k)
                                    pin=re.search(pattern1,j)
                                    dictionary[i][count]=j.replace(j[pin.span()[0]:pin.span()[1]],'%s:%s'%(re.search(pattern1,j).groups()[0],pwl.suggest(re.search(pattern1,j).groups()[1])[index]))
                                          
                                elif len(time2)==2:
                                    for k in time1:
                                        if AMPM in k:
                                            index=time1.index(k)
                                    pin=re.search(pattern1,j)
                                    dictionary[i][count]=j.replace(j[pin.span()[0]:pin.span()[1]],'%s:%s'%(re.findall(pattern,j)[1][0],pwl.suggest(re.findall(pattern,j)[1][1])[index]))




                    count=count+1
        return dictionary
    except:
        print 'timecheck did not work'
        return dictionary
                                
                            
                            
                            
                            
                            
    
    
def listofemptycells(datalist):#function to get the list of empty cells for weekdays
    
    day={}
    for i in xrange(1,len(datalist[0])):
        
        daylist=[]
        for j in xrange(1,len(datalist)):
            try:
            
                if datalist[j][i]=='' and datalist[j+1][i]=='':#50min time space
                    daylist.append(data[j][0])
            except:
                pass
        day[datalist[0][i]]=daylist
    return day
def listofemptycells2(datalist):#function to get the list of empty cells for weekends
    
    day={}
    for i in xrange(len(datalist[0])-2,len(datalist[0])):
        
        daylist=[]
        for j in xrange(1,len(datalist)):
            try:
            
                if datalist[j][i]=='' and datalist[j+4][i]=='':#two hour time soace
                    if dt.datetime.strptime('09 00 AM', "%I %M %p").strftime("%H %M")<dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M") and dt.datetime.strptime('06 30 PM', "%I %M %p").strftime("%H %M")>dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M"):
                        daylist.append(datalist[j][0])
            except:
                pass
        day[datalist[0][i]]=daylist
    return day                
                
                
def lecturereview(datalist):#places lecture reviews after every lecture
    pattern=re.compile(r'\w+')
    for i in xrange(1,len(datalist[0])):


        for j in xrange(1,len(datalist)):
            if 'Lecture' in datalist[j][i] and 'Review' not in datalist[j][i]:
                spacelist=listofemptycells(datalist)[datalist[0][i]]
                for k in spacelist:
                    if dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M")<dt.datetime.strptime(k, "%I %M %p").strftime("%H %M"):
			

                        wordsoftextblock=re.findall(pattern,datalist[j][i])
                        etime=timecolumn[timecolumn.index(k)+1]
                        endtime=etime.split(' ')
                        endtime[1]='20'
                        etime=' '.join(endtime)
                        
                        text='%s %s\n%s\n%s - %s'%(wordsoftextblock[0],wordsoftextblock[1],'Lecture Review',k,etime)
                        datalist[timecolumn.index(k)][i]=text
                        datalist[timecolumn.index(k)+1][i]='place'


                        break
    return datalist

def weeekendstudy(datalist):#creates a weekend study plan
    
    pattern=re.compile(r'\w+')
    pattern2=re.compile(r'.+\d\w+')
    listtext=[]
    point=[]
    for i in xrange(1,len(datalist[0])):
        


        for j in xrange(1,len(datalist)):
            
            if 'Lecture' in datalist[j][i] and 'Review' not in datalist[j][i]:
                
                text=re.findall(pattern2,data[j][i])[0]
                try:
                    
                    listtext.index(text)

                except:
                    listtext.append(text)
    while len(listtext)>0:
        
        point.append(listtext.pop(random.randint(0,len(listtext)-1)))
        
    
    for text in point:
        
        spacelistweekend=listofemptycells2(datalist)
        
        days=spacelistweekend.keys()
        days.sort()
        if spacelistweekend[days[0]]!=[]:
            k=days[0]
            for l in spacelistweekend[k]:
                
                
                timeend=dt.datetime.strptime(datalist[timecolumn.index(l)][0], "%I %M %p")+dt.timedelta(hours=2)
                timeend=timeend.strftime("%I %M %p")   
                text3='%s\n%s - %s'%(text, datalist[timecolumn.index(l)][0],timeend)
                
                datalist[timecolumn.index(l)][datalist[0].index(k)]=text3
                datalist[timecolumn.index(l)+1][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+2][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+3][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+4][datalist[0].index(k)]='place'
                break
        elif spacelistweekend[days[1]]!=[]:
            k=days[1]
            for l in spacelistweekend[k]:
                
                
                timeend=dt.datetime.strptime(datalist[timecolumn.index(l)][0], "%I %M %p")+dt.timedelta(hours=2)
                timeend=timeend.strftime("%I %M %p")   
                text3='%s\n%s - %s'%(text, datalist[timecolumn.index(l)][0],timeend)
                
                
                
                                             
                datalist[timecolumn.index(l)][datalist[0].index(k)]=text3
                datalist[timecolumn.index(l)+1][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+2][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+3][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+4][datalist[0].index(k)]='place'
                break
    return datalist
            
            
            
            
    
   
def labreview(datalist):#puts a labreview before every lab
    pattern=re.compile(r'\w+')
    for i in xrange(1,len(datalist[0])):
        
        
        for j in xrange(1,len(datalist)):
            if 'Lab' in datalist[j][i] and 'Review' not in datalist[j][i]:
                listoftimes=[]
                
                spacelist=listofemptycells(datalist)[datalist[0][i]]
                for k in spacelist:
                    
                    if dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M")>dt.datetime.strptime(k, "%I %M %p").strftime("%H %M"):
                        listoftimes.append(k)

                
                try:
                    time=listoftimes[len(listoftimes)-1]
                        
                        
                    wordsoftextblock=re.findall(pattern,datalist[j][i])
                    etime=timecolumn[timecolumn.index(time)+1]
                    endtime=etime.split(' ')
                    endtime[1]='20'
                    etime=' '.join(endtime)
                    text='%s %s\n%s\n%s - %s'%(wordsoftextblock[0],wordsoftextblock[1],'Lab Review',time,etime)
                    datalist[timecolumn.index(time)][i]=text
                    datalist[timecolumn.index(time)+1][i]='place'
                except:
                    pass
    return datalist
    
                
        


def sobel(image):#gets a list of horizontal slices
    
    pictures=[]
    sobelx8u = cv2.Sobel(image,cv2.CV_8U,0,1,ksize=-1)
    edges = cv2.Canny(sobelx8u,0,250,apertureSize = 3)
    lines = cv2.HoughLinesP(edges,1,np.pi/2,150, minLineLength = image.shape[1]-50, maxLineGap = 10)
    yont=[]
    line=[]
    width=[]
    try:
        for x1,y1,x2,y2 in lines[0]:
            
            

            width.append(x2)
            yont.append([x1,y1,x2,y2])
            

        yont=sorted(yont,key=itemgetter(1))
        for i in yont:

            

            try:
            
                if yont[yont.index(i)+1][1]-i[1]<10:
                    
                    del yont[yont.index(i)+1]

                            
            except:
                
                pass
        if yont[0][1]>10 :
                line.append(0)
        for i in yont:
            line.append(i[1])
            
            
        for i in line:
            try:
            
                pictures.append(image[i:line[line.index(i)+1],0:max(width)])
            except:
                pass
                                    


                
        return pictures
    except:
        pass
            


def c2I(ideal):#converts from cv2 to Image
    ideal= cv2.cvtColor(ideal,cv2.COLOR_GRAY2RGB)
                    
    ideal = Image.fromarray(ideal)
    return ideal
def I2c(ideal):#converts from Image to cv2
    ideal=np.array(ideal)
    
    ideal= cv2.cvtColor(ideal,cv2.COLOR_RGB2GRAY)
    return ideal



#slices up the image vertically
def vertslice(clrim,edges):


    lines = cv2.HoughLinesP(edges,1,np.pi,150, minLineLength = 100, maxLineGap = 10)#uses probabilistic hough transforms to get horizontal and vertical lines in an image, output is the coordinates of those lines
    y=[]
    for x1,y1,x2,y2 in lines[0]:#iterates the line list to get the vertical coordinates so the length of the photo can be determined
        y.append(y1)
        y.append(y2)
    bottom=max(y)#gets the vertical length of the photo
    lister=[]
    for i in lines[0]:#iterates the line list to get the coordinates,this is done so that a list with the first lines as the first elements can be produced through sorting
        lister.append((i[0],i[1],i[2],i[3]))
    lister.sort()
    ind1=0
    for i in lister:#removes the noisy vertical lines
        ind=-1
        for j in lister:

            ind=ind+1
            if type(j)!=str and type(i)!=str:
                if ind!=ind1 and ind>ind1 and j[0]-i[0]<100:#makes sure the lines being removed are not pivotal lines
                    lister[ind]='destroy'
        ind1=ind1+1


    try:
        while lister.index('destroy'):
            lister.remove('destroy')
    except:
        pass
    ind=0
    listofslices=[]
    #end goal of above code ||S|WFR |ENG|--> |SWFR ENG|
    for i in lister:#this cuts up the image using the vertical coordinates of each pivotal line from the lister list which has been cleaned of noisy lines
        ind=ind+1
        try:
            name='/Users/damola/Desktop/blaze/point%s.tiff'%(ind)
            roi=clrim[0:bottom,i[0]:lister[lister.index(i)+1][0]]
            cv2.imwrite(name,roi)
            listofslices.append(name)

        except IndexError:
            pass
    return listofslices
"""
Vertical slicer can be improved by using sobel to blur out horizontal lines before putting it into the canny edge detector
"""
#########
#Sizer to be added
clrim=cv2.imread('/Users/damola/Desktop/abe.png')#######input file here


im = cv2.cvtColor(clrim,cv2.COLOR_RGB2GRAY)#converts from RGB to GRAY so that edges can be detected by cv2
edges = cv2.Canny(im,0,250,apertureSize = 3)#uses canny edge detection to getting all the edges in the photo

listofslices=vertslice(clrim,edges)
dayweek=['Mond','Tues','Wedn','Thur','Frid','Satu']#list of days
timetabledict={}#dictionary for timetable
#takes the slices and put the text in the dictionary sec
for slicedpic in listofslices:
    
    text=pytesseract.image_to_string(Image.open(slicedpic))#gets the text out of an image
    
    text=text.decode('utf-8').encode(errors='replace').replace('?',' ')#replaces any funny characters
   
    inde=0
    for day in dayweek:#iterates for each day
        inde=inde+1

        if day in text:#checks for the day in the text from the picture
            index=0

            headers=[]#headers for the timetables
            textblks=[]#textblocks the four line
            picture = cv2.imread(slicedpic,0)#reads the image from the folder blaze,sliced pic is the address of the vertical slice

            
            images=sobel(picture)#gets the horizontal slices
                
                
            
        
            if type(images)==list:
                for ideal in images:#iterates for each horizontal slice
                    index=index+1
                    ideal=c2I(ideal)#turns it from cv2 to Image picture file
                    ideal=ideal.filter(ImageFilter.SHARPEN)#this only works with an image file hence the conversion
                    ideal=I2c(ideal)#turns it back so that cv2 operations can continue
                    
                    
                    p,ideal = cv2.threshold(ideal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#turns it black and white using an optimal threshold value determined automatically
                    
                    
                    ideal=c2I(ideal)#turns it from cv2 to Image picture file
                    text=pytesseract.image_to_string(ideal)#this only works with an image file hence the conversion
                    text=text.decode('utf-8').encode(errors='replace').replace('?',' ')
                    textblks.append(text)#creates a list of textblocks for the day in question
                timetabledict[day]=textblks#assigns the list of textblocks to the day in the dictionary as the value for the key day
                
for i in timetabledict:#removes spaces from the dictionary
    count=0
    for j in timetabledict[i]:
        
        if j.isspace() or j=='':
            timetabledict[i][count]='destroy'
        count=count+1
            
    try:
        while 'destroy' in timetabledict[i]:
            
            del timetabledict[i][timetabledict[i].index('destroy')]
        
    except:
        pass
            
		
          

gui=TextCorrectionGUI(timetabledict)
timetabledict=gui.sec11()    
timetabledict['Sunday']=[]
try:
    timetabledict['Saturday']
except:
    timetabledict['Saturday']=[]
timetable=[]
timecolumn=['Time']
for i in xrange(7,24):#creates a time column full of time slots such as 7 00 AM, 7 30 AM
	timecolumn.append(dt.time(i).strftime('%I %M %p'))# creates a timeslot 7 00 AM
	timecolumn.append(dt.time(i,30).strftime('%I %M %p'))# creates a timeslot 7 30 AM
	if i==23:
		timecolumn.append(dt.time(0).strftime('%I %M %p'))#timeslot 12 00 AM
dytw=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']#List of the days of the week

data= [[timecolumn[0], dytw[0], dytw[1], dytw[2], dytw[3],dytw[4],dytw[5],dytw[6]]]#creates the first element of the data of the which is a list of the string 'Time' and days of the week
row={}                
rowfinal=[]
row=timesort(timetabledict,timecolumn,dytw,row)#this is a dictionary that has holds all the time slots for the week and has them as keys.
"""
the row dictionary is a dictionary that holds all the time slots, each time slot within row is a dictionary that has the every day of the week as a key.
So the time slots e.g. 7 00 AM are keys which in themselves are dictionaries that hold the days of the weeks as keys to the content.



"""

for i in xrange(1,len(timecolumn)):#the for loop creates the data list which will hold the timetable values
    rowfinal=[timecolumn[i]]# creates the first element of the list rowfinal which is a time slot e.g. 7 00 AM
    for j in dytw:#iterates over the days of the week to get all the content from row occurring at the first element of rowfinal

        try:
            


            appending=row[timecolumn[i]][j]#accesses the  row dictionary to get the content using the keys time slot and days of the week

            



            rowfinal.append(appending)
        except:
            rowfinal.append('')#if nothing is found for that time slot make it empty

    data.append(rowfinal)#the data list appends the contents of rowfinal which is a list.

#next stage placeholders are introduced
pattern=re.compile(r'(\d+):\d+([AP]M)')#pattern for the first digit and am or pm of the second time in eg 4:30am - 5:30am it gets 5 and am

for i in xrange(1,len(data)):#this for loop creates the placeholders that serve as the pointers for spanning
    for j in xrange(1,len(data[i])):
        """
        the list data has list within it making it a list of lists hence why it is necessary to you two for loops to access the content.
        We avoid the the days of the week and time slots by starting the loops at 1 for both loops.
        """
        if ''!=data[i][j] and 'place'!=data[i][j]:#check if its is empty or is just a pointer for spanning



            firstdigit=re.findall(pattern,data[i][j])[1][0]#firstdigit
            amorpm=re.findall(pattern,data[i][j])[1][1]#am or pm


            for k in xrange(1,len(data)):#len(data) gives the length of the list of lists

                if amorpm in data[k][0] and int(firstdigit)==int(data[k][0].split()[0]) and '00' in data[k][0]:#data[k][0] is in reference to the time column containing the times 7 00 AM
                    """
                    The first condition checks if it is am or pm ,the second condition checks if the first digit of the end time matches the time slot   and then the third condition checks if the time ends in 00.
                    This is all done to check at what time do labs, lectures and tutorials end and set spanners to the end times.
                    Since the classes at mcmaster end at for example 2:20, I cant set the span point to 2:30 because of the possibility of another class starting at that time.
                    But I can set it to 2:00 because the time column is spaced by 30 min intervals so 2:00 will be free and conflict free.This simplicity aids
                    in making spanning less confusing and avoid funny overwrites that may occur.

                    """

                    if data[k][j]=='':#this checks if the time slot that has passed the conditions above is empty and available to be spanned to

                        vdist=k-i# calculates the index difference between the span point on the content
                        count=0

                        for m in xrange(vdist):#this calculates the number of empty rows to be filled and fills them with the word place.
                            count=count+1
                            data[i+count][j]='place'

data=labreview(data)
data=lecturereview(data)
data=weeekendstudy(data)
user=UserGUI(data)
icsfilemaker(user.data)
endtime=timing.time()
print '%f s to run program'%(endtime-starttime)

