import cv2
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

import MatchImage

window_size = 10
window_avg_delta = 15

cv = cv2.VideoCapture("video/FML.mp4")
pv = cv2.VideoCapture("video/F_PV.mp4")
transmat = sio.loadmat('Scale_transfer.mat')  # read the transfer matrix

# TODO don't include this
# fast-forward to interesting part of video for development
"""
for i in range(306):
    cv.read()
    pv.read()
"""

while(cv.isOpened() and pv.isOpened()):

    _, cv_frame = cv.read() # get the figure
    _, pv_frame = pv.read() # get the background

    ## use the frist frame to calculate transfer matrix
    if cv.get(1) == 1.0:
        print 'Calculating Transfer Matrix'
        M= MatchImage.matchimage(cv_frame, pv_frame)
        

    cv2.imshow('cv_frame', cv_frame)
    cv2.waitKey(1)
    cv2.imshow('pv_frame', pv_frame)
    cv2.waitKey(1)

     ## Transfer CV
    cv_trans = cv2.warpPerspective(cv_frame,M,(1920,1080))
    cv2.imshow('transfercv', cv_trans)
    cv2.waitKey(1)
    print cv.get(1) #print frame No

    ##find threshold
    if cv.get(1) == 1.0:
        threshb = np.amin(cv_trans[10:1070,10:1910,0])
        threshg = np.amin(cv_trans[10:1070,10:1910,1])
        threshr = np.amin(cv_trans[10:1070,10:1910,2])

    #apply thresholding
    threshCV = np.empty([1080,1920,3])
    _, threshCV[:,:,0] = cv2.threshold(cv_trans[:,:,0],threshb,255,cv2.THRESH_TOZERO_INV)
    _, threshCV[:,:,1] = cv2.threshold(cv_trans[:,:,1],threshg,255,cv2.THRESH_TOZERO_INV)
    _, threshCV[:,:,2] = cv2.threshold(cv_trans[:,:,2],threshr,255,cv2.THRESH_TOZERO_INV)
    cv2.imshow('CVthresh', threshCV)
    cv2.waitKey(1)
    #create binary mask
    threshCV = np.empty([1080,1920,3])
    _, threshCV[:,:,0] = cv2.threshold(cv_trans[:,:,0],threshb,255,cv2.THRESH_BINARY_INV)
    _, threshCV[:,:,1] = cv2.threshold(cv_trans[:,:,1],threshg,255,cv2.THRESH_BINARY_INV)
    _, threshCV[:,:,2] = cv2.threshold(cv_trans[:,:,2],threshr,255,cv2.THRESH_BINARY_INV)
    CV_result = threshCV[:,:,0]+threshCV[:,:,1]+threshCV[:,:,2]
    CV_result[CV_result>0] = 1 
    cv2.imshow('mask', CV_result)
    cv2.waitKey(1)
    
    #post processing, fill up holes
    





    # # only run once every three frames
    # if (cv.get(1) % 3) != 0:
    #     continue

    

    # ## Edge detection here
    # cv_edges = cv2.Canny(cv_frame,50,60)
    # pv_edges = cv2.Canny(pv_frame,50,60)

    # cv_np_edges = np.array(cv_edges)
    # pv_np_edges = np.array(pv_edges)

    # # get width and height for cv_np_edges
    # cv_np_height = cv_np_edges.shape[0]
    # cv_np_width = cv_np_edges.shape[1]

    # # get starting pixel of every window in cv
    # start_y = 0
    # start_x = 0
    # extracted_subject = np.zeros((cv_np_height,cv_np_width,3), np.uint8)
    # for end_y in range(window_size, cv_np_height, window_size):
    #     for end_x in range(window_size, cv_np_width, window_size):
    #         cv_np_window = cv_np_edges[start_y:end_y, start_x:end_x]
    #         pv_np_window = pv_np_edges[start_y:end_y, start_x:end_x]
    #         cv_np_window_avg = np.average(cv_np_window)
    #         pv_np_window_avg = np.average(pv_np_window)

    #         if abs(cv_np_window_avg - pv_np_window_avg) > window_avg_delta:
    #             extracted_subject[start_y:end_y, start_x:end_x] = (0,0,255)

    #         start_x = end_x
    #     start_y = end_y

    # cv2.imshow('extracted_subject', extracted_subject)
    # cv2.waitKey(0)

    # # get width and height for pv_np_edges
    # pv_np_height = pv_np_edges.shape[0]
    # pv_np_width = pv_np_edges.shape[1]

    # #
    # cv2.imshow('cv_edges', cv_edges)
    # cv2.waitKey(1)
    # cv2.imshow('pv_edges', pv_edges)
    # cv2.waitKey(1)
    ##

    if cv.get(1) == cv.get(7):
        break


cv.release()
pv.release()
cv2.destroyAllWindows()