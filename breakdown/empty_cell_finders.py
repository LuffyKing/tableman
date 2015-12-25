import datetime as dt
def listofemptycells(datalist):#function to get the list of empty cells for weekdays

    day={}
    """
    The for loop is accessing the datalist, each element of the list is
    accessed in the a columnar fashion.The datalist is a list of lists.
    for example the first element of datalist is
    ['Time','Monday','Tuesday',...,'Sunday']
    and the second element of datalist is
    ['7 00 AM','Somesubject',...]
    and the third element of datalist is
    ['7 30 AM','Somesubject1',..]
    The for loop starts from the second element hence the 1 for the i loop
    and starts at 'Somesubject' skipping '7 00 AM' hence the 1 for the j loop.
    Then the next j element will be 'Somesubjects1'.
    """
    for i in xrange(1,len(datalist[0])):

        daylist=[]
        for j in xrange(1,len(datalist)):

            if j+1>=len(datalist):#avoids index error
                pass

            elif datalist[j][i]=='' and datalist[j+1][i]=='':#50min time space,simply checks if the space is two textblocks which is about 50 mins
                """
                An example of what goes on
                Lets say the loop is a the following element below(the '' is where the loop is the list is just there for illustration)
                ['7 00 AM','',...]
                It then checks if the space below is empty  and if it is it appends the index of '' above
                ['7 30 AM','',...]
                ['8 00 AM','somesubject',...]
                so the 50 mins comes into play because we cant span to the 8AM time slot as it will over-ride somesubject
                so we schedule 10 mins before somesubject

                """
                daylist.append(datalist[j][0])

        day[datalist[0][i]]=daylist
    return day
def listofemptycells2(datalist):#function to get the list of empty cells for weekends

    day={}
    for i in xrange(len(datalist[0])-2,len(datalist[0])):

        daylist=[]
        for j in xrange(1,len(datalist)):

            if j+4>=len(datalist):
                pass
            elif datalist[j][i]=='' and datalist[j+4][i]=='':#two hour time space
                if dt.datetime.strptime('09 00 AM', "%I %M %p").strftime("%H %M")<dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M") and dt.datetime.strptime('06 30 PM', "%I %M %p").strftime("%H %M")>dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M"):
                    "The above if statement gets all the free time for saturday and sunday betwwen 9 AM and 6 30 PM"
                    daylist.append(datalist[j][0])

        day[datalist[0][i]]=daylist
    return day