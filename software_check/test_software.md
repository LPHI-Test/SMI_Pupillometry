# Use virtual environments to recreate test conditions

## Using macOS Terminal and pip
module venv is included in the standard library for python3
virtualenv must be installed in order to test different Python versions

### Shell Commands to Install virtualenv:
Run:
> python3 -m pip install --user virtualenv

### Shell Commands to Create and Activate Virtual Environments
> python3 -m venv /path/to/new/virtual/environment
> source environment_name/bin/Activate

### Shell Commands to Install modules using pip
#### OpenCV
> pip install opencv-python==[version_number]

or, to view list of versions available for installation
>pip install opencv-python==

#### Libraries
> pip install matplotlib
> pip install numpy

Check all installed packages:
>pip list

### Shell Commands to Check Current versions
#### Python
>python -V

or
>python --version

#### OpenCV
Run:
>python
import cv2
cv2.__version__
exit()

### Shell Commands to Change Python Version
1. Start new virtual environment session
2. Install virtualenv (see line 7-8)
3. Run
>virtualenv --python=/usr/bin/python<version_number> environment_name

or
>python -m virtualenv --python=/usr/bin/python<version_number> environment_name

4.
> source environment_name/bin/activate

### Shell Commands to Change OpenCV Version
>pip uninstall opencv-python
>pip install opencv-python==<version_number>

### Shell Commands to Run software_check.py
>cd /path/to/software_check_folder
python software_check.py
