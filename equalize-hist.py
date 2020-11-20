import cv2
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument("--video_src", 
                    type=str, 
                    default = "", 
                    help = "path to video file")

args = parser.parse_args()
video_file = args.video_src
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

# A counter for frames that have been written to the output file so far
n_frames = 0

while(True):
  ret, frame = cap.read()
  if ret == True: 
    n_frames += 1
    print("Frame %d" % (n_frames))
    # Display the resulting frame    
    cv2.imshow('Original ... Type q to quit',frame)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    ts = time.time()
    frame[:,:,0] = cv2.equalizeHist(frame[:,:,0])
    frame[:,:,1] = cv2.equalizeHist(frame[:,:,1])
    frame[:,:,2] = cv2.equalizeHist(frame[:,:,2])
    print("---------------------------------------Elapsed time", time.time()-ts)
    cv2.imwrite('frame_%05d.jpg'%(n_frames), frame)
    # Display the resulting frame    
    cv2.imshow('Equalize Hist ... Type q to quit',frame)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

   #Break the loop
  else:
    break 

