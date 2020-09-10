import os
import cv2
import numpy as np


LAB_TARGET_MEAN = os.getenv('LAB_TARGET_MEAN', '80.0:135.0:128.0')
LAB_TARGET_MEAN = LAB_TARGET_MEAN.strip().split(':')
LAB_TARGET_MEAN = [float(v) for v in LAB_TARGET_MEAN]
LAB_TARGET_STDDEV = os.getenv('LAB_TARGET_STDDEV', '40.0:20.0:10.0')
LAB_TARGET_STDDEV = LAB_TARGET_STDDEV.strip().split(':')
LAB_TARGET_STDDEV = [float(v) for v in LAB_TARGET_STDDEV]


def convert_color_bgr2gray(img_bgr):
  gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
  return gray

def convert_color_bgr2lab(bgr):
  """  
  Convert BGR images to L*A*B images
  """
  lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
  return lab

def convert_color_lab2bgr(lab):
  """  
  Convert L*A*B images to BGR images
  """
  bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
  return bgr

def eval_lab_color_stats(img_lab):
  """
  Calculate color statistics in the L*A*B space:
  """
  std = np.std(img_lab, axis=(0,1))
  mean = np.mean(img_lab, axis=(0,1))
  return (mean, std)

def transfer_color(img_lab, src_mean, src_std, target_mean, target_std):
  """
  Color transfer 
  """
  scale = np.divide(target_std, src_std)
  img_lab_float32 = img_lab.astype(np.float32)
  img_lab_float32 = np.multiply(img_lab_float32-src_mean, scale) + target_mean
  img_lab_float32 = np.clip(img_lab_float32, 0, 255)
  return img_lab_float32.astype(np.uint8)

def transfer_to_default_color(img_bgr):
  img_lab = convert_color_bgr2lab(img_bgr)
  src_mean, src_std = eval_lab_color_stats(img_lab)
  img_lab_transferred = transfer_color(img_lab, src_mean, src_std, LAB_TARGET_MEAN, LAB_TARGET_STDDEV)
  img_bgr_transferred = convert_color_lab2bgr(img_lab_transferred)
  return img_bgr_transferred

def equalize_histogram(image, mask=None):
  """
  If mask is not None, just correct the masked pixels
  """
  img = image.astype(np.uint8)
  if mask is None:
    img[:,:,0] = cv2.equalizeHist(img[:,:,0])
    img[:,:,1] = cv2.equalizeHist(img[:,:,1])
    img[:,:,2] = cv2.equalizeHist(img[:,:,2])
  else:
    mask_indexes = np.where(mask==1)
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    _b = cv2.equalizeHist(b[mask_indexes].reshape(-1,1))
    _g = cv2.equalizeHist(g[mask_indexes].reshape(-1,1))
    _r = cv2.equalizeHist(r[mask_indexes].reshape(-1,1))
    b[mask_indexes], g[mask_indexes], r[mask_indexes] = _b[:,0], _g[:,0], _r[:,0]
    img = np.stack([b,g,r], axis=2)
  return img

"""
img_bgr = img_manipulate.convert_color_bgr2gray(image)
img_bgr = img_manipulate.transfer_to_default_color(image)
img_bgr = img_manipulate.equalize_histogram(image)
"""