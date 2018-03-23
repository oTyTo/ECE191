## this program read in a projected image and captured image and detect oscar on the captured image
import cv2
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

#initiate sliding window parameters
window_size = 10
window_avg_delta = 65

# inputs
cv = cv2.imread('images/NoCV100.jpg')          # cv
pv = cv2.imread('images/PV100.jpg')        # pv
transmat = sio.loadmat('Geo_transfer.mat')  # read the transfer matrix

# Apply transfer matrix CV
cv_trans = cv2.warpPerspective(cv,transmat['M'],(1920,1080))
cv2.imwrite('TransferedCV.jpg',cv_trans)

#Sliding window detection
