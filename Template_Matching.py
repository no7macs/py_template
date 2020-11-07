import cv2 as cv
from numpy import shape, array, linspace
from PIL import ImageGrab, ImageDraw
import imutils
from numpy.core import multiarray

Debug = bool(True)

class Template_Matching():

    def __init__(self, imgtemplate = None, screencap = None, size = None, threshhold = 0.8, multi_size = False, Debug = True, **kwargs):
        #Should be able to declare all stuff ahead of time to lower on overhead
        self.imgtemplate = imgtemplate
        self.screencap = screencap
        self.size = size
        self.threshhold = threshhold
        self.multi_size = multi_size
        self.Debug = Debug

    def templatesize(self, imgtemplate = None): return (cv.imread(self.imgtemplate if not self.imgtemplate is None else imgtemplate , 0)).shape[::-1]

    def image_grab(self, size):
        try:
            return(ImageGrab.grab(bbox = (size if not size is None else(None))))
        except IOError: 
            if self.Debug == True: print('failed to grab screen')
            else: pass
            return(None)

    def multi_size_match(self, screencap = None, imgtemplate = None):
        found = None

        (x, y) = imgtemplate.shape[:2]
        for scale in linspace(0.2, 1.0, 20)[::-1]:
            resized = imutils.resize(imgtemplate, width = int(imgtemplate.shape[1] / scale))
            print(scale)
            r = float(resized.shape[1]) * screencap.shape[1] 
            if resized.shape[0] > y or resized.shape[1] < x:
                print('break')
                break
            edged = cv.Canny(resized, 50, 200)
            res = cv.matchTemplate(screencap, edged, cv.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            print(max_val)
            if found is None or max_val > found[1]:
                #found = [i * scale for i in res]
                found = (min_val,max_val,min_loc,(max_loc[0]*r,max_loc[1]*r))
        print(found)
        return(found)

    def match_image_multi(self, imgtemplate = None, screencap = None, size = None, threshhold = 0.8, multi_size = None, **kwargs):
        
        threshhold = self.threshhold if not self.threshhold is None else threshhold if threshhold is None else 0.8
        im = self.image_grab(self.size if not self.size is None else size) if not self.screencap is None else (self.screencap if not self.screencap is None else screencap)
        multi_size = self.multi_size if multi_size == None else multi_size

        if im is None: return([])

        template = cv.imread(self.imgtemplate if not self.imgtemplate is None else imgtemplate , 0)

        location_list = []
        searching = bool(True)
        while searching == True:

            img_rgb = array(im)
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

            try:
                x,y = template.shape[::-1]
            except IOError: 
                if self.Debug == True: print('Failed to find shape Template.Shape most likely caused by image not being found') 
                else: pass 
            try:

                min_val, max_val, min_loc, max_loc =  cv.minMaxLoc(cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)) if multi_size == False else self.multi_size_match(screencap = img_gray, imgtemplate = template)

                if max_val > threshhold:
                    searching = True
                    draw = ImageDraw.Draw(im)
                    draw.rectangle([(max_loc[0],max_loc[1]),(max_loc[0]+x,max_loc[1]+y)], fill='#ffffff', outline='#ffffff', width=1)
                    location_list.append(max_loc)
                    im.show()
                else: searching = False
            except IOError: 
                if self.Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
                else: pass
        return (location_list)

    def match_image(self, imgtemplate = None, screencap = None, size = None, threshhold = 0.8, multi_size = None, **kwargs):
        
        threshhold = self.threshhold if not self.threshhold is None else threshhold if threshhold is None else 0.8
        im = self.image_grab(self.size if not self.size is None else size) if not self.screencap is None else (self.screencap if not self.screencap is None else screencap)
        multi_size = self.multi_size if multi_size == None else multi_size

        if im is None: return([])

        img_rgb = array(im)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(self.imgtemplate if not self.imgtemplate is None else imgtemplate, 0)
        try:
            min_val, max_val, min_loc, max_loc =  cv.minMaxLoc(cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)) if multi_size == False else self.multi_size_match(screencap = img_gray, imgtemplate = template)
            if max_val < threshhold:
                return []
            else: return (max_loc)
        except IOError: 
            if self.Debug == True: print('Could not process template, is either caused by Template.shape failing or issue with either image') 
            else: pass
        return []

if __name__ == "__main__":
    objName = Template_Matching()
    objName.match_image() 