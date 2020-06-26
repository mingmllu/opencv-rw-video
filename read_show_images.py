import os
import re
import cv2
import argparse

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

args = parser.parse_args()
subtree_path = args.path
ext_name = args.type
check_before_saving = True if args.check!='No' else False

def scan_image_files(subtree_path):
    list_images = []
    for (path, dirs, files) in os.walk(subtree_path):
        for file in files:
            if file.endswith(ext_name):
                list_images.append(os.path.join(path, file))
    list_images.sort()
    return list_images

list_images = scan_image_files(subtree_path)

list_images_selected = []
for fname in list_images:
    img = cv2.imread(fname)
    print("Image file name:", fname)
    if check_before_saving:
        cv2.imshow(fname, img)
        if cv2.waitKey() & 0xFF == ord('y'):
            list_images_selected.append(img)
        elif cv2.waitKey() & 0xFF == ord('e'):
            break
        cv2.destroyAllWindows()
    else:
        list_images_selected.append(img)

if list_images_selected:
    H,W,_=list_images_selected[0].shape
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    fps = args.fps
    output_filename = args.output_filename
    out = cv2.VideoWriter(output_filename+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (W,H))
    for img in list_images_selected:
        out.write(img)

