import numpy as np
import cv2  #add OpenCV Library
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys, getopt

initThresh = 50#150 #Initial Threshold Value
pupilMin = 600
pupilMax = 600000
#text
font = cv2.FONT_HERSHEY_SIMPLEX
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
#output: saves CSV file of contour of pupil and avi file, returns imgFile w/ edit
def pupillometry(input_, debug = 2 ):

    if isinstance(input_, str):
        img = cv2.imread(input_)
    else:
        img = input_

    imgMain = img.copy() #Main to display of what's going on
    baseName = "test"

    if debug > 0:
        cv2.imshow('Main',img)

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

if __name__ == "__main__":
    pupillometry("right.bmp")
