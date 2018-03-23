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

# Basic color correction
# TODO develop a more dynamic and exact color correction technique
# For now, decrease intensity of every RGB value by 10, arbitrarily
cv_trans = cv_trans - 10


pv_np = np.array(pv)
cv_np = np.array(cv_trans)
cv_np_height, cv_np_width, _ = cv_np.shape

#Sliding window detection
start_y = 0
start_x = 0

extracted_subject = np.zeros((cv_np_height, cv_np_width, 3), np.uint8)

for end_y in range(window_size, cv_np_height, window_size):
    for end_x in range(window_size, cv_np_width, window_size):

        cv_np_window = cv_np[start_y:end_y, start_x:end_x]
        pv_np_window = pv_np[start_y:end_y, start_x:end_x]

        cv_np_window_avg = np.average(cv_np_window)
        pv_np_window_avg = np.average(pv_np_window)

        if abs(cv_np_window_avg - pv_np_window_avg) > window_avg_delta:
            extracted_subject[start_y:end_y, start_x:end_x] = (0,0,255)
            cv_np[start_y:end_y, start_x:end_x] = (0,0,255)
            pv_np[start_y:end_y, start_x:end_x] = (0,0,255)

        start_x = end_x
    start_y = end_y
