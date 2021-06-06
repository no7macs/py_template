import cv2 as cv
from numpy import shape, array, linspace
from PIL import ImageGrab, ImageDraw
import imutils
import time

Debug = bool(True)

class TemplateMatching():

    def __init__(self, imgtemplate = None, screenCap = None, size = (1920, 1080), threshHold = 0.8, multi_size = False, Debug = True, **kwargs):
        #Should be able to declare all stuff ahead of time to lower on overhead
        self.imgtemplate = imgtemplate
        self.screenCap = screenCap
        self.size = size
        self.threshHold = threshHold
        self.multi_size = multi_size
        self.Debug = Debug

    #returns the size of the template
    def getTamplateSize(self, imgtemplate = None): 
        return (cv.imread(self.imgtemplate if not self.imgtemplate is None else imgtemplate , 0)).shape[::-1]

    #grabs a screenshot
    def image_grab(self, size):
        try:
            return(ImageGrab.grab(bbox = (size if not size is None else(None))))
        except IOError: 
            if self.Debug == True: print('failed to grab screen')
            else: pass
            return(None)

    '''
    def multi_size_match(self, screenCap = None, imgtemplate = None):
        return

    def match_image_multi(self, imgtemplate = None, screenCap = None, size = None, threshHold = 0.8, multi_size = None, **kwargs):
        threshHold = self.threshHold if not self.threshHold is None else threshHold if threshHold is None else 0.8
        im = self.image_grab(self.size if not self.size is None else size) if not self.screenCap is None else (self.screenCap if not self.screenCap is None else screenCap)
        multi_size = self.multi_size if multi_size is None else multi_size

        location_list = []
        max_val_list = []
        searching = bool(True)

        template = cv.imread(self.imgtemplate if not self.imgtemplate is None else imgtemplate , 0)
        y,x = template.shape[::1]

        #return max_val, max_loc
        while searching == True:
            
            max_val, max_loc, scale = self.match_image(imgtemplate, im, multi_size = multi_size)

            if max_val > threshHold:
                searching = True
                draw = ImageDraw.Draw(im)
                draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
                location_list.append(max_loc)
                max_val_list.append(max_val)

                im.show()
                time.sleep(2)
            else: searching = False
        return max_val_list,location_list
    '''

    def match_image(self, threshHold = 0.8, **kwargs):
        threshHold = self.threshHold if not self.threshHold is None else 0.8 #grab treshold, if not given set to 0.8
        im = self.image_grab(self.size) if self.screenCap is None else self.screenCap #grabs screensize if size is not given

        if im is None: return(0,(0,1))

        img_rgb = array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(self.imgtemplate, 0)
        #template = cv.cvtColor(imgtemplate, cv.COLOR_BGR2GRAY)
        scale = int(1)

        try:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED))
            
            if max_val < threshHold:
                return 0,(0,1),0
            else: return max_val, max_loc, scale
        except IOError: 
            if self.Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
            else: pass
        return 0,(0,1),0

    #------------------------------------------------------------------------------------#
    #setters

    def setImageTemplate(self, imgTemplate) -> None:
        self.imgtemplate = imgTemplate
        return()

    def setscreenCap(self, screenCap) -> None:
        self.screenCap = screenCap
        return()

    def setTheshHold(self, threshHold) -> None:
        self.threshHold = threshHold
        return()

    def setSize(self, size) -> None:
        self.size = size
        return()
