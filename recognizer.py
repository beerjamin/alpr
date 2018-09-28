from PIL import Image
import sys, os
import pyocr
import pyocr.builders
import cv2



tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]

def recognize_characters(name, mode):

    for filename in os.listdir(name):
        
        if filename.endswith('.jpg'):
            txt = tool.image_to_string(
                Image.open(os.path.join(name, filename)),
                lang="leu",
                builder=pyocr.builders.TextBuilder(mode) #TextBuilder has default parameter -psm 3, 1 for lstm
            )
            print(filename, txt)


