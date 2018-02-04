import cv2
import numpy as np


cap = cv2.VideoCapture("video\NoLightFigure.mp4")
rec = cv2.VideoCapture("video\NoLightBase.mp4")
while(cap.isOpened()):
    a, frame = cap.read() # get the figure
    b, back  = rec.read() # get the background
    cv2.imshow('frame', frame) 
    cv2.waitKey(1)
    cv2.imshow('back', back) 
    cv2.waitKey(1)
    print cap.get(1) #print frame No

    ## Edge detection here
    edges_f = cv2.Canny(frame,100,120)
    edges_b = cv2.Canny(back,100,120)
    edges = edges_f - edges_b
    cv2.imshow('edge_f', edges_f)
    cv2.waitKey(1)
    cv2.imshow('edge_b', edges_b)
    cv2.waitKey(1)
    cv2.imshow('edges', edges)
    cv2.waitKey(1)    
    ##
    if cap.get(1) == cap.get(7):
        break


cap.release()
rec.release()
cv2.destroyAllWindows()