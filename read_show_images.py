import os
import re
import cv2

subtree_path = '.'
ext_name = 'jpg'

def scan_image_files(subtree_path):
    list_images = []
    for (path, dirs, files) in os.walk(subtree_path):
        for file in files:
            if file.endswith(ext_name):
                list_images.append(file)
    return list_images

list_images = scan_image_files(subtree_path)

list_images_selected = []
for fname in list_images:
    img = cv2.imread(fname)
    cv2.imshow(fname, img)
    #your_decison = cv2.waitKey()
    #if your_decison == 1:
    if cv2.waitKey() & 0xFF == ord('y'):
        print(fname)
    else:
        cv2.destroyWindow(fname)
#cv2.destroyAllWindows()

