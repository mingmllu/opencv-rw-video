import cv2
import numpy as np

# Create a VideoCapture object
#cap = cv2.VideoCapture('http://108.53.114.166/mjpg/video.mjpg')
cap = cv2.VideoCapture('http://root:fitecam@135.222.247.179:9107/mjpg/video.mjpg')

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
  exit()

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('video_h264_11_06_9107.avi',cv2.VideoWriter_fourcc('H', '2', '6', '4'), 10, (frame_width,frame_height))
# A counter for frames that have been written to the output file so far
n_frames = 0
# The maximum number of frames to be written
max_number_framed_to_be_saved = 100000000

while(True):
  ret, frame = cap.read()

  if ret == True: 
     
    # Write the frame into the file 'output.avi'
    out.write(frame)
    n_frames += 1
    print("Frame %d out of %d saved " % (n_frames, max_number_framed_to_be_saved))
    if n_frames == max_number_framed_to_be_saved:
      break
    # Display the resulting frame    
    cv2.imshow('Display live video while recording ... Type q to quit',frame)
 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break 

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 
