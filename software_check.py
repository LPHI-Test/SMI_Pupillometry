import cv2
import sys
import subprocess
import pkg_resources

pyVersion = sys.version[0:5]
cvVersion = cv2.__version__

# check python version
if(pyVersion != "3.7.4"):
        print("Error: using Python ", pyVersion)
        print("Install Python 3.7.4")

# check OpenCV version
if(cvVersion != "4.1.1"):
    print("Error: using OpenCV ", cvVersion)
    print("Install OpenCV 4.1.1")

# check for libraries
required = {'math', 'matplotlib', 'numpy'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Error: missing modules ", missing)

exit()
