import numpy as np 
import cv2 
import matplotlib.pyplot as plt
from top_hat import top_hat

''' 

NOTE ABOUT THIS SCRIPT

Band clipping is done before plate_clipping

this script is to crop horizontal sides, should be done before plate clipping which is also called (horizontal detection)

This snippet is called vertical clipping aka band clipping and clips horizontal edges,
not to be confused with "horizontal" detection. 

It is called vertical clipping and clips horizontal edges because we iterate through
the rows of the image (aka height), meaning we iterate the image in a vertical manner.
When we find the peaks of the vertical iteration, we crop according to those peaks, thus, 
resulting in a horizontal clip. 

'''

def image_threshold(image):
    
    ''' 
        params [image] - skew corrected image

        return val [vertical] - array with sum of rows from thresholded image, 
                                used for vertical projection, can be used to plot histogram 
                                and find borders 
    '''

    trialed = top_hat(image)
    vertical = trialed.sum(axis=1)

    return vertical

def normalize(points):
    
    ''' 
        params [points] - array with sum of rows, returned from image_threshold

        return val [points, new] - if the image has noise and the points have no variance,
                                    then we find the points above a threshold and double them,
                                    other points we divide in half to point out the difference 
                                    between borders,
                            new - contains begin and end points of the band
    '''
    mark = []
    highest_value = np.amax(points, axis=0)
    mid_value = int(highest_value*0.6)

    for i in range(0, len(points)):        
        if mid_value <= points[i] <= highest_value:
            points[i] *= 2
            mark.append(i)
        else:
            points[i] *= 0.5
    new = []
    new.append(mark[0])
    new.append(mark[-1])

    return points, new

def select_band(image, vertical):
    
    ''' 
        params [image, vertical] - 
                        image - rotated image
                        vertical - array with sum of rows
        
        return val [roi] - region where the band clipping happened
    '''
    
    _, width = image.shape[:2]
    _, mark = normalize(vertical)
    roi = image[mark[0]-4:mark[1]+4, 0:width]

    return roi
