import cv2
from operator import itemgetter
import numpy as np
def sobel(image):#gets a list of horizontal slices

    pictures=[]
    sobelx8u = cv2.Sobel(image,cv2.CV_8U,0,1,ksize=-1)
    edges = cv2.Canny(sobelx8u,0,250,apertureSize = 3)#uses canny edge detection to get the edges from the sobel image which has gotten rid of vertical lines
    lines = cv2.HoughLinesP(edges,1,np.pi/2,150, minLineLength = image.shape[1]-50, maxLineGap = 10)#houghlines probabilistic function has been set to detect horizontal lines
    horizontal_lines=[]
    line=[]
    width=[]#used to determine the maximum width of the image
    try:
        for x1,y1,x2,y2 in lines[0]:



            width.append(x2)
            horizontal_lines.append([x1,y1,x2,y2])


        horizontal_lines=sorted(horizontal_lines,key=itemgetter(1))#sorts out the coordinates by setting the first horizontal line first in the list horizontal_lines
        for i in horizontal_lines:



            try:

                if horizontal_lines[horizontal_lines.index(i)+1][1]-i[1]<10:

                    del horizontal_lines[horizontal_lines.index(i)+1]


            except:

                pass
            """
            The above try statement removes noisy horizontal lines
            """
        if horizontal_lines[0][1]>10 :
                line.append(0)
        """
        The above makes sure that zero is a the top of the horizontal lines
        """
        for i in horizontal_lines:
            line.append(i[1])
            "This takes the y coordinate of the horizontal line"


        for i in line:
            try:

                pictures.append(image[i:line[line.index(i)+1],0:max(width)])
            except:
                pass
        "The images are sliced above by iterating of the line list of y coordinates of the horizontal lines"



        return pictures
    except:
        pass