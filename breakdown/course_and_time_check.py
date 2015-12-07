
import re
import enchant
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