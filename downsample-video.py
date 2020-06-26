import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--video_src", 
                    type=str, 
                    default = "", 
                    help = "path to video file")
parser.add_argument("--target_fps", 
                    type=float, 
                    default = 10, 
                    help = "Target video FPS")
parser.add_argument("--output_video", 
                    type=str, 
                    default = "output_video", 
                    help = "Output video file name")

args = parser.parse_args()

video_file = args.video_src
target_fps = args.target_fps
output_filename = args.output_video

# Create a VideoCapture object
cap = cv2.VideoCapture(video_file)
source_fps = cap.get(cv2.CAP_PROP_FPS)
print("Source FPS", source_fps)

if target_fps >= source_fps:
  exit()

decimation_factor = int(source_fps/target_fps)
target_fps = source_fps/decimation_factor

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
  exit()

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter(output_filename+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), target_fps, (frame_width,frame_height))

n_frames = 0

while(True):
  ret, frame = cap.read()
  if not ret:
    break
  n_frames += 1
  if (n_frames-1) % decimation_factor != 0:
    continue
  # Write the frame into the file 'output.avi'
  out.write(frame)
  print("Frame %d" % (n_frames))
  # Display the resulting frame    
  cv2.imshow('Display live video while recording ... Type q to quit',frame)
  # Press Q on keyboard to stop recording
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 
