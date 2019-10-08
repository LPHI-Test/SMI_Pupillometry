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

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
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

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    timestamp = time.clock()

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

          getTime(frame,timestamp)

          resized_frame = ResizeWithAspectRatio(frame, width = 640) #Resize by
          # resized_frame = ResizeWithAspectRatio(frame, height = 480)

          # Display the resulting frame
          cv2.imshow('Frame',resized_frame)

          # Press Q on keyboard to  exit
          if cv2.waitKey(25) & 0xFF == ord('q'):
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
