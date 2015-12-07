import cv2
import numpy as np
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