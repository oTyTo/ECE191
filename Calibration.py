import numpy as np
import cv2
import os
import math

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1


def calibrate(img1, img2):

    # develop gray-scale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Instantiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1_gray,None)
    kp2, des2 = sift.detectAndCompute(img2_gray,None)

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        distance = find_max_distance(src_pts, dst_pts)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        return M, distance
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        return None, None


def find_max_distance(src_pts, dst_pts):
    max_distance = 0
    for i in range(len(src_pts)):
        src_x = src_pts[i][0][0]
        src_y = src_pts[i][0][1]

        dst_x = dst_pts[i][0][0]
        dst_y = dst_pts[i][0][1]

        distance = math.hypot(abs(src_x-dst_x), abs(src_y-dst_y))
        max_distance = max(distance, max_distance)

    return max_distance


if __name__ == "__main__":
    print("This module cannot run standalone...Aborting")
    os._exit(1)