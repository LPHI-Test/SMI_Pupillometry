# SMI_Pupillometry
Pupillometry using the SMI setup in the lab

## Software Setup
* Python 3.7.4
* OpenCV 4.1.1
* matplotlib

## Hardware Setup:

![Hardware Setup](https://github.com/LPHI-Test/SMI_Pupillometry/blob/master/Images/Hardware%20Setup.jpg)

Each channel (2 channels) of the SMI system output (composite video) is connected to a HD Flow Pro Wireless MultiMedia Kit.  The output (composite video) of the HD Flow device is connected to a Night Owl L-DVR4 system.  The two composite video signals are combined in the Night Owl system.  The output (HDMI 1080P) of the Night Owl system is connected to a Evolve HDML Cloner Box which records the video on a USB thumb drive.

### SMI:
* None.

### HD FLOW:
* None.

### Night Owl:
* Menu -> Output -> VGA/HDMI Resolution: 1080p.
* Left Eye Ch 1.
* Right Eye Ch 2.
* Configure NTP Time: Menu -> System -> General  -> Configure Date and Time.
* Menu -> Live -> Show time -> Enable

### Evolve HDML Cloner Box:
* Configure for 1080p setup. (button on remote)
* Configure for 4:3 ratio setup. (button on remote)
* Configure for BitRate Unlimited 16M. (button on remote)

# IDE Setup
- Atom w/ packages (optional)
  - autocomplete-python
  - kite
  - linter-pylint

# Software Instructions

## split.py
- function: Takes video from NightOwl System, splits the left and right channels, and runs pupillometry script on each frame. Provides visualization of pupillometry performance.
- Run:
```
python split.py
```
- or
```
python split.py [frame_number] [file_name]
```
- frame_number - allows to analyze just one frame in full debug mode, -1 for all frames.
- file_name - select the source file if not default
### Ex1:
```
python split.py -1 .\SMI_Pupilometry_Test.mp4
```
### Ex2:
```
python split.py 20 .\SMI_Pupilometry_Test.mp4
```
## find_pupil.py
- function: takes in a pupil image and finds the center and contour.
```
python find_pupil.py [methond] [file_name]
```
- methond 1 = V.S., methond 2 = ZH
