import sys
import numpy as np
import cv2
from find_pupil import rank_pFilter

defaultFileName = "right.bmp"
L_RANK_FILTER_DEFAULT = 7
p_RANK_FILTER_DEFAULT = 2

def main(filename,L,p):
    img = cv2.imread(filename)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    lp_imgray = rank_pFilter(imgray,L,p)
    cv2.imshow('gray',imgray)
    cv2.imshow('lp_imgray',lp_imgray)
    cv2.waitKey(0)

if __name__ == "__main__":
    print(len(sys.argv))
    if(len(sys.argv) > 1):
        if(len(sys.argv) == 2):
            filename = sys.argv[1]
            L = L_RANK_FILTER_DEFAULT
            p = p_RANK_FILTER_DEFAULT
        if(len(sys.argv) == 3):
            filename = sys.argv[1]
            L = int(sys.argv[2])
            p = p_RANK_FILTER_DEFAULT
        if(len(sys.argv) == 4):
            filename = sys.argv[1]
            L = int(sys.argv[2])
            p = int(sys.argv[3])
    else:
        filename = defaultFileName
        L = L_RANK_FILTER_DEFAULT
        p = p_RANK_FILTER_DEFAULT
    print("File Name",filename)
    main(filename, L, p)
