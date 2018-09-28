import numpy as np 
import cv2

def line_remover(plate):
    
    gray = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    height, width = edges.shape[:2]
    edges = edges[0: int(height/2), 0:width]
    minLineLength = 50
    maxLineGap = 30
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength, maxLineGap)

    if lines is None:
        return True
    else:
        return False


def asserter(plate, cut_index=0):

    if line_remover(plate):
        cut_index = cut_index 
    else:
        cut_index += 3
    return cut_index


def boundary(plate):

    cut_index = 0
    height, width = plate.shape[:2]
    asserter(plate, cut_index)
    plate2 = plate[cut_index:height, 0: width]
    
    return plate2