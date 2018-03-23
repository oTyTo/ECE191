## This program take two images as inputs and output a geomatric transform matrix
import numpy as np
import scipy.io as sio
import cv2

MIN_MATCH_COUNT = 10                          #least number of matches to generate transform matrix
cv = cv2.imread('images/NoCV1.jpg')           # cv
pv = cv2.imread('images/PV1.jpg')             # pv

img1 = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(pv, cv2.COLOR_BGR2GRAY)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

#match keypoints using KNN
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    sio.savemat('Geo_Transfer.mat',{'M':M})

else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None