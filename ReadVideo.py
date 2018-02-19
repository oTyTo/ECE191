import cv2
import numpy as np


cap = cv2.VideoCapture("video\No_Cali.mp4")
rec = cv2.VideoCapture("video\PV_Cali.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2(200, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
while(cap.isOpened()):
    a, frame = cap.read() # get the figure
    #back = frame
    b, back  = rec.read() # get the background
    
    cv2.imshow('frame', frame) 
    cv2.waitKey(1)
    print cap.get(1)
    cv2.imshow('back', back) 
    cv2.waitKey(1)
    print rec.get(1) #print frame No
    

    ## Edge detection here
    edges_f = cv2.Canny(frame,100,120)
    edges_b = cv2.Canny(back,100,120)
   
    #apply mult gaussian
    fgmask = fgbg.apply(edges_f)
    cv2.imshow('sub',fgmask)
    cv2.waitKey(1)
    #edges = edges_f - edges_b

    #print edges_f[100:140][100:140]
    #print edges_b[100:140][100:140]
    #print edges[100:140][100:140]

    #break;

    cv2.imshow('edge_f', edges_f)
    cv2.waitKey(1)
    cv2.imshow('edge_b', edges_b)
    cv2.waitKey(1)
   # cv2.imshow('edges', edges)
    #cv2.waitKey(1)    
    ##
    if cap.get(1) == cap.get(7):
        break


cap.release()
rec.release()
cv2.destroyAllWindows()