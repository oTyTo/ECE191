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
    #cv2.imshow('transfercv', cv_frame)
    #cv2.waitKey(1)

    pv_np = np.array(pv_frame)
    cv_np = np.array(cv_frame)

    cv_np_height, cv_np_width, _ = cv_np.shape

    print "here1"
    extracted_subject = np.zeros((cv_np_height, cv_np_width, 3), np.uint8)
    for y in range(cv_np_height):
        print "here " + str(y)
        for x in range(cv_np_width):
            if np.average(cv_np[y,x]) != np.average(pv_np[y,x]):
                extracted_subject[y,x] = (0,0,255)

    print "here2"
    cv2.imshow('cv', cv_np)
    cv2.imshow('pv', pv_np)
    cv2.imshow('extracted', extracted_subject)
    cv2.waitKey(1)

    if cv.get(1) == cv.get(7):
        break
    else:
        cv.set(1, (cv.get(1)+3))
        pv.set(1, (pv.get(1)+3))

    continue

    print cv_np[0][0]
    #cv_np = cv_np * (1,1,.1)
    #cv_np = cv_np * .01
    cv_np = cv_np - 10
    #cv_np = cv_np - (10, 5, 5)
    #cv_np = cv_np - .5
    print cv_np[0][0]
    #cv2.imshow('cv_after_adjustment', cv_np)
    #cv2.waitKey(1)

    # get width and height for cv_np_edges

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

    #cv2.imshow('extracted_subject', extracted_subject)
    cv2.imshow('masked_cv', cv_np)
    #cv2.imshow('masked_pv', pv_np)
    cv2.waitKey(1)

    if cv.get(1) == cv.get(7):
        break
    else:
        cv.set(1, (cv.get(1)+3))
        pv.set(1, (pv.get(1)+3))


cv.release()
pv.release()
cv2.destroyAllWindows()