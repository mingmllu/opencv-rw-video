import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--video_src", 
                    type=str, 
                    default = "", 
                    help = "path to video file")
parser.add_argument("--resize", 
                    type=float, 
                    default = 1, 
                    help = "Downsize factor to get full view")

args = parser.parse_args()

video_file = args.video_src
resize = args.resize

# Create a VideoCapture object
cap = cv2.VideoCapture(video_file)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
  exit()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
ret, frame = cap.read()
if ret:
    frame=cv2.resize(frame, (0,0), fx=resize, fy=resize)
    roi = cv2.selectROI(frame, False)
    print("Resolution: H %d, W %d" %(frame_height, frame_width))
    x, y, w, h = roi
    x, y = int(x/resize),int(y/resize)
    w, h = int(w/resize), int(h/resize)
    print("Selected ROI (x, y, w, h):", roi)
    print("Selected ROI (y1, x1, y2, x2):", (y, x, y + h, x + w))
else:
    print("Failed to read the video!")

    