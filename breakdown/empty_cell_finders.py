import datetime as dt
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