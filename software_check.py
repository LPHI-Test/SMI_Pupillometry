"""
Intended for use by new collaborators
Checks that OpenCV, Python, and needed libraries are installed
Checks that OpenCV and Python versions are compatible with this project
"""
import sys
import pkg_resources

# constants
# change according to version
PYTHON_CHECK = "3.7"
CV_CHECK = "4.1"


def python_check():
    """checks if user's python version is compatible with project"""
    # check python version
    if PY_VERSION != PYTHON_CHECK:
        return False
    return True


def cv_check():
    """checks if user's OpenCV version is compatible with project"""
    # check OpenCV version
    if cvVersion != CV_CHECK:
        return False
    return True


def library_check():
    """checks if necessary libraries are installed"""
    # check for libraries
    required = {'matplotlib', 'numpy'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        return False

    return True

def not_lib_check():
    """prints missing libraries"""
    required = {'matplotlib', 'numpy'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    print("Error: missing modules ", missing)

def main():
    """if python and OpenCV are installed, checks versions and libraries"""
    if python_check() and cv_check() and library_check():
        print("Software Check: Passed")
    else:
        if not python_check():
            print("Error: using Python ", PY_VERSION)
            print("Install Python ", PYTHON_CHECK)
        if not cv_check():
            print("Error: using OpenCV ", cvVersion)
            print("Install OpenCV ", CV_CHECK)
        if not library_check():
            not_lib_check()


if __name__ == "__main__":

    # collects user versions
    PY_VERSION = sys.version[0:3]

    try:
        import cv2
        cvVersion = cv2.__version__[0:3]
    except ImportError:
        print("Error: cv2 not installed")
        if not python_check():
            print("Error: using Python ", PY_VERSION)
            print("Install Python ", PYTHON_CHECK)
        if not library_check():
            not_lib_check()
        sys.exit()

    main()
