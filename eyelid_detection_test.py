# script for tuning parameters
import time
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt

# parse argument
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# reads the image
img = cv2.imread(args['image'])
height, width = img.shape[:2]

#disply input
pupilCenter = (int(width * .5)-20,int(height * .5))#guess for now
img_input = img.copy()
print(pupilCenter)
cv2.circle(img_input,pupilCenter,4,(0,0,255),-1)
cv2.imshow('input',img_input)


start_row, start_col = int(0), int(0)
end_row, end_col = pupilCenter[1], int(width)

img_top = img[start_row:end_row , start_col:end_col]
#img_top =  cv2.GaussianBlur(img_top,(3,3),0)

img_top = cv2.cvtColor(img_top, cv2.COLOR_BGR2GRAY)

img_bottom = img[end_row:height , start_col:end_col]
#img_bottom = cv2.GaussianBlur(img_bottom,(3,3),0)
img_bottom = cv2.cvtColor(img_bottom, cv2.COLOR_BGR2GRAY)

cv2.imshow('topRaw',img_top)
cv2.imshow('bottomRaw',img_bottom)

def noisy_edge_elimination(Eraw,pupilCenter):
    #Eliminate noisy edge points via shape similarity calculation
    rightSize = len(Eraw)-pupilCenter[0]-1
    leftSize = len(Eraw)-rightSize-1
    x = np.arange(-leftSize,rightSize+1)

    #limit to +/-100 pixels (future limit to contras only in iris)
    x100 = np.arange(-100,100+1)
    Eraw100 = []
    for n in np.arange(-100,100+1):
        Eraw100.append(Eraw[pupilCenter[0]-n])

    M2a = 0.001
    M2 = -M2a*(x100**2)+66
    M3 = -M2a*(x100**2)+66 + 0.16*x100+0.0008*(x100**2)
    M1 = -M2a*(x100**2)+66 - 0.16*x100+0.0008*(x100**2)

    D1 = M1-Eraw100
    D2 = M2-Eraw100
    D3 = M3-Eraw100

    histD2, bin_edges_D2 = np.histogram(D2, bins='auto')
    histD1, _ = np.histogram(D1, bins=bin_edges_D2)
    histD3, _ = np.histogram(D3, bins=bin_edges_D2)

    #find max
    _, maxValD2, _, maxLocD2 = cv2.minMaxLoc(histD2)
    _, maxValD3, _, maxLocD3 = cv2.minMaxLoc(histD3)
    _, maxValD1, _, maxLocD1 = cv2.minMaxLoc(histD1)

    maxVals=[maxValD1,maxValD2,maxValD3]
    maxM = maxVals.index(max(maxVals))

    if maxM==0:
        pass#use M1
    elif maxM==1:
        pass#use M2
    elif maxM==2:
        pass#use M3

    print(histD2)
    print(histD1)
    print(histD3)

    plt.subplot(2,3,1)
    #plt.xlim(-100, 100)
    plt.ylim(0, 105)
    plt.plot(x100,M1, label="M1", color='black',linestyle='dashdot')
    plt.plot(x100,M2, label="M2", color='red',linewidth=2)
    plt.plot(x100,M3, label="M3", color='blue',linestyle='dashed')
    plt.plot(x100,Eraw100, label="Eraw", color='orange')
    plt.legend()
    plt.subplot(2,3,2)
    plt.plot(x100,D1, label="D1", color='black',linestyle='dashdot')
    plt.plot(x100,D2, label="D2", color='red')
    plt.plot(x100,D3, label="D2", color='blue', linestyle='dashed')
    plt.legend()
    plt.subplot(2,3,3)
    plt.hist(D1, bins=bin_edges_D2, label='Hist. D1',color='black',linestyle='dashdot')
    plt.hist(D3, bins=bin_edges_D2, label='Hist. D3', color='blue', linestyle='dashed')
    plt.hist(D2, bins=bin_edges_D2, label='Hist. D2', color='red')
    plt.xlim(-40, 40)
    plt.legend()
    plt.show()
    return 1


def max_edge(imgray_in):
    imgray_out = cv2.cvtColor(imgray_in,cv2.COLOR_GRAY2RGB)
    h = imgray_in.shape[0]
    w = imgray_in.shape[1]

    maxEdgePoints = []

    for i in np.arange(0,w-1):
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(imgray_in[:,i])#find max
        imgray_out[maxLoc[1],i,0] = 0
        imgray_out[maxLoc[1],i,1] = 0
        imgray_out[maxLoc[1],i,2] = 255
        maxEdgePoints.append(h-maxLoc[1])
    return maxEdgePoints, imgray_out

# empty callback function for creating trackar
def callback(foo):
    pass

# create windows and trackbar
cv2.namedWindow('parameters')
cv2.createTrackbar('scale', 'parameters', 1, 3, callback)  # change the maximum to whatever you like
cv2.createTrackbar('delta', 'parameters', 0, 3, callback)  # change the maximum to whatever you like
cv2.createTrackbar('apertureSize', 'parameters', 0, 2, callback)

ddepth = -1

scalePast = cv2.getTrackbarPos('scale', 'parameters')
deltaPast = cv2.getTrackbarPos('delta', 'parameters')
apSizePast = cv2.getTrackbarPos('apertureSize', 'parameters')*2+3
first = True;

while(True):
    # get threshold value from trackbar
    scale = cv2.getTrackbarPos('scale', 'parameters')
    delta = cv2.getTrackbarPos('delta', 'parameters')

    # aperture size can only be 3,5, or 7
    apSize = cv2.getTrackbarPos('apertureSize', 'parameters')*2+3

    if  ((first == True) or scalePast != scale) or (deltaPast != delta) or (apSizePast != apSize) :
        first = False
        # print out the values
        print('scale: {}'.format(scale))
        print('delta: {}'.format(delta))
        print('apertureSize: {}'.format(apSize))

        #edge_top = cv2.Canny(img_top, th1, th2, apertureSize=apSize, L2gradient=norm_flag)
        sobely_top = cv2.Sobel(img_top,ddepth,0,1,ksize=apSize, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        maxEdgePointsTop ,imtop = max_edge(sobely_top)
        print((pupilCenter[0],0))
        noisy_edge_elimination(maxEdgePointsTop, (pupilCenter[0],0))
        cv2.imshow('top', imtop)

        #edge_bottom = cv2.Canny(img_bottom, th1, th2, apertureSize=apSize, L2gradient=norm_flag)
        sobely_bottom = cv2.Sobel(img_bottom,ddepth,0,1,ksize=apSize, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        maxEdgePointsBottom ,imbot = max_edge(sobely_bottom)
        cv2.imshow('bot',imbot)

        abs_grad_y_top = cv2.convertScaleAbs(sobely_top)
        abs_grad_y_bottom = cv2.convertScaleAbs(sobely_bottom)

        cv2.imshow('canny_top', abs_grad_y_top)
        cv2.imshow('canny_bottom', abs_grad_y_bottom)

        scalePast = scale
        deltaPast = delta
        apSizePast = apSize

    if cv2.waitKey(1)&0xFF == ord('q'):
        break

    time.sleep(0.1)

cv2.destroyAllWindows()
