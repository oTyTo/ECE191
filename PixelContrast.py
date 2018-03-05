import cv2
import numpy as np

# Reads image
cv = cv2.imread("CV_Cali_with_subject.jpg")

# Gets dimensions of cv
cv_height, cv_width, cv_depth = cv.shape

# Sets threshold
threshold = [10, 10, 10]

# Sets initial minimum
minimum = [255,255,255]

# Loop through each pixel - optimize this
for i in range(0, cv_height):
    for j in range(0, cv_width):
        if ((cv[i,j] < minimum).all()): 
            minimum = cv[i,j]

# Create copy of cv to mask over
image = cv.copy()

# Mask proper area
image[np.where((image < (minimum + threshold)).all(axis=2))] = [0, 0, 255]

# Display images
cv2.imshow('image', cv)
cv2.waitKey(0)
cv2.imshow('image2', image)
cv2.waitKey(0)

