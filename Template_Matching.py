import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageGrab, ImageDraw
import gc
location = []
location_list = []
def match_image_multi(screencap,imgtemplate):
    searching = bool(True)
    while searching == True:
        im = Image.open(imgtemplate)
        img_rgb = np.array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(imgtemplate, 0)
        template.shape[::-1]
        threshold = 0.8
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val < threshold:
            location_list.append(max_loc)
            im = ImageDraw.rectangle(im, max_loc[0],max_loc[1],min_loc[0],min_loc[1], fill=None, outline=None, width=1)
            searching = True
            
            im.show()
        
        return max_loc

def match_image(screencap,imgtemplate):
    
    im = Image.open(imgtemplate)
    img_rgb = np.array(im)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)
    template.shape[::-1]
    threshold = 0.8
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val < threshold:
        return []
    return max_loc

item = "Lupo_Icon"
pos = match_image('Current.png', 'Lupo_Icon.png')
print(pos)