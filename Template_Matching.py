import cv2 as cv
from numpy import shape, array
from PIL import Image, ImageGrab, ImageDraw

Debug = bool(True)

location_list = []
def match_image_multi(imgtemplate, **kwargs):
    if kwargs.get('screencap',None) == None: im = image_grab(size = kwargs.get('size',None))
    else: im = Image.open(kwargs.get('screencap'))

    if im == None: return([])

    img_rgb = array(im)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)

    searching = bool(True)
    while searching == True:

        try:
            x,y = template.shape[::-1]
        except: 
            if Debug == True: print('Failed to find shape Template.Shape most likely caused by image not being found') 
            else: pass
        try:
            if kwargs.get('threshold',None) == None: threshold = 0.8
            else: threshold = Image.open(kwargs.get('threshold'))

            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val > threshold:
                searching = True
                draw = ImageDraw.Draw(im)
                draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
                location_list.append([(max_loc[0],max_loc[1]),(x,y)])
            else: searching = False
        except: 
            if Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
            else: pass
        return location_list

def match_image(imgtemplate,**kwargs):
    if kwargs.get('screencap',None) == None: im = image_grab(size = kwargs.get('size',None))
    else: 
        try: im = Image.open(kwargs.get('screencap',None))
        except: im = kwargs.get('screencap',None)
    if im == None: return([])

    img_rgb = array(im)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(imgtemplate, 0)
    try:
        x,y = template.shape[::-1]
    except: 
        if Debug == True: print('Failed to find shape Template.Shape most likely caused by image not being found') 
        else: pass
    try:
        if kwargs.get('threshold',None) == None: threshold = 0.8
        else: threshold = Image.open(kwargs.get('threshold'))

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val < threshold:
            return []
        else: return (max_loc)
    except: 
        if Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
        else: pass
    return []

def image_grab(**kwargs):
    try:
        return(ImageGrab.grab(bbox = (kwargs.get('size',None))))
    except: 
        if Debug == True: print('failed to grab screen')
        else: pass
        return(None)