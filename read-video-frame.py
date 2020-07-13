import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--video_src", 
                    type=str, 
                    default = "", 
                    help = "path to video file")
parser.add_argument("--start_frame_no", 
                    type=int, 
                    default = 1, 
                    help = "start frame number")
parser.add_argument("--max_frames", 
                    type=int, 
                    default = -1, 
                    help = "maximum number of frames to be read")
parser.add_argument("--stride", 
                    type=int, 
                    default = 1, 
                    help = "sampling interval")
parser.add_argument("--skip_frames", 
                    type=int, 
                    default = 0, 
                    help = "The number of frames to be dropped")

args = parser.parse_args()

video_file = args.video_src

stride = args.stride

skip_frames = args.skip_frames

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
n_frames = args.start_frame_no-1
# The maximum number of frames to be written
max_number_framed_to_be_read = args.max_frames

while(True):
  ret, frame = cap.read()

  if ret == True: 

    n_frames += 1

    if n_frames % stride != 0:
      continue

    print("Frame %d out of %d read " % (n_frames, max_number_framed_to_be_read))
    if n_frames >= skip_frames:
      cv2.imwrite('frame_%06d.jpg'%(n_frames), frame)
    if n_frames == max_number_framed_to_be_read:
      break
    
    # Display the resulting frame    
    cv2.imshow('Display live video while recording ... Type q to quit',frame)
 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

   #Break the loop
  else:
    break 

