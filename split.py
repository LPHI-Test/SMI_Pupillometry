"""
Valentin Siderskiy 10/22/2019
Integrative Human Physiology Lab
Rutgers University

split.py
This function takes the video input recorded by the
Night Owel Security stystem, splits the left and right
and assigns a timestamp based on the night owel clock.
"""

import sys
import cv2
import matplotlib.pyplot as plt
from find_pupil import pupillometry
#text
FONT = cv2.FONT_HERSHEY_SIMPLEX
SMI_DIM = (720, 480) # Dimension from SMI System
DEFAULT_FILE_NAME = 'V1219_20850228_234726_Dilation2.mp4'


def plot_radial_perimeter(left_rads, left_radius, right_rads, right_radius):
    """plots radians over radius for the left and right eye"""
    plt.subplot(121)
    plt.clf()
    plt.subplot(122)
    plt.clf()

    plt.subplot(121)
    plt.ion()
    plt.axis([-4, 4, 35, 60])
    plt.plot(left_rads, left_radius, 'ro')
    plt.ylabel('left radius (pixels)')
    plt.xlabel('angle (radians)')
    plt.subplot(122)
    plt.ion()
    plt.axis([-4, 4, 35, 60])
    plt.plot(right_rads, right_radius, 'ro')
    plt.ylabel('right radius (pixels)')
    plt.xlabel('angle (radians)')
    plt.show()
    plt.pause(0.05)

def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """Resizes image to particular width or height but keeps aspect ratio"""
    dim = None
    (image_h, image_w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        ratio = height / float(image_h)
        dim = (int(image_w * ratio), height)
    else:
        ratio = width / float(image_w)
        dim = (width, int(image_h * ratio))

    return cv2.resize(image, dim, interpolation=inter)

def display_left(left):
    """ Display the Left Eye"""
    resized_left = resize_with_aspect_ratio(left, width=640) #Resize by\
    # pylint: disable=C0103
    L_STRING = "Left"
    cv2.putText(resized_left, L_STRING, (0, 20), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Left Eye', resized_left)
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)


def display_right(right):
    """Display the Right Eye"""
    resized_right = resize_with_aspect_ratio(right, width=640) #Resize by
    # pylint: disable=C0103
    R_STRING = "Right"
    cv2.putText(resized_right, R_STRING, (0, 20), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Right Eye', resized_right)
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

def display_main(frame, cap):
    """Display Main#"""
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    resized_frame = resize_with_aspect_ratio(frame, width=640) #Resize by
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

    frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fp_string = "Frame " + str(frame_position) + '/' + str(fcount)
    cv2.putText(resized_frame, fp_string, (230, 350), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    # pylint: disable=C0103
    QUIT_STRING = "Press Q to Quit"
    cv2.putText(resized_frame, QUIT_STRING, (230, 250), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Frame', resized_frame)

# pylint: disable=W0613
def get_time(frame, timestamp):
    """Get time from Night Owel security syste use OCT
    Input: frame
    Output: time"""
    print("time")

def main(frame=-1, filename=DEFAULT_FILE_NAME):
    """#input frame: -1, the whole file, else a particular frame"""
    if int(framenum) == -1:
        debug = 0
    else:
        debug = 3

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(filename)

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    is_before_first = True

    print("WIDTH: ", frame_w)
    print("HEIGHT: ", frame_h)
    print("FPS: ", fps)
    print("FCOUNT: ", fcount)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")

    #   Read until video is completed
    while cap.isOpened():
      # Capture frame-by-frame

        if int(framenum) != -1:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(framenum)-1)

        ret, frame = cap.read()

        if ret:

            print(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if framenum == -1 or int(framenum) == int(cap.get(cv2.CAP_PROP_POS_FRAMES)):
                #get_time(frame,timestamp)
                left_image_owl = frame[10:int(frame_h/2), 1:int(frame_w/2)]
                right_imag_owl = frame[10:int(frame_h/2), int(frame_w/2+1):frame_w]

                left_image = cv2.resize(left_image_owl, SMI_DIM, interpolation=cv2.INTER_AREA)
                right_image = cv2.resize(right_imag_owl, SMI_DIM, interpolation=cv2.INTER_AREA)

                if debug > 0:
                    print("Left Size: ", left_image.shape)
                    print("Right Size: ", left_image.shape)


              #save nth frame to a file
                if framenum == -1:
                    if(is_before_first and cap.get(cv2.CAP_PROP_POS_FRAMES) == 45):
                        is_before_first = False
                        cv2.imwrite("left.bmp", left_image)
                        cv2.imwrite("right.bmp", right_image)
                else:
                    if(is_before_first and cap.get(cv2.CAP_PROP_POS_FRAMES) == framenum):
                        is_before_first = False
                        cv2.imwrite("left.bmp", left_image)
                        cv2.imwrite("right.bmp", right_image)


                left_image_edit, left_rads, left_radius = pupillometry(left_image, debug)
                right_image_edit, right_rads, right_radius = pupillometry(right_image, debug)

                display_main(frame, cap)
                display_left(left_image_edit)
                display_right(right_image_edit)
                plot_radial_perimeter(left_rads, left_radius, right_rads, right_radius)

                # Press Q on keyboard to  exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

              # Break the loop
        else:
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == int(framenum):
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) > 1 :
        if len(sys.argv) == 2:
            framenum = int(sys.argv[1])
            filename = DEFAULT_FILE_NAME
        if len(sys.argv) == 3:
            framenum = int(sys.argv[1])
            filename = sys.argv[2]
    else:
        framenum = -1
        filename = DEFAULT_FILE_NAME
    print("Frame Number: ", framenum)
    print("File Name", filename)
    main(framenum, filename)
