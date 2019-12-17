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

img_bottom = img[end_row:height , start_col:end_col]

# empty callback function for creating trackar
def callback(foo):
    pass

# create windows and trackbar
cv2.namedWindow('parameters')
cv2.createTrackbar('threshold1', 'parameters', 0, 255, callback)  # change the maximum to whatever you like
cv2.createTrackbar('threshold2', 'parameters', 40, 255, callback)  # change the maximum to whatever you like
cv2.createTrackbar('apertureSize', 'parameters', 0, 2, callback)
cv2.createTrackbar('L1/L2', 'parameters', 0, 1, callback)

ddepth = -1

while(True):
    # get threshold value from trackbar
    th1 = cv2.getTrackbarPos('threshold1', 'parameters')
    th2 = cv2.getTrackbarPos('threshold2', 'parameters')

    # aperture size can only be 3,5, or 7
    apSize = cv2.getTrackbarPos('apertureSize', 'parameters')*2+3

    # true or false for the norm flag
    norm_flag = cv2.getTrackbarPos('L1/L2', 'parameters') == 1

    # print out the values
    print('')
    print('threshold1: {}'.format(th1))
    print('threshold2: {}'.format(th2))
    print('apertureSize: {}'.format(apSize))
    print('L2gradient: {}'.format(norm_flag))



    #edge_top = cv2.Canny(img_top, th1, th2, apertureSize=apSize, L2gradient=norm_flag)
    sobely_top = cv2.Sobel(img_top,ddepth,0,1,ksize=apSize)

    #edge_bottom = cv2.Canny(img_bottom, th1, th2, apertureSize=apSize, L2gradient=norm_flag)
    sobely_bottom = cv2.Sobel(img_bottom,ddepth,0,1,ksize=apSize)

    abs_grad_y_top = cv2.convertScaleAbs(sobely_top)
    abs_grad_y_bottom = cv2.convertScaleAbs(sobely_bottom)

    cv2.imshow('canny_top', abs_grad_y_top)
    cv2.imshow('canny_bottom', abs_grad_y_bottom)




    if cv2.waitKey(1)&0xFF == ord('q'):
        break

    time.sleep(0.1)

cv2.destroyAllWindows()
