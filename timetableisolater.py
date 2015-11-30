import numpy as np
import cv2
import pytesseract
from PIL import Image
from PIL import ImageFilter
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (3, 3), 0)#applies a gaussian blur to help with the edge detection
    
    squares = []#list to contain all the coordinates of squares/rectangles in the image
    bbox=[]#boundary box information of the squares
    #areas={}#dictionary to contain all the areas of the squares
    
    b=img[:,:,0]
    g=img[:,0,:]
    r=img[0,:,:]
    bgr=[b,g,r]
    """
    The above process is to split the image into blue,green and red colour channels this was done.
    This method of numpy indexing was used because cv2.split() is a costly function.
    Each resulting channel is gray which is essential for performing a lot of cv2 operations.
    Uncomment the following lines to see the individual channels
    """
    #cv2.imshow('windowblue',b)
    #cv2.imshow('windowgreen',g)
    #cv2.imshow('windowred',r)
    
    for gray in bgr:#iterates over each channel
        
        for thrs in xrange(0, 255, 26):#iterates over the pixel range 0 to 255 at intervals of 26
            if thrs == 0:
                bins= cv2.Canny(gray, 0, 25, apertureSize=3)#performs canny edge detection to get the edges in an image, the pixel range is from 0 to 25
                bins= cv2.dilate(bins, None)#comment below
                """
                This performs the dilation operation from cv2.This means if you have a black image on a white background
                it will force the black image to take up more white space, hence the term 'dilate'.
                """
            else:
                retval, bins = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)#this function turns the image black and white.Explanation below
                """
                cv2.threshold(image,threshold value,value to be given if more than threshold value,type of threshold)
                turns an image black and white, it does this by setting  any pixel higher than the specified threshold value
                to black and the rest white.
                The bins variable is the image(numpy array) while retval is not useful.
                """
            contours, hierarchy = cv2.findContours(bins, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            """
            cv2.findCountours(image,mode,method) is a function that finds contours(http://opencvpython.blogspot.ca/2012/06/hi-this-article-is-tutorial-which-try.html)
            and their hierarchy( http://opencvpython.blogspot.ca/2013/01/contours-5-hierarchy.html).This mainly used to aid object detection.
            CV_RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours.
            CV_CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments and leaves only their end points. For example, an up-right rectangular contour is encoded with 4 points.
            """
            for j in contours:#iterates over every contour
                cnt_len = cv2.arcLength(j, True)#calculates the perimeter of the contour
                cnt = cv2.approxPolyDP(j, 0.02*cnt_len, True)#this approximates the contour to a straight line by removing small curves with an epsilon of 2%
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    """
                    The above if-statement works as follows:-
                     1. len(cnt) checks if it has 4 points(a square or rectangle) as opposed to 2 straight line
                     2. cv2.contourArea(cnt) calculates the area of the square/rectangle and sees if it is greater than 1000.
                        This is an attempt to weed out noisy/smaller squares.
                     3. cv2.isContourConvex(cnt) is done to check if the square is an idealic shape.For example a normal square instead of a square with jagged edges
                    """
                    cnt = cnt.reshape(-1, 2)#matrix operation to turn it into x X 2 matrix
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)]) #calculates the cosine of the four points and takes the maximum
                    if max_cos < 0.1:#checks if the maximum is less than 0.1
                        #squares.append(cnt)
                        bbox.append(cv2.boundingRect(j))#the function generates a list [x,y,w,h].Let (x,y) be the starting coordinate of rectangle, (w,h) be its width and height.
                        #this is a bounding rectangle around the rectangle to enable extraction

                        #areas[cv2.boundingRect(j)]=cv2.contourArea(cnt)
    return bbox

if __name__ == '__main__':


    clr=cv2.imread('/Users/damola/Desktop/abe.png')
    
    
    
    
    bbox=find_squares(clr)
    """
    The RTREE setting in cv2,findcontours orders the rectangles by which has the most direct rectangle children in this case the timetable
    will have the most rectangle children and therefore be the first in the list.
    """
           
    x,y,w,h =bbox[0]#retrieving the timetable
    
    roi2=clr[y:y+h,x:x+w]#slices up the timetable away from the rest of the image
    
    cv2.imwrite('/Users/damola/Desktop/aloisi.tiff',roi2)#writes it to a file
    
    
    

    #im.save('/Users/damola/Desktop/rasengan.tiff')
