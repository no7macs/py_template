import cv2 as cv
from PIL import ImageGrab, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import gc
location = []

def match_image_multi(screencap,imgtemplate):
    #screencap.thumbnail((round(screencap.size[0] * 0.5), round(screencap.size[1] * 0.5)))
    #img_rgb = np.array(screencap)
    img_rgb = cv.imread(screencap)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)
    template.shape[::-1]
    threshold = 0.8
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val < threshold:
        return []
    return max_loc

def match_image(screencap,imgtemplate):
    
    #screencap.thumbnail((round(screencap.size[0] * 0.5), round(screencap.size[1] * 0.5)))
    #img_rgb = np.array(screencap)
    img_rgb = cv.imread(screencap)
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
for b in ['./Item_Icons/' + item + '.png','./Item_Icons/' + item + '_Rotated.png']:
    pos = find_image('Screen_Cap/Current.png', b)
print(pos)