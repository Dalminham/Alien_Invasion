import cv2 
import numpy as np
from PIL import Image

img = cv2.imread('mario.bmp')

#尺寸
rows, cols, channels =img.shape
print(f"rows {rows},cols {cols},channels {channels}")

#缩放
img2 = cv2.resize(img, None, fx = 0.5, fy =0.5)
rows2, cols2, channels2 =img2.shape
print(f"\nrows {rows2},cols {cols2},channels {channels2}")
img_bk = cv2.imread('new_plane.png')
"""for i in range(171): 
    for j in range(139): 
        if img_bk[i,j][0] == 112 and img_bk[i,j][1] == 174 and img_bk[i,j][2] == 228:
            img_bk[i,j] = (255,255,255)"""
img_bk = cv2.resize(img_bk,(80,80))
cv2.imwrite('./new_palyer.png',img_bk)
cv2.imshow('mario',img_bk)
cv2.waitKey(0)

#取背景色像素
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#二值化处理 
lower_blue = np.array([20,20,20])
upper_blue = np.array([200,200,200])

mask_tmp = cv2.inRange(hsv, lower_blue, upper_blue)



