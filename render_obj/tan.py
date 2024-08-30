"""写入均匀的6个视角"""
import numpy as np
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2

img = cv2.imread(r'C:\Users\bupty\Desktop\code\render_obj\result\hdr\chicken_bg_train\3\depth1.exr',cv2.IMREAD_UNCHANGED)
print(img)