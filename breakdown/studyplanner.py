import re
import random
from empty_cell_finders import listofemptycells
from empty_cell_finders import listofemptycells2
import datetime as dt

def lecturereview(datalist,timecolumn):#places lecture reviews after every lecture
    pattern=re.compile(r'\w+')
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


        for j in xrange(1,len(datalist)):
            if 'Lecture' in datalist[j][i] and 'Review' not in datalist[j][i]:
                spacelist=listofemptycells(datalist)[datalist[0][i]]#for an element/textblock in the inner list all the free times are gotten
                for k in spacelist:#iterating through the list of of free times
                    if dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M")<dt.datetime.strptime(k, "%I %M %p").strftime("%H %M"):
                        """
                    The if statement compares the free times from spacelist and the currrent textblock and makes sure that the
                    times allowed are greater than the current textblock timeslot.
                        """

                        wordsoftextblock=re.findall(pattern,datalist[j][i])
                        """
                        find all words but we are mainly aiming for the course name and course code

                        """
                        etime=dt.datetime.strptime(k,"%I %M %p")+dt.timedelta(minutes=50)
                        etime=etime.strftime("%I %M %p")
                        """
                        We make the end time(lecture reviews are 50 mins long) for the textblock and construct a textblock as follows
                        somesubject 3RA3
                        Lecture Review
                        8 00 AM - 8 50 AM
                        """

                        text='%s %s\n%s\n%s - %s'%(wordsoftextblock[0],wordsoftextblock[1],'Lecture Review',k,etime)
                        datalist[timecolumn.index(k)][i]=text#text placed here
                        datalist[timecolumn.index(k)+1][i]='place'#pointer for spanning


                        break
    return datalist




def weeekendstudy(datalist,timecolumn):#creates a weekend study plan
    pattern2=re.compile(r'.+\d\w+')#to divide textblacks line by line
    listtext=[]
    point=[]
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



        for j in xrange(1,len(datalist)):

            if 'Lecture' in datalist[j][i] and 'Review' not in datalist[j][i]:

                text=re.findall(pattern2,datalist[j][i])[0]#pick the first line of the textblock
                """
                Example:
                SFWRENG 3MX3 - C01/n blah blah/n.../n...
                picks SFWRENG 3MX3 - C01
                """
                #quick way to generate a lists without duplicates
                try:

                    listtext.index(text)

                except:
                    listtext.append(text)
    while len(listtext)>0:

        point.append(listtext.pop(random.randint(0,len(listtext)-1)))
        """
        randomizes the  order in which the courses appear
        """


    for text in point:

        spacelistweekend=listofemptycells2(datalist)

        days=spacelistweekend.keys()
        #days=[Sat,Sun]
        days.sort()
        if spacelistweekend[days[0]]!=[]:#if the list of freetimes for saturday is not empty continue
            k=days[0]
            for l in spacelistweekend[k]:


                timeend=dt.datetime.strptime(datalist[timecolumn.index(l)][0], "%I %M %p")+dt.timedelta(hours=2)
                """
                Add two hours to the time
                """
                timeend=timeend.strftime("%I %M %p")
                text3='%s\n%s - %s'%(text, datalist[timecolumn.index(l)][0],timeend)
                """
                Example:
                SFWRENG 3MX3 - C01/n blah blah/n.../n...
                picks SFWRENG 3MX3 - C01
                """

                datalist[timecolumn.index(l)][datalist[0].index(k)]=text3
                datalist[timecolumn.index(l)+1][datalist[0].index(k)]='place'#pointer for spanning
                datalist[timecolumn.index(l)+2][datalist[0].index(k)]='place'#pointer for spanning
                datalist[timecolumn.index(l)+3][datalist[0].index(k)]='place'#pointer for spanning
                datalist[timecolumn.index(l)+4][datalist[0].index(k)]='place'#pointer for spanning
                break
        elif spacelistweekend[days[1]]!=[]:#if the list of freetimes for sunday is not empty continue
            k=days[1]
            for l in spacelistweekend[k]:


                timeend=dt.datetime.strptime(datalist[timecolumn.index(l)][0], "%I %M %p")+dt.timedelta(hours=2)
                """
                Add two hours to the time
                """
                timeend=timeend.strftime("%I %M %p")
                """
                Make the end time
                """
                text3='%s\n%s - %s'%(text, datalist[timecolumn.index(l)][0],timeend)
                """
                Example:
                SFWRENG 3MX3 - C01/n blah blah/n.../n...
                picks SFWRENG 3MX3 - C01
                """
                datalist[timecolumn.index(l)][datalist[0].index(k)]=text3
                datalist[timecolumn.index(l)+1][datalist[0].index(k)]='place'#pointer for spanning
                datalist[timecolumn.index(l)+2][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+3][datalist[0].index(k)]='place'
                datalist[timecolumn.index(l)+4][datalist[0].index(k)]='place'
                break
    return datalist






def labreview(datalist,timecolumn):#puts a labreview before every lab
    pattern=re.compile(r'\w+')
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


        for j in xrange(1,len(datalist)):
            if 'Lab' in datalist[j][i] and 'Review' not in datalist[j][i]:
                listoftimes=[]

                spacelist=listofemptycells(datalist)[datalist[0][i]]#for an element/textblock in the inner list all the free times are gotten
                for k in spacelist:

                    if dt.datetime.strptime(datalist[j][0], "%I %M %p").strftime("%H %M")>dt.datetime.strptime(k, "%I %M %p").strftime("%H %M"):
                        """
                    The if statement compares the free times from spacelist and the currrent textblock and makes sure that the
                    times allowed are lesser than the current textblock timeslot.
                        """
                        listoftimes.append(k)


                try:
                    time=listoftimes[len(listoftimes)-1]
                    wordsoftextblock=re.findall(pattern,datalist[j][i])
                    """
                    find all words but we are mainly aiming for the course name and course code

                    """
                    etime=dt.datetime.strptime(k,"%I %M %p")+dt.timedelta(minutes=50)
                    etime=etime.strftime("%I %M %p")
                    """
                    We make the end time(lecture reviews are 50 mins long) for the textblock and construct a textblock as follows
                    somesubject 3RA3
                    Lecture Review
                    8 00 AM - 8 50 AM
                    """
                    text='%s %s\n%s\n%s - %s'%(wordsoftextblock[0],wordsoftextblock[1],'Lab Review',time,etime)
                    datalist[timecolumn.index(time)][i]=text
                    datalist[timecolumn.index(time)+1][i]='place'
                except:
                    pass
    return datalist



