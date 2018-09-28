import numpy as np 
import cv2

SIZE_MULTIPLIER = 1
PLATE_SIZE = (50 * SIZE_MULTIPLIER, 20 * SIZE_MULTIPLIER)
CHARACTER_SIZE = (17 * SIZE_MULTIPLIER, 7 * SIZE_MULTIPLIER)
ACCEPTED_ERROR = 0.7

def top_hat(image):

    '''  
        params [image] - rotated image 

        return val [open] - image after being preprocessed
                            with morphological operations
                            close is the morphological operation used to close small holes in the image
                            open is the morphological operation used to remove noise
    '''

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # kernel is a structuring element for morphological operation open
    # we use different sizes of kernels because we perform different operations
    kernel_tophat = cv2.getStructuringElement(cv2.MORPH_RECT, (CHARACTER_SIZE[0]*2, 1))
    kenel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (np.uint8(CHARACTER_SIZE[0]/ACCEPTED_ERROR), 1))
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (np.uint8(PLATE_SIZE[0] * ACCEPTED_ERROR), np.uint8(CHARACTER_SIZE[0] * ACCEPTED_ERROR)))

    blur = cv2.GaussianBlur(gray, (3,3), 0)

    # equalize histogram of image in order to improve contrast
    equ = cv2.equalizeHist(blur)

    tophat = cv2.morphologyEx(equ, cv2.MORPH_TOPHAT, kernel_tophat)

    # use OTSU's binarzation since we need to calculate local thresholds
    _, otsu = cv2.threshold(tophat ,0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    close = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kenel_close)
    open = cv2.morphologyEx(close, cv2.MORPH_OPEN, kernel_open)

    return open


