import Calibration
import cv2
import matplotlib.pyplot as plt

cv = cv2.imread('CV_Grid_no_cursor.jpg')
pv = cv2.imread('PV_Grid.jpg')

for i in range(1):
    M, distance = Calibration.calibrate(cv, pv)
    print i
    print distance
    cv_warped = cv2.warpPerspective(cv,M,(1920,1080))
    cv2.imshow("cv_warped", cv_warped)
    cv2.waitKey(1)
    
"""

cv = cv2.VideoCapture("video/No_Cali.mp4")
pv = cv2.VideoCapture("video/PV_Cali.mp4")

for i in range(77):
    cv.read()
    pv.read()

_, img1 = cv.read()
_, img2 = pv.read()

cv2.imshow('pv', img2)
cv2.waitKey(1)

for i in range(1):
    M, distance = Calibration.calibrate(img1, img2)
    print i
    print distance
    img1 = cv2.warpPerspective(img1, M, (1920, 1080))
    cv2.imshow("transfercv", img1)
    cv2.waitKey(1)

"""
