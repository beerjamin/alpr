import cv2 
import numpy as np
import os.path, os, sys
import matplotlib.pyplot as plt
import glob

def increase_brightness(img, value=30):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

def segment(image, name):
    
    bright = increase_brightness(image)
    gray = cv2.cvtColor(bright, cv2.COLOR_BGR2GRAY)
    denoised_gray = cv2.fastNlMeansDenoising(gray, 30, 7, 21)
    equ = cv2.equalizeHist(denoised_gray)
    ret, thresh = cv2.threshold(equ, 80, 255, cv2.THRESH_BINARY)
    height, width = thresh.shape[:2]

    points = thresh.sum(axis=0)
    high = np.amax(points, axis=0)
    marker, y = 0, 0,
    limit = high*0.95
    counter = 0
    
    character_list = []

    named = name.split(".")

    if os.path.exists(str(named[0])):
        print('Directory already exists!')

    else:
        os.mkdir(str(named[0]))

        for i in range(0, width):
            if points[i] >= limit:
                if i-marker > 2:
                    counter += 1

                    if marker > 1 and 3 <= i-marker <= 8:
                        region = image[y: y+height, marker-2:i+4]

                    else:
                        region = image[y: y+height, marker: i+1]

                    character_list.append(region)

                    gray2 = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                    thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                    cv2.imwrite(str(named[0])+'/'+str(counter)+'.jpg', thresh2)
                    marker = i

                else:                   
                    marker += 1
        