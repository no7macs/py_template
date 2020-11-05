import cv2 as cv
from numpy import shape, array
from PIL import ImageGrab, ImageDraw

Debug = bool(True)

class Template_Matching:
    Debug = bool(True)

    def __init__(self, imgtemplate = None, screencap = None, size = None, threshhold = 0.8, **kwargs):
        #Should be able to declare all stuff ahead of time to lower on overhead
        self.imgtemplate = imgtemplate
        self.screencap = screencap
        self.size = size
        self.threshhold = threshhold

    def match_image_multi(self, imgtemplate = self.imgtemplate if not self.imgtemplate is None else None, screencap = self.screencap if not self.screencap is None else None, size = self.size if not self.size is None else None, 
                        threshhold = self.threshold if not self.threshhold is None else None, **kwargs):
        im = image_grab(size) if screencap is None else screencap

        if im is None: return([])

        template = cv.imread(imgtemplate if not imgtemplate is None else None , 0)

        location_list = []
        searching = bool(True)
        while searching == True:

            img_rgb = array(im)
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

            try:
                x,y = template.shape[::-1]
            except IOError: 
                if Debug == True: print('Failed to find shape Template.Shape most likely caused by image not being found') 
                else: pass 
            try:
                threshold = 0.8 if threshhold is None else 0.8

                res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

                if max_val > threshold:
                    searching = True
                    draw = ImageDraw.Draw(im)
                    draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
                    location_list.append([(max_loc[0],max_loc[1]),(x,y)])
                    im.show()
                else: searching = False
            except IOError: 
                if Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
                else: pass
        return location_list

    def match_image(self, imgtemplate = self.imgtemplate if not self.imgtemplate is None else None, screencap = self.screencap if not self.screencap is None else None, size = self.size if not self.size is None else None, 
                    threshhold = self.threshold if not self.threshhold is None else None, **kwargs):
        im = image_grab(size) if screencap is None else screencap

        if im is None: return([])

        img_rgb = array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(imgtemplate if not imgtemplate is None else None , 0)
        try:
            threshold = 0.8 if threshhold is None else 0.8

            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val < threshold:
                return []
            else: return (max_loc)
        except IOError: 
            if Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
            else: pass
        return []

def image_grab(size):
    try:
        return(ImageGrab.grab(bbox = (size if not size is None else(None))))
    except IOError: 
        if Debug == True: print('failed to grab screen')
        else: pass
        return(None)