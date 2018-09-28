
License Plate Recognition
=========================

Source code for License Plate Recognition 

Main file, (steps.py) includes 5 steps

    1. Getting the ROI by using the cascade classifier
    2. Checking if the plates are rotated, if yes, find the angle of rotation and correct the skew
    3. Remove the horizontal edges, also known as band clipping
    4. Remove the vertical edges, also known as plate clipping
    5. Segment the characters of the license plate

For more information see `the docs`_.


