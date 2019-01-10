import cv2
import numpy as np
import time

# Create a VideoCapture object
#cap = cv2.VideoCapture('http://108.53.114.166/mjpg/video.mjpg')
#cap = cv2.VideoCapture('http://anomaly:lucent@135.104.127.10:58117/mjpg/video.mjpg') # Caffe
cap = cv2.VideoCapture('http://root:fitecam@135.222.247.179:9122/mjpg/video.mjpg') # Kiosk

fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
  exit()

# A counter for frames that have been written to the output file so far
n_frames = 0
# The maximum number of frames to be written
max_number_framed_to_be_read = 100
start_time = time.time()
while(True):
  ret, frame = cap.read()
  if ret == True: 
    n_frames += 1
    print("Frame %d out of %d read " % (n_frames, max_number_framed_to_be_read))
    if n_frames == max_number_framed_to_be_read:
      break

  # Break the loop
  else:
    break 
total_time = time.time() - start_time
print("frame rate = %f"%(n_frames / total_time))
# When everything done, release the video capture and video write objects
cap.release()