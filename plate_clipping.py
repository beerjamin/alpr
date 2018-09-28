import cv2 
import numpy as np 

''' 

NOTE ABOUT THIS SCRIPT

Plate clipping is done after Band clipping

this script is to crop vertical sides of the license plate. it is called plate-clipping or horizontal detection.

It is called horizontal detection because we iterate the columns of the image, through the horizontal axis X.
It should not be confused with band_clipping, which clips horizontal edges.

When we find the peaks of the horizontal iteration, we crop according to those peaks, thus, 
resulting in a vertical clip. 

'''

def normalize_plate(points):
    
    ''' 
        params [points] - array with sum of rows, returned from image_threshold_hor,
                            selects points above the threshold and stores them as 
                            plate coordinates

        return val [new] - contains begin and end points of the plate
    '''
    
    mark = []
    mark2= []

    highest_value = np.amax(points, axis=0)
    low_limit = int(highest_value*0.1)
    mid_length = int(len(points)/2)

    for i in range(0, mid_length):
        if points[i] <= low_limit:
            mark.append(i)

    for i in range(mid_length, len(points)):
        if points[i] <= low_limit:
            mark2.append(i)
        
    new = []
    new.append(mark[-1])
    new.append(mark2[0])
    return new

def image_threshold_hor(image):
    
    ''' 
        params [image] - band clipped image

        return val [horizontal] - array with sum of columns from thresholded image, 
                                used for horizontal projection, can be used to plot histogram 
                                and find borders 
    '''

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    horizontal = thresh.sum(axis=0)

    return horizontal

def resize(image, direction):
    
    '''  
        function used to resize image regions, not very useful anymore
    '''
    
    height, _ = image.shape[:2]
    mark = normalize_plate(direction)
    roi = image[0:height,mark[0]:mark[1]]

    return roi

def clip_plate(image, horizontal):
    
    ''' 
        params [image, horizontal] - 
                        image - rotated image
                        horizontal - array with sum of columns
        
        return val [roi] - region where the plate clipping happened
    '''

    height, _ = image.shape[:2]
    mark = normalize_plate(horizontal)
    roi = image[0:height,mark[0]:mark[1]]

    return roi
