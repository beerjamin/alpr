from dependencies import *
import argparse

if __name__ == '__main__':

    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--image", help="path to the (optional) image file")
    ap.add_argument("-m", "--mode", help="segmentation mode supported by tesseract")
    ap.add_argument("-b", "--boundary", help="additional image processing by cropping external boundaries")
    args = vars(ap.parse_args())

    if not args['image']:
        print('--image argument needed') 
        sys.exit(0)

    else:
        image = cv2.imread(args['image'])

        # Step 1. Get the ROI from the cascade classifier
        roi = get_cascade(image)

        # Step 2. Find the rotation angle of the license plates and normalize them
        rotated = rotate(roi)

        # Step 3. Band Clip the rotated ROI (remove horizontal edges)
        vertical = image_threshold(rotated)
        band = select_band(rotated, vertical)

        # Step 4. Plate Clip the band (remove vertical edges)
        horizontal = image_threshold_hor(band)
        plate = clip_plate(band, horizontal)

        # Step 5 (optional). Further pre-process the image by removing remaining line boundaries
        if args['boundary'] == 'y':
            plate = boundary(plate)
        elif args['boundary'] == 'n':
            pass

        # Step 6. Segment the license plate characters
        name = args['image'].split("/")
        segment(plate, name[-1])
        image_dir = name[-1].split('.')

        # Step 7. Do OCR using Tesseract
        recognize_characters(image_dir[0], 10)