import time as timing
starttime=timing.time()
from icalendar import Calendar,Event,Alarm
from datetime import datetime
from icalendar import LocalTimezone
import re
import datetime as dt
from random import randint
import numpy as np
import cv2
from PIL import Image
from PIL import ImageFilter
import pytesseract
from operator import itemgetter
from PIL import ImageEnhance
import sys
import datetime as dt
#
from test1 import TextCorrectionGUI
from test1 import UserGUI
#the above are the guis for textcorrection and table adjustments
import random
import enchant
import os



if not os.path.exists((os.path.expanduser("~/Desktop/blaze"))):
    os.makdirs(os.path.expanduser("~/Desktop/blaze"))


def icsfilemaker(data):
	cal=Calendar()
	cal.add('version','2.0')
	cal.add('prodid','-//cal test//studybuddy.com//')
	daterule=dt.datetime.now()
	pattern=re.compile(r'(\S+)([AP]M)')#pattern to find the first time in the textblock from the user(the times are gotten in the following format ('11:30','AM'))
	pattern1=re.compile(r'(\d+)')#pattern to get the first two digits in a timeslot(i.e. the 11 from 11:30 )
	daysrc=['MO','TU','WE','TH','FR','SA','SU']
	pattern2=re.compile(r'(\S+)\s+(\S+)\s+([AP]M)')
	for i in xrange(1,len(data)):
		for j in xrange(1,len(data[0])):
			if data[i][j]!='' and not(data[i][j].isspace()) and  data[i][j]!='place':
			
				if re.findall(pattern,data[i][j]):
			

					timeslot=re.findall(pattern,data[i][j])#gets the time from the textblock
				
				elif re.findall(pattern2,data[i][j]):
					timeslot=re.findall(pattern2,data[i][j])
					count=0
					for a in timeslot:
						timeslot[count]=('%d:%s'%(int(a[0]),a[1]),a[2])
						count=count+1
			

			
			
				if len(timeslot)==2:
					#hour=int(re.search(pattern1,timeslot[0][0]).group())
					minutes=int(re.findall(pattern1,timeslot[0][0])[1])
					nlsplit=data[i][j].split('\n')
					
				
					dur=dt.datetime.strptime('%s%s'%(timeslot[1][0],timeslot[1][1]), "%I:%M%p")-dt.datetime.strptime('%s%s'%(timeslot[0][0],timeslot[0][1]), "%I:%M%p")
					hour=dt.datetime.strptime('%s%s'%(timeslot[0][0],timeslot[0][1]), "%I:%M%p").hour
					event=Event()
					alarm=Alarm()
					event.add('dtstart',daterule)
					event.add('exdate',daterule)
					event.add('rrule',{'FREQ':'WEEKLY','BYDAY':daysrc[j-1],'BYHOUR':hour,'BYMINUTE':minutes,'BYSECOND':0,'UNTIL':datetime(2015,12,30,23,59,59)})
					event.add('summary','%s\r\n%s'%(nlsplit[0],nlsplit[1]))
					alarm['trigger']='-PT30M'
					alarm['repeat']=3
					alarm['duration']=10
					alarm['action']='Display'
					alarm['Description']='Time for %s %s'%(nlsplit[0],nlsplit[1])
					event.add_component(alarm)
					if 'AM' not in nlsplit[len(nlsplit)-1] and 'PM' not in nlsplit[len(nlsplit)-1] and ':'  not in nlsplit[len(nlsplit)-1]:
						event.add('location',nlsplit[len(nlsplit)-1])
				
					event['duration']='PT%dH%dM'%(int(dur.total_seconds()//3600),int((dur.total_seconds()//60)%60))

					cal.add_component(event)

	file=open('/Users/damola/Desktop/cal.ics','w+')
	file.write(cal.to_ical())
	file.close()
  
def timesort(cleanneddict,timecolumn,dytw,row):#function for getting the dictionary that contains the times,days and courses
    
    pattern=re.compile(r'(\S+)([AP]M)')#pattern to find the first time in the textblock from the user(the times are gotten in the following format ('11:30','AM'))
    pattern1=re.compile(r'(\d+)')#pattern to get the first two digits in a timeslot(i.e. the 11 from 11:30 AM)
    
    for i in xrange(1,len(timecolumn)):#iterates over the list of times from 7AM to 12PM
        rowtime={}#a dictionary for specific timeslots in the timecolumn list, it holds all the courses taking place at a timeslot for the week
        for j in dytw:#iterate dytw to get days
            daylist=cleaneddict[j]#list of courses taking place on day j
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
"""
def ccspacecheck(dictionary):
    if
"""
    
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

#Sizer has to be added       
clrim=cv2.imread('/Users/damola/Desktop/abe.png')#######input file here

#clrim=cv2.equalizeHist(clrim)
im = cv2.cvtColor(clrim,cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(im,0,250,apertureSize = 3)


#slices up the image vertically
indx=0
lines = cv2.HoughLinesP(edges,1,np.pi,150, minLineLength = 100, maxLineGap = 10)
y=[]
for x1,y1,x2,y2 in lines[0]:
    y.append(y1)
    y.append(y2)
bottom=max(y)
lister=[]
for i in lines[0]:
    lister.append((i[0],i[1],i[2],i[3]))
lister.sort()
ind1=0
for i in lister:
    ind=-1
    for j in lister:
            
        ind=ind+1
        if type(j)!=str and type(i)!=str:
            if ind!=ind1 and ind>ind1 and j[0]-i[0]<100:
                lister[ind]='destroy'
    ind1=ind1+1


try:
    while lister.index('destroy'):
        lister.remove('destroy')
except:
    pass
ind=0
listofslices=[]   
for i in lister:
    ind=ind+1
    try:
        name='/Users/damola/Desktop/blaze/point%s.tiff'%(ind)
        roi=clrim[0:bottom,i[0]:lister[lister.index(i)+1][0]]
        cv2.imwrite(name,roi)
        listofslices.append(name)

    except IndexError:
        pass
##########

dayweek=['Mond','Tues','Wedn','Thur','Frid','Satu']
sec={}
#takes the slices and put the text in the dictionary sec
for slicedpic in listofslices:
    
    text=pytesseract.image_to_string(Image.open(slicedpic))
    
    text=text.decode('utf-8').encode(errors='replace').replace('?',' ')
   
    inde=0
    for day in dayweek:
        inde=inde+1

        if day in text:
            index=0

            headers=[]
            textblks=[]
            picture = cv2.imread(slicedpic,0)
            
            #ideal=cv2.fastNlMeansDenoising(ideal)
            try:
                images=sobel(picture)
                
                
            except:
                pass
        
            try:
                for ideal in images:
                    index=index+1
                    ideal=c2I(ideal)
                    ideal=ideal.filter(ImageFilter.SHARPEN)
                    ideal=I2c(ideal)
                    
                    
                    p,ideal = cv2.threshold(ideal,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                    
                    
                    ideal=c2I(ideal)
                    text=pytesseract.image_to_string(ideal)
                    text=text.decode('utf-8').encode(errors='replace').replace('?',' ')
                    textblks.append(text)
                sec[day]=textblks
                
            except:
                pass
 




for i in sec:
    count=0
    for j in sec[i]:
        
        if j.isspace() or j=='':
            sec[i][count]='destroy'
        count=count+1
            
    try:
        while 'destroy' in sec[i]:
            
            del sec[i][sec[i].index('destroy')]
        
    except:
        pass
            
		
          
"""       
sec=ccchecker(sec)
sec=timecheck(sec)
"""

gui=TextCorrectionGUI(sec)
sec=gui.sec11()    



seckeys=sec.keys()

cleaneddict=sec

cleaneddict['Sunday']=[]
try:
    cleaneddict['Saturday']
except:
    cleaneddict['Saturday']=[]
timetable=[]
timecolumn=['Time']
for i in xrange(7,24):#creates a time column full of time slots such as 7:00 and 7:30
	timecolumn.append(dt.time(i).strftime('%I %M %p'))
	timecolumn.append(dt.time(i,30).strftime('%I %M %p'))
	if i==23:
		timecolumn.append(dt.time(0).strftime('%I %M %p'))
dytw=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']#List of the days of the week

data= [[timecolumn[0], dytw[0], dytw[1], dytw[2], dytw[3],dytw[4],dytw[5],dytw[6]]]



row={}
               
                
                
rowfinal=[]
row=timesort(cleaneddict,timecolumn,dytw,row)
for i in xrange(1,len(timecolumn)):#the for loop creates the data list
    rowfinal=[timecolumn[i]]
    for j in dytw:

        try:
            


            appending=row[timecolumn[i]][j]

            



            rowfinal.append(appending)
        except:
            rowfinal.append('')

    data.append(rowfinal)

#next stage placeholders are introduced
pattern=re.compile(r"[\w']+")
for i in xrange(1,len(data)):#this for loop creates the placeholders that serve as the pointers for spanning
    
     
     
    for j in xrange(1,len(data[i])):
        if ''!=data[i][j] and 'place'!=data[i][j]:
            index=[]
            splitted=data[i][j].split('\n')
            for l in splitted:
                if 'AM' in l or 'PM' in l:
                    index.append(splitted.index(l))
            hunt=max(index)
            
            
            time=re.findall(pattern,splitted[hunt])
            indices = [o for o, x in enumerate(time) if 'AM' in x or 'PM' in x  ]
            a=time[indices[1]-1]
            b=time[indices[1]]

            for k in xrange(1,len(data)):


                if len(b.split('00'))==2:
                    used=b.split('00')
                elif len(b.split('20'))==2:
                    used=b.split('20')
              


                if used[1] in data[k][0] and int(a)==int(data[k][0].split()[0]) and '00' in data[k][0]:



                    if data[k][j]=='':

                        hdist=k-i
                        count=0
                        
                        for m in xrange(hdist):
                            count=count+1
                            data[i+count][j]='place'

data=labreview(data)
data=lecturereview(data)
data=weeekendstudy(data)
user=UserGUI(data)
icsfilemaker(user.data)
endtime=timing.time()
print '%f s to run program'%(endtime-starttime)

