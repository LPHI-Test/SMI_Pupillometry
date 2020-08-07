import cv2
import sys
import subprocess
import pkg_resources

# collects user versions
pyVersion = sys.version[0:5]
cvVersion = cv2.__version__

# constants
# change according to version
pythonCheck = "3.7.4"
cvCheck = "4.1.1"

# check python version
if(pyVersion != pythonCheck):
        print("Error: using Python ", pyVersion)
        print("Install Python ", pythonCheck)

# check OpenCV version
if(cvVersion != cvCheck):
    print("Error: using OpenCV ", cvVersion)
    print("Install OpenCV ", cvCheck)

# check for libraries
required = {'math', 'matplotlib', 'numpy'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Error: missing modules ", missing)

exit()
