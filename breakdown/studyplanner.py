import re
import random
from empty_cell_finders import listofemptycells
from empty_cell_finders import listofemptycells2
import datetime as dt

def lecturereview(datalist,timecolumn):#places lecture reviews after every lecture
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




def weeekendstudy(datalist,timecolumn):#creates a weekend study plan

    pattern=re.compile(r'\w+')
    pattern2=re.compile(r'.+\d\w+')
    listtext=[]
    point=[]
    for i in xrange(1,len(datalist[0])):



        for j in xrange(1,len(datalist)):

            if 'Lecture' in datalist[j][i] and 'Review' not in datalist[j][i]:

                text=re.findall(pattern2,datalist[j][i])[0]
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






def labreview(datalist,timecolumn):#puts a labreview before every lab
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



