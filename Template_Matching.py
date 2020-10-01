import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageGrab, ImageDraw

location_list = []
def match_image_multi(screencap,imgtemplate, **kwargs):
    searching = bool(True)
    im = Image.open(screencap)
    while searching == True:
        img_rgb = np.array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(imgtemplate, 0)
        x,y = template.shape[::-1]
        threshold = 0.8
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val > threshold:
            searching = True
            draw = ImageDraw.Draw(im)
            draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
            location_list.append(max_loc)
        else: searching = False
    return location_list

def match_image(screencap,imgtemplate,**kwargs):
    im = Image.open(screencap)
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

def image_grab(**kwargs):
    screenshot = ImageGrab.grab(bbox = (None))
    screenshot.show()



image_grab()
#item = "Lupo_Icon"
#pos = match_image_multi('Current.png', 'Lupo_Icon.png',)
#print(pos)