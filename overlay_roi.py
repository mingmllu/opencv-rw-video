import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--video_src", 
                    type=str, 
                    default = "", 
                    help = "path to video file")
parser.add_argument("--y1x1y2x2", 
                    type=str, 
                    default = '50,100,150,300', 
                    help = "Region of interest:y1,x1,y2,x2 (CSV)")

args = parser.parse_args()
video_file = args.video_src
y1,x1,y2,x2 = [int(v) for v in args.y1x1y2x2.split(',')]

# Create a VideoCapture object
cap = cv2.VideoCapture(video_file)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
  exit()

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

while(True):
  ret, frame = cap.read()
  if ret == True: 
    thickness = 2
    color = (0,255,0)
    pt1 = (x1,y1)
    pt2 = (x2,y2)
    cv2.rectangle(frame, pt1, pt2, color, thickness)
    # Display the resulting frame    
    cv2.imshow('Display live video while recording ... Type q to quit',frame)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
   #Break the loop
  else:
    break 

