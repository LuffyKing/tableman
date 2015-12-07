import time as timing
starttime=timing.time()
import re
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFilter
import pytesseract
import datetime as dt
from guis import TextCorrectionGUI
from guis import UserGUI
#the above are the guis for textcorrection and table adjustments
import os
from horizontal_slicer import sobel
from vertical_slicer import vertslice
from timesort import timesort
from studyplanner import labreview,lecturereview,weeekendstudy
from icsmaker import icsfilemaker

if not os.path.exists((os.path.expanduser("~/Desktop/blaze"))):
    os.mkdir(os.path.expanduser("~/Desktop/blaze"))
def c2I(ideal):#converts from cv2 to Image
    ideal= cv2.cvtColor(ideal,cv2.COLOR_GRAY2RGB)

    ideal = Image.fromarray(ideal)
    return ideal
def I2c(ideal):#converts from Image to cv2
    ideal=np.array(ideal)

    ideal= cv2.cvtColor(ideal,cv2.COLOR_RGB2GRAY)
    return ideal

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

data=labreview(data,timecolumn)
data=lecturereview(data,timecolumn)
data=weeekendstudy(data,timecolumn)
user=UserGUI(data)
icsfilemaker(user.data)
endtime=timing.time()
print '%f s to run program'%(endtime-starttime)
