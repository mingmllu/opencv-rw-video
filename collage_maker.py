import os
import argparse
import math
import cv2
import numpy as np


parser = argparse.ArgumentParser()

parser.add_argument("--paths-to-images", 
                    type=str, 
                    required=True,
                    help = "CSV of paths to image files")
parser.add_argument("--image-suffix", 
                    type=str, 
                    default = '.jpg', 
                    help = "Image file suffix")
parser.add_argument("--tile-height", 
                    type=int, 
                    default = 256, 
                    help = "Tile height in pixels")
parser.add_argument("--tile-width", 
                    type=int, 
                    default = 128, 
                    help = "Tile width in pixels")
parser.add_argument("--keep-aspect-ratio", 
                    action='store_true',
                    help = "Whether or not keep image aspect ratio")
parser.add_argument("--num-columns", 
                    type=int, 
                    default = 12, 
                    help = "Number of columns for the standard tiles")
parser.add_argument("--max-num-rows", 
                    type=int, 
                    default = 6, 
                    help = "Max number of row for the standard tiles")
parser.add_argument("--caption", 
                    action='store_true',
                    help = "Add filename to image")
parser.add_argument("--output-filename", 
                    type=str, 
                    required=True,
                    help = "Output file name")


args = parser.parse_args()
list_paths = args.paths_to_images.split(',')
image_suffix = args.image_suffix
list_paths_to_files = []
for path in list_paths:
    if os.path.isdir(path):
        list_dir = os.listdir(path)
        list_dir.sort()
        for filename in list_dir:
            if filename.endswith(image_suffix):
                list_paths_to_files.append(os.path.join(path, filename))
    elif os.path.isfile(path):
        list_paths_to_files.append(path)
list_paths = list_paths_to_files

H = args.tile_height
W = args.tile_width
num_columns = args.num_columns
max_num_rows = args.max_num_rows
num_rows = int(math.ceil(len(list_paths)/float(num_columns)))
num_rows = min(num_rows, max_num_rows)
canvas_height = (H+2)*num_rows
canvas_width = (W+2)*num_columns
canvas = 255*np.ones((canvas_height, canvas_width, 3), dtype=np.uint8)

standard_tile_dim = (W,H)
idx_row = 0
idx_col = 0
for path in list_paths:
    if idx_row >= num_rows:
        break
    im = cv2.imread(path)
    if args.keep_aspect_ratio:
        pass
    else:
        im_resized = cv2.resize(im, standard_tile_dim, interpolation = cv2.INTER_AREA)
        if args.caption:
            im_name = os.path.splitext(os.path.basename(path))[0]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.8
            thickness = 2
            fontColor = (255,255,255)
            origin = (W//3, H//2)
            cv2.putText(im_resized, im_name, origin, font, fontScale, fontColor, thickness)
        y1, y2 = 2*idx_row + idx_row*H, 2*idx_row + (idx_row+1)*H
        x1, x2 = 2*idx_col + idx_col*W, 2*idx_col + (idx_col+1)*W
        canvas[y1:y2,x1:x2,:] = im_resized
        idx_col += 1
        if idx_col == num_columns:
            idx_col = 0
            idx_row += 1

cv2.imwrite(args.output_filename, canvas)


