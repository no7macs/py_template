import cv2 as cv
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt
import gc
location = []

def find_image_multi(screencap,imgtemplate):
    img_rgb = cv.imread(screencap)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate,0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    #WaCkY ThREsHOld
    threshold = 0.8
    print(res)
    #Grabs location of WaCkY items
    loc = np.where( res >= threshold)
    itemcount = 0
    mask = np.zeros(img_rgb.shape[:2], np.uint8)
    for pt in zip(*loc[::-1]):
        #Mask, only appends item to list if item was not found already
        if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255:
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            itemcount += 1
            location.append([pt[0],pt[1]])
    gc.collect
    return(location)

def find_image(screencap,imgtemplate):
    
    #screencap.thumbnail((round(screencap.size[0] * 0.5), round(screencap.size[1] * 0.5)))
    #img_rgb = np.array(screencap)
    img_rgb = cv.imread(screencap)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)
    template.shape[::-1]
    precision = 0.8
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val < precision:
        return []
    return max_loc

item = "Lupo_Icon"
for b in ['./Item_Icons/' + item + '.png','./Item_Icons/' + item + '_Rotated.png']:
    pos = find_image('Screen_Cap/Current.png', b)
print(pos)