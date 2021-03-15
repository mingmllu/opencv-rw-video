import os
import re
import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--path", 
                    type=str, 
                    default = ".", 
                    help = "path to image files")
parser.add_argument("--type", 
                    type=str, 
                    default = 'jpg', 
                    help = "extension name of image files")
parser.add_argument("--output_filename", 
                    type=str, 
                    default = 'video', 
                    help = "output video file name")
parser.add_argument("--fps", 
                    type=float, 
                    default = 1, 
                    help = "frames per second")
parser.add_argument("--check", 
                    type=str, 
                    default = 'No', 
                    help = "check before saving: Yes or No")
parser.add_argument("--repetitions", 
                    type=int, 
                    default = 1, 
                    help = "times each images repaeted")
parser.add_argument("--resolution", 
                    type=str, 
                    default = '720x1280', 
                    help = "Video resolution, e.g., 720x1280")
parser.add_argument("--embed_image", 
                    type=str, 
                    default = 'No', 
                    help = "Embed source image in a blank frame")

def overlay_image_with_text(raw_image, text, origin=None):
  raw_image_uint8 = raw_image.astype(np.uint8)
  img_heigth, img_width, _ = raw_image_uint8.shape
  font = cv2.FONT_HERSHEY_SIMPLEX
  fontScale = 1
  thickness = 2
  fontColor = (0,255,255)
  (W,H),m = cv2.getTextSize(text, font, fontScale, thickness)
  if origin is None:
    origin = (0, H)
  cv2.putText(raw_image_uint8, text, origin, font, fontScale, fontColor, thickness)
  return raw_image_uint8

args = parser.parse_args()
subtree_path = args.path
ext_name = args.type
check_before_saving = True if args.check!='No' else False
resolution = args.resolution.split('x')
embed_image = True if args.embed_image=='Yes' else False
if len(resolution) == 2:
  H, W = resolution
  H, W = int(H), int(W)
else:
  H, W = 0, 0

def scan_image_files(subtree_path):
    list_images = []
    for (path, dirs, files) in os.walk(subtree_path):
        for file in files:
            if file.endswith(ext_name) and path == subtree_path:
                list_images.append(os.path.join(path, file))
    list_images.sort()
    return list_images

list_images = scan_image_files(subtree_path)
list_images_selected = []
if list_images:
  if H == 0 or W == 0:
    img = cv2.imread(list_images[0])
    H, W, _ = img.shape
for fname in list_images:
    img = cv2.imread(fname)
    img = cv2.resize(img, (W,H), interpolation = cv2.INTER_AREA)
    print("Image file name:", fname)
    if check_before_saving:
        cv2.imshow(fname, img)
        if cv2.waitKey() & 0xFF == ord('y'):
            list_images_selected.append(fname)
        elif cv2.waitKey() & 0xFF == ord('e'):
            break
        cv2.destroyAllWindows()
    else:
        list_images_selected.append(fname)

if list_images_selected:
    # Define the codec and create VideoWriter object.The output is stored in 'output_filename.avi'.
    fps = args.fps
    output_filename = args.output_filename
    out = cv2.VideoWriter(output_filename+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (W,H))
    frame_seqno = -1
    for fname in list_images_selected:
        img = cv2.imread(fname)
        frame_seqno += 1
        if embed_image and img.shape[0] <= H and img.shape[1] <= W:
            blank = 0*np.ones((H,W,3),dtype=np.uint8)
            h, w, _ = img.shape
            y,x = H//2 - h//2, W//2 - w//2
            blank[y:(y+h),x:(x+w),:] = img
            img = blank
        else:
            img = cv2.resize(img, (W,H), interpolation = cv2.INTER_AREA)
            #img = cv2.resize(img, (W,H), interpolation = cv2.INTER_AREA)
        img = overlay_image_with_text(img, str(frame_seqno))
        out.write(img)
        for i in range(args.repetitions-1):
            out.write(img)

