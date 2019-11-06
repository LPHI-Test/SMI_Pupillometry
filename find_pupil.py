import numpy as np
import cv2  #add OpenCV Library
#import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys, getopt

initThresh = 50#150 #Initial Threshold Value
pupilMax = 600000
defaultFileName = "right.bmp"
#text
font = cv2.FONT_HERSHEY_SIMPLEX

class Point():
    x = -1
    y = -1
    x_l = -1
    x_r = -1
    y_t = -1
    y_b = -1

#pupilContour
#input: color image, graysacle theshold, minimum pupil size, maximum pupil size
#output contour
def pupilContour(img,threshold, debug = 1):
    #Find contour
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,threshImg = cv2.threshold(imgray,initThresh,255,0)

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
        if area > pupilMin and area < pupilMax:

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
                bestContour = pupilContour(img,initThresh + i,debug)
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
            cv2.putText(imgMain, skipStr, (230, 250), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
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

        print(threshImg[1,1])

        height, width = imgray.shape
        #bilinear interpolation
        bi_imgray = imgray.copy()
        bi_threshImg = threshImg.copy()
        rfPoints = np.where(threshImg == 255) #white points
        listOfRfPoints = list(zip(rfPoints[0],rfPoints[1])) #list of white points
        points = np.full((height,width),Point()) #matrix of all points

        for pt in listOfRfPoints:
            ytemp = pt[0]
            xtemp = pt[1]
            #threshImg[ytemp,xtemp] = 0
            cv2.imshow('threshold',threshImg)
            print(ytemp,xtemp)
            #cv2.waitKey(0)

            points[ytemp,xtemp].x = xtemp
            points[ytemp,xtemp].y = ytemp
            #find x_l
            if(xtemp > 1):#not along the edge
                for k in range(xtemp-1,-1,-1):
                    if(threshImg[ytemp,k]==0):
                        x_l = k-1
                        points[ytemp,xtemp].x_l = x_l
                        bi_threshImg[ytemp,x_l] = 100
                        print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_l = -1


            #find x_r
            if(xtemp < 719):#not along the edge
                for l in range(xtemp+1,719):
                    if(threshImg[ytemp,l]==0):
                        x_r = l+1
                        points[ytemp, xtemp].x_r = x_r
                        bi_threshImg[ytemp,x_r] = 100
                        print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_r = -1

            #find y_b
            if(ytemp > 1): #not along the edge
                for m in range(ytemp-1,-1,-1):
                    if(threshImg[m,xtemp]==0):
                        y_b = m-1
                        points[ytemp,xtemp].y_b = y_b
                        bi_threshImg[y_b,xtemp] = 100
                        print(ytemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_b = -1

            #find y_t
            if( ytemp < 479):
                for n in range(ytemp+1,479):
                    if(threshImg[n,xtemp]==0):
                        y_t = n +1
                        points[ytemp,xtemp].y_t = y_t
                        bi_threshImg[y_t,xtemp] = 100
                        print(ytemp)
                        #TODO: move backwarda and fill in the rest.
                        break
            else:
                y_t = -1


            if( x_l != -1 and x_r != -1 and  y_b != -1 and y_t != -1):
                print('xtemp: ',xtemp,'ytemp: ', ytemp, 'x_l: ',x_l,'x_r: ', x_r,'y_t: ', y_t,'y_b: ', y_b)
                print('I(P_L):',imgray[ytemp,x_l],'I(P_R):',imgray[ytemp,x_r],'I(P_t):',imgray[y_t,xtemp],'I(P_d):',imgray[y_b,xtemp])
                #cv2.waitKey(0)
                bi_imgray[ytemp,xtemp] = (imgray[ytemp,x_l]*(x_r-xtemp)+imgray[ytemp,x_r]*(xtemp-x_l))/(2*(x_r-x_l)) + \
                                         (imgray[y_t,xtemp]*(ytemp-y_b)+imgray[y_b,xtemp]*(y_t-ytemp))/(2*(y_t-y_b))




            # for l in range(j-1,0):
            #     if(threshImg[i,l]==0):
            #         points[i,l].x_r = k-1
            #         #TODO: move backwards and fill in the rest.
            #         break
            #         #find l,r,t,d

                    #x_l =
                    #x_r =
                    #y_t =
                    #y_d =

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
            filename = defaultFileName
        if(len(sys.argv) == 3):
            method = int(sys.argv[1])
            filename = sys.argv[2]
    else:
        method = 1
        filename = defaultFileName
    print("Method : ",method)
    print("File Name",filename)
    pupillometry(filename,2,method)
