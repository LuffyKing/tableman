import cv2
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