import os
import cv2
import argparse
import numpy as np

def fade_image_by_box(image, box, alpha=0.5):
  """
  Fade the image portion by given box
  Arguments:
    image: cv2 image in numpy array
    box: (x1,y1,x2,y2)
  Return:
    The faded image
  """
  x1,y1,x2,y2 = box
  sub_img = image[y1:y2, x1:x2, :].astype(np.uint32)*(1-alpha)
  image[y1:y2, x1:x2, :] = sub_img
  return image

def overlay_image_with_detection_result(raw_image, list_det):
  raw_image_uint8 = raw_image.astype(np.uint8)
  for i, obj in enumerate(list_det):
    x,y,w,h = obj
    # draw bbox
    y1, x1, y2, x2 = y,x,y+h,x+w
    _y1, _x1, _y2, _x2 = y1+3, x1+3, y2+3, x2+3
    thickness = 1
    color = (0,0,0)
    pt1 = (_x1,_y1)
    pt2 = (_x2,_y2)
    cv2.rectangle(raw_image_uint8, pt1, pt2, color, thickness) # shadow
    color = (5,211,156)  # apple green
    pt1 = (x1,y1)
    pt2 = (x2,y2)
    cv2.rectangle(raw_image_uint8, pt1, pt2, color, thickness)


    # Draw label
    opt_draw_label = True
    if opt_draw_label:
      label = str(i+1)
      font = cv2.FONT_HERSHEY_SIMPLEX
      fontScale = 1
      thickness = 1
      fontColor = (255,255,255)
      (W,H),m = cv2.getTextSize(label, font, fontScale, thickness)
      s = 3 # in pixels
      origin = (x1+m, max(y1-m-s, 0))
      bottomright = (x1+W+2*m, max(y1-s,0))
      topleft = (origin[0]-m, max(origin[1]-H-m-s,0))
      label_box = (topleft[0], topleft[1], bottomright[0], bottomright[1])
      fade_image_by_box(raw_image_uint8, label_box)
      cv2.putText(raw_image_uint8, label, origin, font, fontScale, fontColor, thickness)

  return raw_image_uint8

parser = argparse.ArgumentParser()

parser.add_argument("--path-to-video-clip", 
                    type=str, 
                    default = "", 
                    help = "Path to target MOT16 video clip")
parser.add_argument("--frame-number", 
                    type=int, 
                    default = 1, 
                    help = "The number of the frame of interest")

args = parser.parse_args()
path = args.path_to_video_clip
frame_number = args.frame_number

print("Read the CSV file ...")
input_file = open(os.path.join(path, 'det/det.txt'), 'r')
list_target_frame = []
for line in input_file:
  fn,_,x,y,w,h,_,_,_,_ = line.rstrip('\n').split(',')
  fn = int(fn)
  x,y,w,h = float(x),float(y),float(w),float(h)
  if fn == frame_number:
    list_target_frame.append([int(x),int(y),int(w),int(h)])
  elif fn > frame_number:
    break

print("Open and read image file ...")
im = cv2.imread(os.path.join(path, 'img1','%06d.jpg'%(frame_number)))
im = overlay_image_with_detection_result(im, list_target_frame)
window_title = path + ': Frame #{}'.format(frame_number)
cv2.namedWindow(window_title,cv2.WINDOW_NORMAL)
cv2.imshow(window_title, im)
cv2.waitKey(0)
cv2.destroyAllWindows()
