import cv2
import numpy as np

window_size = 20
window_avg_delta = 5

cv = cv2.VideoCapture("video/no_light_marked.mp4")
pv = cv2.VideoCapture("video/PV_calibrated.mp4")

## TODO don't include this
## fast-forward to interesting part of video for development
for i in range(200):
    cv.read()
    pv.read()

while(cv.isOpened() and pv.isOpened()):

    _, cv_frame = cv.read() # get the figure
    _, pv_frame = pv.read() # get the background

    """
    cv2.imshow('cv_frame', cv_frame)
    cv2.waitKey(1)
    cv2.imshow('pv_frame', pv_frame)
    cv2.waitKey(1)
    """

    print cv.get(1) #print frame No

    ## Edge detection here
    cv_edges = cv2.Canny(cv_frame,100,120)
    pv_edges = cv2.Canny(pv_frame,100,120)

    cv_np_edges = np.array(cv_edges)
    pv_np_edges = np.array(pv_edges)

    # get width and height for cv_np_edges
    cv_np_height = cv_np_edges.shape[0]
    cv_np_width = cv_np_edges.shape[1]

    # get starting pixel of every window in cv
    start_y = 0
    start_x = 0
    extracted_subject = np.zeros((cv_np_height,cv_np_width,3), np.uint8)
    for end_y in range(window_size, cv_np_height, window_size):
        for end_x in range(window_size, cv_np_width, window_size):
            cv_np_window = cv_np_edges[start_y:end_y, start_x:end_x]
            pv_np_window = pv_np_edges[start_y:end_y, start_x:end_x]
            cv_np_window_avg = np.average(cv_np_window)
            pv_np_window_avg = np.average(pv_np_window)

            if abs(cv_np_window_avg - pv_np_window_avg) > window_avg_delta:
                extracted_subject[start_y:end_y, start_x:end_x] = (0,0,255)

            start_x = end_x
        start_y = end_y

    cv2.imshow('extracted_subject', extracted_subject)
    cv2.waitKey(1)

    # get width and height for pv_np_edges
    pv_np_height = pv_np_edges.shape[0]
    pv_np_width = pv_np_edges.shape[1]

    #
    cv2.imshow('cv_edges', cv_edges)
    cv2.waitKey(1)
    cv2.imshow('pv_edges', pv_edges)
    cv2.waitKey(1)
    ##

    if cv.get(1) == cv.get(7):
        break


cv.release()
pv.release()
cv2.destroyAllWindows()