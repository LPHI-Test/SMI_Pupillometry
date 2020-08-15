import sys
import pkg_resources

# constants
# change according to version
pythonCheck = "3.7"
cvCheck = "4.1"


def Python_Check():
    # check python version
    if(pyVersion != pythonCheck):
        return False
    return True


def CV_Check():
    # check OpenCV version
    if(cvVersion != cvCheck):
        return False
    return True


def Library_Check():
    # check for libraries
    required = {'matplotlib', 'numpy'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        return False

    return True

def notLibCheck():
    required = {'matplotlib', 'numpy'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    print("Error: missing modules ", missing)

def main():
    if(Python_Check() and CV_Check() and Library_Check()):
        print("Software Check: Passed")
    else:
        if(not Python_Check()):
            print("Error: using Python ", pyVersion)
            print("Install Python ", pythonCheck)
        if(not CV_Check()):
            print("Error: using OpenCV ", cvVersion)
            print("Install OpenCV ", cvCheck)
        if(not Library_Check()):
            notLibCheck()


if __name__ == "__main__":

    # collects user versions
    pyVersion = sys.version[0:3]

    try:
        import cv2
        cvVersion = cv2.__version__[0:3]
    except ImportError:
        print("Error: cv2 not installed")
        if(not Python_Check()):
            print("Error: using Python ", pyVersion)
            print("Install Python ", pythonCheck)
        if(not Library_Check()):
            notLibCheck()
        exit()

    main()
