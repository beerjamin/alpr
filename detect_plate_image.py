import cv2, sys
import numpy as np

def get_cascade(image):
    
    ''' 
        params: [filename]

        return value: [roi_color] - region of interest selected by the cascade classifier 
    '''

    car_cascade = cv2.CascadeClassifier('cascade.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = car_cascade.detectMultiScale(gray, 1.3, 5)
    
    # checking if we actually detected the license plate regions
    if len(faces) == 0:
        print('Nothing has been detected, try another image. Exiting...')
        sys.exit(0)

    for (x,y,w,h) in faces:
        roi_color = image[y:y+h, x:x+w]

        #checking not to have two regions of interest
        if faces.shape[0] > 1:
            break

    return roi_color
