import numpy as np
import cv2
import math
from math import *
from scipy import ndimage


def assert_lines(lines):
    
    ''' 
        params [lines] - lines returned from cv2.HoughLinesP()
        
        return value [truth statement] - checking if lines are horizontal or not
                                            we need to avoid horizontal lines
    '''
    
    for x1, y1, x2, y2 in lines[0]:
        return (x2-x1 == 0 or y2-y1 == 0)


def find_line(lines):
    
    '''  
        params [lines] - lines returned from cv2.HoughLinesP()

        return value [line endpoints] - find longest line, if it is 
                                            horizontal, then shift it for 1 pixel 
    '''
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if not (x2-x1 == 0 or y2-y1 == 0):
                return [[x1, y1, x2, y2]]
            else:
                print('added degree to line')
                return [[x1, y1, x2, y2+0.5]]


def rotate(image):
    
    ''' 
        params: [image] - rgb image containing ROI

        return value: [rotated] - rotated image with normalized tilt angle.
                                    in other words, deskewed image
    '''

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    not_image = cv2.bitwise_not(gray)
    
    # blur the image to remove noise
    blur = cv2.GaussianBlur(not_image, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    lines = cv2.HoughLinesP(edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    ''' 
        this statement checks two cases:

            1. If there are no lines detected - if not, change function parameters 
                                from cv2.HoughLinesP(), look for shorter lines
            
            2. If the lines detected are horizontal, horizontal lines will have an angle of 0
    '''
    if lines is None or assert_lines(lines):
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 70, minLineLength=70, maxLineGap=5)
        if lines is None or assert_lines(lines):
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=40, maxLineGap=5)

    newline = find_line(lines)
    angles = []

    # loop to find angle of line
    for x1, y1, x2, y2 in newline:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    
    median_angle = np.median(angles)
    rotated = ndimage.rotate(image, median_angle)
    
    return rotated         
    
        