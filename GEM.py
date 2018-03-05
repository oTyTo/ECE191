import cv2
import numpy as np
from sklearn.mixture import GaussianMixture 

img = cv2.imread('modcali.jpg')
newdata = img.reshape(1080*1920,3)
gmm = GaussianMixture(n_components=2, covariance_type="tied")
gmm = gmm.fit(newdata)
cluster = gmm.predict(newdata)
mask = 255.*cluster.reshape(1080, 1920)
cv2.imwrite('segmodimage.jpg',mask)