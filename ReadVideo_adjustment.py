import cv2
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

window_size = 10
window_avg_delta = 40

cv = cv2.VideoCapture("video/No_Cali.mp4")
pv = cv2.VideoCapture("video/PV_Cali.mp4")
transmat = sio.loadmat('Scale_transfer.mat')  # read the transfer matrix
M = transmat['M']

# TODO get rid of this
# Fast forward to interesting part of the video
cv.set(1, 450)
pv.set(1, 450)

while(cv.isOpened() and pv.isOpened()):

    _, cv_frame = cv.read() # get the figure
    _, pv_frame = pv.read() # get the background

    print cv.get(1) #print frame No

    ## Transfer CV
    cv_frame = cv2.warpPerspective(cv_frame,M,(1920,1080))

    pv_np = np.array(pv_frame)
    cv_np = np.array(cv_frame)

    # get width and height for cv_np_edges
    cv_np_height, cv_np_width, _ = cv_np.shape

    # get starting pixel of every window
    start_y = 0
    start_x = 0

    extracted_subject = np.zeros((cv_np_height, cv_np_width, 3), np.uint8)

    for end_y in range(window_size, cv_np_height, window_size):
        for end_x in range(window_size, cv_np_width, window_size):

            cv_np_window = cv_np[start_y:end_y, start_x:end_x]
            pv_np_window = pv_np[start_y:end_y, start_x:end_x]

            cv_np_window_avg = np.average(cv_np_window)
            pv_np_window_avg = np.average(pv_np_window)

            #if abs(cv_np_window_avg - pv_np_window_avg) <= window_avg_delta:
            #    cv_np_window_avg = pv_np_window_avg

            if abs(cv_np_window_avg - pv_np_window_avg) > window_avg_delta:
                extracted_subject[start_y:end_y, start_x:end_x] = (0,0,255)
                cv_np[start_y:end_y, start_x:end_x] = (0,0,255)
                pv_np[start_y:end_y, start_x:end_x] = (0,0,255)

            start_x = end_x
        start_y = end_y

    if cv.get(1) == cv.get(7):
        break
    else:
        cv.set(1, (cv.get(1)+3))
        pv.set(1, (pv.get(1)+3))


cv.release()
pv.release()
cv2.destroyAllWindows()