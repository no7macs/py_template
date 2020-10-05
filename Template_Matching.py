import cv2 as cv
from numpy import shape, array
from PIL import Image, ImageGrab, ImageDraw

location_list = []
def match_image_multi(imgtemplate, **kwargs):
    if kwargs.get('screencap',None) == None: im = image_grab(size = kwargs.get('size',None))
    else: im = Image.open(kwargs.get('screencap'))

    searching = bool(True)
    while searching == True:
        img_rgb = array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(imgtemplate, 0)
        try:
            x,y = template.shape[::-1]
            threshold = 0.8
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val > threshold:
                searching = True
                draw = ImageDraw.Draw(im)
                draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
                location_list.append([(max_loc[0],max_loc[1]),(x,y)])
            else: searching = False
        except: pass
        return location_list

def match_image(imgtemplate,**kwargs):
    if kwargs.get('screencap',None) == None: im = image_grab(size = kwargs.get('size',None))
    else: im = Image.open(kwargs.get('screencap'))
    
    if im == None: return([])

    img_rgb = array(im)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)
    try:
        x,y = template.shape[::-1]
        threshold = 0.8
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val < threshold:
            return []
        else: return max_loc
    except: pass
    return []

def image_grab(**kwargs):
    try:
        screenshot = ImageGrab.grab(bbox = (kwargs.get('size',None)))
        return(screenshot)
    except: 
        print('failed to grab screen')
        return(None)