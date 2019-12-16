"""finds pupil, exports center and perimeter  """
import math
import sys
#import getopt
import numpy as np
import cv2  #add OpenCV Library
#import argparse
import matplotlib.pyplot as plt

INIT_THRESH = 50#150 #Initial Threshold Value
PUPIL_MIN = 600
PUPIL_MAX = 600000
DEFAULT_FILE_NAME = "right.bmp"
#text
FONT = cv2.FONT_HERSHEY_SIMPLEX

class Point():
    """Dont remember what this is for """
    x = -1
    y = -1
    x_l = -1
    x_r = -1
    y_t = -1
    y_b = -1


def rank_p_filter(imgray, length, rank):
    '''
    #rank_p_filter - 1D horizontal rank-p filter
    #input: grayscale image, Length, rank
    '''
    imgray_out = imgray.copy()

    if (length % 2) == 1:
        m = int((length-1)/2)  # -----!-----
    else:
        raise ValueError('Length must be odd')

    if(rank>length):
        raise ValueError('Rank (rank) cannot be greater than length (length).')

    h = imgray.shape[0]
    w = imgray.shape[1]

    for i in np.arange(m,h-m):
        for j in np.arange(m,w-m):
            window = imgray[i,j-m:j+m+1]
            values, index = np.unique(window, return_index = True)

            if(index.size < rank): #not enouph ranks
                pass
            else:
                imgray_out[i,j] = window[index[index.size-rank]]
                # print('window', window)
                # print('sorted values',values)
                # print('index', index)
                # print('result',imgray_out[i,j-length:j+length+1])
                # print('result v',imgray_out[i,j])

    cv2.imshow('no lashes?', imgray_out)
    return imgray_out


#pupilContour
#input: color image, graysacle theshold, minimum pupil size, maximum pupil size
#output contour
def pupilContour(img,threshold, debug = 1):
    #Find contour
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,threshImg = cv2.threshold(imgray,INIT_THRESH,255,0)

    if debug > 1:
        cv2.imshow('threshold',threshImg)
        cv2.imshow('gray',imgray)
        cv2.waitKey(0) #TODO: make this a flag

    #for threshold testing
    threshImgCopy = cv2.cvtColor(threshImg,cv2.COLOR_GRAY2RGB)
    imgCopy = img.copy()

    contourCandidates = []
    #find the iris contour
    #for this image
    print(threshold)
    contours, _ = cv2.findContours(threshImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    bestContour = np.empty(contours[1].shape) #Empty Contour
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > PUPIL_MIN and area < PUPIL_MAX:

            #circle test
            perimeter = cv2.arcLength(contour, True)
            circularity = 4*math.pi*(area/(perimeter*perimeter))
            if perimeter == 0:
                break

            if debug > 1:
                cv2.drawContours(threshImgCopy, contour, -1, (0,255,0), 3)
                cv2.drawContours(imgCopy, contour, -1, (0,255,0), 3)
                cv2.imshow("Contour Testing RAW", imgCopy)
                cv2.imshow("Contour Testing Thresh", threshImgCopy)
                print("circularity = ", circularity)
                print("Contour Area = ", cv2.contourArea(contour))
                cv2.waitKey(0)

            if(circularity > 0.80):
                contourCandidates.append({'Circularity': circularity, 'Contour': contour})

    #if nothing found
    if contourCandidates == []:
        return np.empty(contours[1].shape)
    else:
        #get best candidate (top circularity for now)
        sortedContourCandidates = sorted(contourCandidates, key= lambda k: k['Circularity'], reverse = True)
        #print(contourCandidates)
        bestContour = sortedContourCandidates[0]["Contour"]
        #print(bestContour)
        return bestContour

#Pupillometry
#input1: input_, string of source file or cv2 image
#input2: dubug, debug level
#input3: method 1 = V.S. 2 = ZH
#output: saves CSV file of contour of pupil and avi file, returns imgFile w/ edit
def pupillometry(input_, debug = 2, method = 1 ):

    if isinstance(input_, str):
        img = cv2.imread(input_)
    else:
        img = input_

    imgMain = img.copy() #Main to display of what's going on
    baseName = "test"

    if debug > 0:
        cv2.imshow('Main',img)

    if(method == 1):
        #CSV file
        # try:
        #     os.remove("data.csv")
        # except:
        #     return "something went wrong"
        csvdata = open(baseName+'.csv', "w")
        csvdata.write('timestamp (ms),data (radius,radians)\n')
        contourFound = False
        #keep trying with different thresholds, until you find something
        for i in range(0,20,5):
            try:
                # #Find best contour
                bestContour = pupilContour(img,INIT_THRESH + i,debug)
                #Find distance from center of contour and contour
                Csize, _ , _ = bestContour.shape
                radius = np.empty(Csize)
                M=cv2.moments(bestContour)
                contourFound = True
                break #exit loop
            except cv2.error as e:
                print('try again')

        #failed to find something
        if(contourFound == False):
            skipStr = "skip"
            cv2.putText(imgMain, skipStr, (230, 250), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            rads = np.empty(Csize)
        else:
            cv2.drawContours(imgMain, bestContour, -1, (0,255,0), 3)
            if debug > 0:
                cv2.imshow('Main',imgMain)
                if debug > 1:
                    cv2.waitKey(0)
            index = 0
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            cv2.circle(imgMain,(centroid_x,centroid_y), 5, (0,0,255), -1)
            if debug > 0:
                cv2.imshow('Main',imgMain)
                cv2.waitKey(0)

            for n in bestContour:
                dx = centroid_x-n[0][0]
                dy = centroid_y-n[0][1]
                radius[index] = math.sqrt( dx**2 + dy**2 )
                index += 1
            #Find angle from center of circle and contour
            rads = np.empty(Csize)
            index = 0
            for n in bestContour:
                dx = centroid_x-n[0][0]
                dy = centroid_y-n[0][1]
                rads[index] = math.atan2(dy,dx)
                index += 1
            # # #print rads
            time = 1
            #save to csv
            csvdata.write(str(time)+',')
            np.savetxt(csvdata,radius, '%s',delimiter=',', newline=',')
            csvdata.write('\n')
            csvdata.write(str(time))
            np.savetxt(csvdata, rads, '%s', delimiter=',', newline=',')
            csvdata.write('\n')
            if debug > 0:
                plt.ion()
                plt.clf()
                plt.axis([-4,4,0,200])
                plt.plot(rads,radius,'ro')
                plt.ylabel('radius (pixels)')
                plt.xlabel('angle (radians)')
                plt.show()
                plt.pause(0.10)
                if debug > 1:
                    cv2.waitKey(0)
        return imgMain, rads, radius
    elif method == 2: #Zhaofeng He Method.

        #Reflection Removal and Iris Detection
        #"reflection" map
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, threshImg = cv2.threshold(imgray,200,255,0) #TODO:Make adaptive
        height, width = imgray.shape
        cv2.imshow('pre-E',threshImg)
        E = 4 # epsilon in pixels to expand reflection area

        #rank-p filter
        L_RANK_FILTER = 13
        p_RANK_FILTER = 2

        for n in range(0,E):
            print('n:',n)
            rfPoints = np.where(threshImg == 255) #white points
            listOfRfPoints = list(zip(rfPoints[0],rfPoints[1])) #list of white point
            for pt in listOfRfPoints:
                ytemp = pt[0]
                xtemp = pt[1]

                if( xtemp + 1 < width):
                    threshImg[ytemp,xtemp+1] = 255
                if( xtemp + 1 < width and ytemp+1 < height ):
                    threshImg[ytemp+1,xtemp+1] = 255
                if( ytemp+1 < height ):
                    threshImg[ytemp+1,xtemp] = 255
                if( ytemp+1 < height and xtemp-1 >= 0):
                    threshImg[ytemp+1,xtemp-1] = 255
                if(xtemp-1 >= 0):
                    threshImg[ytemp,xtemp-1] = 255
                if(xtemp-1 >= 0 and ytemp-1 >= 0):
                    threshImg[ytemp-1,xtemp-1] = 255
                if(ytemp-1 >= 0):
                    threshImg[ytemp-1,xtemp] = 255
                if(ytemp-1 >= 0 and xtemp + 1 < width):
                    threshImg[ytemp-1,xtemp+1] = 255

        cv2.imshow('post-E',threshImg)
        #print(threshImg[1,1])


        #bilinear interpolation
        L = 2  # separation between the reflection points and their envelope points
        bi_imgray = imgray.copy()
        bi_threshImg = threshImg.copy()

        rfPoints = np.where(threshImg == 255) #white points
        listOfRfPoints = list(zip(rfPoints[0],rfPoints[1])) #list of white points
        points = np.full((height,width),Point()) #matrix of all points

        for pt in listOfRfPoints:
            ytemp = pt[0]
            xtemp = pt[1]
            x_l = -1
            x_r = -1
            y_t = -1
            y_b = -1
            #threshImg[ytemp,xtemp] = 0
            cv2.imshow('threshold',threshImg)
            #print(ytemp,xtemp)
            #cv2.waitKey(0)

            points[ytemp,xtemp].x = xtemp
            points[ytemp,xtemp].y = ytemp
            #find x_l
            if(xtemp > L-1):#not along the edge
                for k in range(xtemp-1,-1,-1):
                    if(threshImg[ytemp,k]==0):
                        x_l = k-(L-1)
                        points[ytemp,xtemp].x_l = x_l
                        bi_threshImg[ytemp,x_l] = 100
                        #print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_l = -1


            #find x_r
            if(xtemp < 719-L):#not along the edge
                for l in range(xtemp+1,719-L):
                    if(threshImg[ytemp,l]==0):
                        x_r = l+(L-1)
                        points[ytemp, xtemp].x_r = x_r
                        bi_threshImg[ytemp,x_r] = 100
                        #print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_r = -1

            #find y_b
            if(ytemp > L-1): #not along the edge
                for m in range(ytemp-1,-1,-1):
                    if(threshImg[m,xtemp]==0):
                        y_b = m-(L-1)
                        points[ytemp,xtemp].y_b = y_b
                        bi_threshImg[y_b,xtemp] = 100
                        #print(ytemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_b = -1

            #find y_t
            if( ytemp < 479-L):
                for n in range(ytemp+1,479-L):
                    if(threshImg[n,xtemp]==0):
                        y_t = n+(L-1)
                        points[ytemp,xtemp].y_t = y_t
                        bi_threshImg[y_t,xtemp] = 100
                        #print(ytemp)
                        #TODO: move backwarda and fill in the rest.
                        break
            else:
                y_t = -1


            if( x_l != -1 and x_r != -1 and  y_b != -1 and y_t != -1):
                #print('xtemp: ',xtemp,'ytemp: ', ytemp, 'x_l: ',x_l,'x_r: ', x_r,'y_t: ', y_t,'y_b: ', y_b)
                #print('I(P_L):',imgray[ytemp,x_l],'I(P_R):',imgray[ytemp,x_r],'I(P_t):',imgray[y_t,xtemp],'I(P_d):',imgray[y_b,xtemp])
                #cv2.waitKey(0)
                bi_imgray[ytemp,xtemp] = (imgray[ytemp,x_l]*(x_r-xtemp)+imgray[ytemp,x_r]*(xtemp-x_l))/(2*(x_r-x_l)) + \
                                         (imgray[y_t,xtemp]*(ytemp-y_b)+imgray[y_b,xtemp]*(y_t-ytemp))/(2*(y_t-y_b))

        lp_imgray = rank_p_filter(bi_imgray,L_RANK_FILTER,p_RANK_FILTER) #L-length p-rank

        if debug > 1:
            cv2.imshow('threshold',threshImg)
            cv2.imshow('gray',imgray)
            cv2.imshow('bi',bi_imgray)
            cv2.imshow('bi_threshold',bi_threshImg)
            cv2.waitKey(0) #TODO: make this a flag
        #Pupillary & Limbic Bd. Localizatoin
        #Eyelid Localization
        #Eyelash and Shadow Detection
        return imgMain, rads, radius
if __name__ == "__main__":
    print(len(sys.argv))
    if(len(sys.argv) > 1):
        if(len(sys.argv) == 2):
            method = int(sys.argv[1])
            filename = DEFAULT_FILE_NAME
        if(len(sys.argv) == 3):
            method = int(sys.argv[1])
            filename = sys.argv[2]
    else:
        method = 1
        filename = DEFAULT_FILE_NAME
    print("Method : ",method)
    print("File Name",filename)
    pupillometry(filename,2,method)
