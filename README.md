# opencv-rw-video
Read, write (particularly H.264 encoding) and display video using OpenCV

See https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/

## Install opencv-python package that does not support H.264
Prerequisites

Create a virtualevn:
```
$ virtualenv --python=python3.6 _venv3.6
```
Activate the virtual environment:
```
$ source _venv3.6/bin/activate
```

```
(_venv3.6) ... $ pip install matplotlib

(_venv3.6) ... $ pip install numpy

(_venv3.6) ... $ pip install opencv-python
```

Now you can play with "read-display.py" and "read-write-mjpg-display.py":
```
(_venv3.6) ... $ python read-write-mjpg-display.py
```
## Install OpenCV that supports H.264
Unfortunately H.264 is not supported by opencv-python package installed via "pip install" due to license issue (see https://github.com/skvark/opencv-python/issues/81). So we have to compile OpenCV manually to get support for H.264 encoding.

The shell script "install_opencv4_ubuntu16.sh" is taken from "https://www.learnopencv.com/install-opencv-4-on-ubuntu-16-04/". First, install CMake and then run the script "install_opencv4_ubuntu16.sh" to install Open-CV:
```
$ sudo apt install cmake

$ ./install_opencv4_ubuntu16.sh
```
Select 1 to install OpenCV 3.4.1 (this version has been tested and works well). Once the installation is completed, run the following commands:
```
$ source ~/.bashrc

$ workon OpenCV-3.4.1-py3
```
Then you will enter the virtual environment (OpenCV-3.4.1-py3). Now you can run "read-write-h264-display.py" to generate H.264 video titled "video_h264.avi":
```
$ python read-write-h264-display.py
```
You can re-run the script "read-write-mjpg-display.py" to generate the MJPG video titled "video_mjpg.avi":
```
$ python read-write-mjpg-display.py
```
> If the script is running but you can't find the output file, probably this is because the CV2 package does not support H.264.

You may compare the file sizes between "video_mjpg.avi" and "video_h264.avi". The size of the H.264 video is much smaller!

To play the videos from the command line, you can install mplayer:
```
$ sudo apt update
$ sudo apt install mplayer
```
Then run
```
$ mplayer video_h264.avi
$ mplayer video_mjpg.avi
```
