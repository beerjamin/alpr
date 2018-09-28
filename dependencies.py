import numpy as np 
import cv2
from detect_plate_image import get_cascade
from deskew_image import *
from band_clipping import *
from plate_clipping import *
from segment import *
from top_hat import top_hat
from remove_lines import *
from recognizer import *