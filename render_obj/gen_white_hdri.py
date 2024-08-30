import cv2
import numpy as np

width = 2048
height =1024

white_image = np.ones((height,width,3),dtype=np.float32)*0.5
hdr_image_path = r'C:\Users\bupty\Desktop\HDRI\hdri-87.hdr'
hdri_image = cv2.imread(hdr_image_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_ANYCOLOR)
new_hdri = hdri_image+white_image

cv2.imwrite(r"C:\Users\bupty\Desktop\HDRI\hdri-0.hdr",new_hdri)