#Valentin Siderskiy 10/4/2019
#Integrative Human Physiology Lab
#Rutgers University

#split.py
#This function takes the video input recorded by the
# Night Owel Security stystem, splits the left and right
# and assigns a timestamp based on the night owel clock.

import cv2
import numpy as np
import time

#text
font = cv2.FONT_HERSHEY_SIMPLEX

def resizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def displayLeft(left):
    # Display the Left Eye
    resized_left = resizeWithAspectRatio(left, width = 640) #Resize by
    lString = "Left"
    cv2.putText(resized_left, lString, (0, 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Left Eye',resized_left)
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)


def displayRight(right):
    # Display the Right Eye
    resized_right = resizeWithAspectRatio(right, width = 640) #Resize by
    rString = "Right"
    cv2.putText(resized_right, rString, (0, 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Right Eye',resized_right)
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

def displayMain(frame,cap):
    #Display Main
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    resized_frame = resizeWithAspectRatio(frame, width = 640) #Resize by
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

    framePosition = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fpString = "Frame " + str(framePosition) + '/' + str(fcount)
    cv2.putText(resized_frame, fpString, (230, 350), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    quitString = "Press Q to Quit"
    cv2.putText(resized_frame, quitString, (230, 250), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Frame',resized_frame)


#Operation a freame form Night Owel security stystem use OCR to find out time of
#recording
#Input: frame
#Output: time
def getTime(frame,timestamp):
    print("time")

def main():
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture('SMI_Pupilometry_Test.mp4')

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    timestamp = time.clock()

    is_before_first = True;

    print("WIDTH: ", w)
    print("HEIGHT: ", h)
    print("FPS: ", fps)
    print("FCOUNT: ", fcount)

    # Check if camera opened successfully
    if (cap.isOpened()== False):
      print("Error opening video stream or file")

    #   Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()

      if ret == True:

          #getTime(frame,timestamp)

          leftImage = frame[1:int(h/2),1:int(w/2)]
          rightImage = frame[1:int(h/2),int(w/2+1):w]

          #save first frame to a file
          if(is_before_first and cv2.CAP_PROP_POS_FRAMES == 1):
              is_before_first = False
              cv2.imwrite("left.bmp",leftImage)
              cv2.imwrite("right.bmp",rightImage)


          displayMain(frame,cap)
          displayLeft(leftImage)
          displayRight(rightImage)


          # Press Q on keyboard to  exit
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break

          # Break the loop
      else:
        break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
        main()
