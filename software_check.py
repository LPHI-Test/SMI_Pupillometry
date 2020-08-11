import sys
import pkg_resources

# constants
# change according to version
pythonCheck = "3.7"
cvCheck = "4.1"


def Python_Check():
    # check python version
    if(pyVersion != pythonCheck):
        print("Error: using Python ", pyVersion)
        print("Install Python ", pythonCheck)
        return False
    return True


def CV_Check():
    # check OpenCV version
    if(cvVersion != cvCheck):
        print("Error: using OpenCV ", cvVersion)
        print("Install OpenCV ", cvCheck)
        return False
    return True


def Library_Check():
    # check for libraries
    required = {'matplotlib', 'numpy'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("Error: missing modules ", missing)
        return False

    return True


def main():
    if(Python_Check()):
        if(CV_Check()):
            if(Library_Check()):
                print("Software Check: Passed")


if __name__ == "__main__":
    try:
        import cv2
        cvVersion = cv2.__version__[0:3]
    except ImportError:
        print("Error: cv2 not installed")

    # collects user versions
    pyVersion = sys.version[0:3]

    main()
