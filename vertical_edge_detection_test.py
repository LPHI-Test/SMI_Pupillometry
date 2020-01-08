# script for tuning parameters
import time
import cv2
import numpy as np
import argparse

# parse argument
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# reads the image
img = cv2.imread(args['image'])

height, width = img.shape[:2]

start_row, start_col = int(0), int(0)
end_row, end_col = int(height * .5), int(width)

img_top = img[start_row:end_row , start_col:end_col]
#img_top =  cv2.GaussianBlur(img_top,(3,3),0)
img_top = cv2.cvtColor(img_top, cv2.COLOR_BGR2GRAY)


img_bottom = img[end_row:height , start_col:end_col]
#img_bottom = cv2.GaussianBlur(img_bottom,(3,3),0)
img_bottom = cv2.cvtColor(img_bottom, cv2.COLOR_BGR2GRAY)


def max_edge(imgray_in):
    imgray_out = cv2.cvtColor(imgray_in,cv2.COLOR_GRAY2RGB)
    h = imgray_in.shape[0]
    w = imgray_in.shape[1]

    for i in np.arange(0,w-1):
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(imgray_in[:,i])#find max
        imgray_out[maxLoc[1],i,0] = 0
        imgray_out[maxLoc[1],i,1] = 0
        imgray_out[maxLoc[1],i,2] = 255
    return imgray_out

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
        imtop = max_edge(sobely_top)
        cv2.imshow('top', imtop)

        #edge_bottom = cv2.Canny(img_bottom, th1, th2, apertureSize=apSize, L2gradient=norm_flag)
        sobely_bottom = cv2.Sobel(img_bottom,ddepth,0,1,ksize=apSize, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        imbot = max_edge(sobely_bottom)
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
