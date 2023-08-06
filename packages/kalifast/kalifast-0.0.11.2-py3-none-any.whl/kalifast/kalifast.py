# Kalifast main package class
import os
from re import S, X
import shutil

import validators

import tempfile

import datetime
from tkinter import Y
from tkinter import Tk


import urllib.request
from urllib.parse import urlparse
from urllib.parse import parse_qs

import pyautogui

import numpy as np
import cv2
import pytesseract

import os
import io
import PIL.Image as Image

import threading
from threading import Event, Thread
import time



class KFT :
    # OutPut #
    LOG_FILE_NAME          = "logs.txt"
    OUTPUT_STATE_FILE_NAME = "KFT_OUTPUT_STATE"
    OUTPUT_PARAMS_DIR_NAME = "output" #output
    IMAGE_DIR_NAME = "images"

    DEBUG = "DEBUG";
    VERBOSE = "VERBOSE";
    INIT = "INIT";
    ERROR = "ERROR";
    incrementLine = 0;

    VERBOSE_MODE = False;


    #Image Detector#

    #REFERENCES#
    CENTER = 10
    LEFT = 11
    RIGHT = 12

    TOP = 13
    TOP_LEFT = 14
    TOP_RIGHT = 15

    BOT = 16
    BOT_LEFT = 17
    BOT_RIGHT = 18



    DefaultCorrelation = 0.998
    DefaultTimeout = 5000
    DefaultReference = CENTER
    DefaultParentZone = False

    ERROR_IMG_URL_NOT_FOUND = "image_url_not_found"
    ERROR_IMG_NOT_DEFINED = "image_not_defined"
    ERROR_IMAGE_NOT_VISIBLE ="image_not_visible"
    ERROR_SPECIFY_POSITION ="no_position_specified"
    ERROR_TIMEOUT ="timeout"

    thread_result = False
    
    def __init__(self, base_path=False):

        # OutPut #
        if base_path == False :
            base_path = "./"

        if base_path[-1] != '/' :
            base_path += '/'

        if os.path.isdir(base_path) == False :
            os.mkdir(base_path)

        self.base_path = base_path
        self.clearAll()
        self.initLog()



    def setDefaultAttributes(self, correlation=False, timeout=False, reference=False, parentZone=False) :
        if correlation != False :
            self.DefaultCorrelation = correlation
            
        if timeout != False :
            self.DefaultTimeout = timeout

        if correlation != False :
            self.DefaultReference = reference

        if correlation != False :
            self.DefaultParentZone = parentZone
            


    def getAllZone(self, img=False, timeout=DefaultTimeout, correlation=DefaultCorrelation, parentZone=DefaultParentZone, onError=False) :
        if img == False:
            if onError != False :
                return onError
            self.writeLog(text="getAllZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.ERROR, comment=self.ERROR_IMG_NOT_DEFINED + "")
            raise NameError(self.ERROR_IMG_NOT_DEFINED)

        waitVisible = self.waitForVisible(img, timeout, correlation, parentZone)

        if waitVisible == True :
                
            template = False
            arr_parent_zone_img = False
            if parentZone == self.DefaultParentZone :
                screenshot = pyautogui.screenshot(tempfile.gettempdir() + '/m_screen.png')

            
            try :

                if validators.url(img) : 
                    arr = np.asarray(bytearray(urllib.request.urlopen(img).read()), dtype=np.uint8)
                    template = cv2.imdecode(arr,-1) # 'load it as it is'     
                else :
                    if os.path.exists(img) :
                        template = cv2.imread(img, cv2.IMREAD_UNCHANGED)
                    else :
                        if onError != False :
                            return onError      
                        self.writeLog(text="getAllZone("+str(img)+","+str(timeout)+","+str(correlation)+","+str(parentZone)+","+str(onError)+")", type=self.ERROR, comment=self.ERROR_IMG_URL_NOT_FOUND + "")
                        raise NameError(self.ERROR_IMG_URL_NOT_FOUND)



                arr_parent_zone_img = cv2.imread(tempfile.gettempdir()+'/m_screen.png', cv2.IMREAD_UNCHANGED)
    
            except Exception as inst:
                if onError != False :
                    return onError      
                self.writeLog(text="getAllZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.ERROR, comment=self.ERROR_IMG_URL_NOT_FOUND + "")
                raise NameError(self.ERROR_IMG_URL_NOT_FOUND)

            hh, ww = template.shape[:2]

            base = template[:,:,0:3]
            alpha = template[:,:,2]

            alpha = cv2.merge([alpha,alpha,alpha])

            correlation_real = cv2.matchTemplate(arr_parent_zone_img, base, cv2.TM_CCORR_NORMED, mask=alpha)
            loc = np.where(correlation_real >= correlation)
            zones = []

            if len(loc[0]) > 0 and len(loc[1]) > 0 :
                # print(loc)
                if(len(loc[0]) > 1) :
                    
                    zones = [
                                [
                                    [
                                        loc[1][i],
                                        loc[0][i]
                                    ], 
                                    [
                                        loc[1][i]+ww, 
                                        loc[0][i]+hh
                                    ]
                                ]
                                for i in range(len(loc[0]))
                            ]

                else :
                    zones = [
                                [
                                    [
                                        int(loc[1][0]),
                                        int(loc[0][0])
                                    ],
                                    [
                                        int(loc[1][0]+ww),
                                        int(loc[0][0]+hh)
                                    ]
                                ]
                            ]
                            
                # print(zones)


                # xxx = int(loc[1][0])

                # yyy =  int(loc[0][0])

                # top_left_x = xxx
                # top_left_y = yyy

                # bot_right_x = xxx+ww
                # bot_right_y =  yyy+hh

                # zones = [[top_left_x,top_left_y],[bot_right_x,bot_right_y]]
            else :
                if onError != False :
                    return onError   
                self.writeLog(text="getAllZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.ERROR, comment=self.ERROR_IMAGE_NOT_VISIBLE)
                raise NameError(self.ERROR_IMAGE_NOT_VISIBLE)


            if self.VERBOSE_MODE == True :
                self.writeLog(text="getAllZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.VERBOSE, comment= "zones : "+ str(len(zones)) )

            return zones
        else :
            if onError != False :
                    return onError   
            self.writeLog(text="getAllZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.ERROR, comment=self.ERROR_TIMEOUT)
            raise NameError(self.ERROR_TIMEOUT)


    
    #ImageDetector
    def getFirstZone(self, img=False, timeout=DefaultTimeout, correlation=DefaultCorrelation, parentZone=DefaultParentZone, onError=False) :
        try :
            zones = self.getAllZone(img,timeout,correlation,parentZone,onError)
            return zones[0]

        except Exception as e:
            if onError != False :
                    return onError   
            # self.writeLog(text="getFirstZone("+str(img)+", "+str(timeout)+", "+str(correlation)+", "+str(parentZone)+", "+str(onError)+")", type=self.ERROR, comment=e)
            # raise NameError(str(e))



    def pause(self, duration=DefaultTimeout) :
        time.sleep(duration/1000)
        
        if self.VERBOSE_MODE == True :
             self.writeLog(text="pause("+str(duration)+")", type=self.VERBOSE)


    def isVisible(self, img=False, correlation=DefaultCorrelation, parentZone=DefaultParentZone) :
        if img == False:
            self.writeLog(text="isVisible(img=\""+str(img)+"\", correlation="+str(parentZone)+", parentZone="+str(parentZone)+")", type=self.ERROR, comment=self.ERROR_IMG_NOT_DEFINED + "")
            raise NameError(self.ERROR_IMG_NOT_DEFINED)
        
        if parentZone == self.DefaultParentZone :
            screenshot = pyautogui.screenshot(tempfile.gettempdir() + '/m_screen.png')
            # arr_parent_zone_img = np.array(screenshot)


        try :
            if validators.url(img) : 
                arr = np.asarray(bytearray(urllib.request.urlopen(img).read()), dtype=np.uint8)
                template = cv2.imdecode(arr,-1) # 'load it as it is'    
            else :
                if os.path.exists(img) :
                    template = cv2.imread(img, cv2.IMREAD_UNCHANGED)
                else :
                    self.writeLog(text="isVisible(img=\""+str(img)+"\", correlation="+str(parentZone)+", parentZone="+str(parentZone)+")", type=self.ERROR, comment=self.ERROR_IMG_URL_NOT_FOUND + "")
                    raise NameError(self.ERROR_IMG_URL_NOT_FOUND)


            arr_parent_zone_img = cv2.imread(tempfile.gettempdir()+'/m_screen.png', cv2.IMREAD_UNCHANGED)
  
        except Exception as inst:         
            self.writeLog(text="isVisible(img=\""+str(img)+"\", correlation="+str(parentZone)+", parentZone="+str(parentZone)+")", type=self.ERROR, comment=self.ERROR_IMG_URL_NOT_FOUND + "")
            raise NameError(self.ERROR_IMG_URL_NOT_FOUND)

        # hh, ww = template.shape[:2]
        base = template[:,:,0:3]
        alpha = template[:,:,2]
        alpha = cv2.merge([alpha,alpha,alpha])
        correlation_real = cv2.matchTemplate(arr_parent_zone_img, base, cv2.TM_CCORR_NORMED, mask=alpha)
        # print(correlation_real)
        # print(correlation)

        loc = np.where(correlation_real >= correlation)

        # print(len(loc[0]))
        if self.VERBOSE_MODE == True :
            self.writeLog(text="isVisible(img=\""+str(img)+"\", correlation="+str(parentZone)+", parentZone="+str(parentZone)+")", type=self.VERBOSE, comment ="visible : "+ str(len(loc[0]) > 0 and len(loc[1]) > 0))

        if len(loc[0]) > 0 and len(loc[1]) > 0 :
            return True

        return False
        




    #  self.eventOnVisible.set()
    def waitForVisible(self, img=False, timeout=DefaultTimeout, correlation=DefaultCorrelation,parentZone=DefaultParentZone) :
        eventOnVisible = Event()

        listenerThread = threading.Thread(target=self.waitForImgThread, args=(eventOnVisible,img,timeout,correlation,parentZone,True,))
        listenerThread.start()

        eventOnVisible.wait()

        if self.VERBOSE_MODE == True :
            self.writeLog(text="waitForVisible(img=\""+str(img)+"\", timeout="+str(timeout)+", correlation="+str(correlation)+",parentZone="+str(parentZone)+")", type=self.VERBOSE, comment="thread timeout : " + str(self.thread_result != self.thread_result))
        return self.thread_result


    def waitForNotVisible(self, img=False, timeout=DefaultTimeout, correlation=DefaultCorrelation,parentZone=DefaultParentZone) :
        eventOnVisible = Event()

        listenerThread = threading.Thread(target=self.waitForImgThread, args=(eventOnVisible,img,timeout,correlation,parentZone,False,))
        listenerThread.start()

        eventOnVisible.wait()


        if self.VERBOSE_MODE == True :
            self.writeLog(text="waitForNotVisible(img=\""+str(img)+"\", timeout="+str(timeout)+", correlation="+str(correlation)+",parentZone="+str(parentZone)+")", type=self.VERBOSE, comment="thread timeout : " + str(self.thread_result != self.thread_result))

        return self.thread_result

    def waitForImgThread(self, eventOnVisible, img=False, timeout=DefaultTimeout, correlation=DefaultCorrelation, parentZone=DefaultParentZone, visible=True) :
        
        start_ms = int(round(time.time() * 1000))

        thread_out = False
        while thread_out == False :
            now_ms = int(round(time.time() * 1000))
            if now_ms-start_ms >= timeout :
                thread_out = True
                self.thread_result = False

            if self.isVisible(img, correlation, parentZone) == visible:
                thread_out = True
                self.thread_result = True
        
        eventOnVisible.set()

        # if self.VERBOSE_MODE == True :
            # self.writeLog(text="", type=self.VERBOSE)


    def getAllPosition(self, img=False, timeout=DefaultTimeout, onError=False, ref=CENTER, at=[0,0], correlation=DefaultCorrelation, parentZone=DefaultParentZone) :
        try :
            zones = self.getAllZone(img=img,timeout=timeout,correlation=correlation,parentZone=parentZone)

            # width = (zones[i][1][0] - zone[i][0][0])
            # height = (zones[i][1][1] - zones[i][0][1])
                # print(loc)
                
            # positions = [[ zones[i][0][0], zones[i][0][1] ] for i in range(len(zones[0]))]

             # print(zone)
            if len(zones) > 1 :
                if ref == self.TOP_LEFT :
                    positions = [[ zones[i][0][0]+at[0], zones[i][0][1]+at[1] ] for i in range(len(zones[0]))]

                    # position_x = zone[0][0]
                    # position_y = zone[0][1]
                if ref == self.TOP :
                    positions = [[ zones[i][0][0]+((zones[i][1][0] - zones[i][0][0])/2)+at[0], zones[i][0][1]+at[1] ] for i in range(len(zones[0]))]

                #      position_x = zone[0][0]+(width/2)
                #      position_y = zone[0][1]
                if ref == self.TOP_RIGHT :
                    positions = [[ zones[i][0][0]+(zones[i][1][0] - zones[i][0][0])+at[0], zones[i][0][1]+at[1] ] for i in range(len(zones[0]))]

                #      position_x = zone[0][0]+width
                #      position_y = zone[0][1]
                if ref == self.LEFT :
                    positions = [[ zones[i][0][0]+at[0], zones[i][0][1]+ ((zones[i][1][1] - zones[i][0][1])/2)+at[1] ] for i in range(len(zones[0]))]

                #      position_x = zone[0][0]
                #      position_y = zone[0][1]+(height/2)
                if ref == self.CENTER :
                    positions = [[ zones[i][0][0]+((zones[i][1][0] - zones[i][0][0])/2)+at[0], zones[i][0][1]+ ((zones[i][1][1] - zones[i][0][1])/2)+at[1] ] for i in range(len(zones[0]))]

                #      position_x = zone[0][0]+(width/2)
                #      position_y = zone[0][1]+(height/2)
                if ref == self.RIGHT :
                    positions = [[ zones[i][0][0]+at[0], zones[i][0][1]+ ((zones[i][1][1] - zones[i][0][1])/2)+at[1] ] for i in range(len(zones[0]))]

                #      position_x = zone[0][0]+width
                #      position_y = zone[0][1]+(height/2)
                if ref == self.BOT_LEFT :
                    positions = [[ zones[i][0][0]+at[0], zones[i][0][1]+ (zones[i][1][1] - zones[i][0][1])+at[1] ] for i in range(len(zones[0]))]

                #     position_x = zone[0][0]
                #     position_y = zone[0][1]+height
                if ref == self.BOT_RIGHT :
                    positions = [[ zones[i][1][0]+at[0], zones[i][1][1]+at[1] ] for i in range(len(zones[0]))]

                #     position_x = zone[1][0]
                #     position_y = zone[1][1]
                if ref == self.BOT :
                    positions = [[ zones[i][0][0]+((zones[i][1][0] - zones[i][0][0])/2)+at[0], zones[i][0][1]+ (zones[i][1][1] - zones[i][0][1])+at[1] ] for i in range(len(zones[0]))]

                #     position_x = zone[0][0]+(width/2)
                #     position_y = zone[0][1]+height

                # position_x += at[0]
                # position_y += at[1]
                
                # pyautogui.moveTo(x =position_x, y =position_y)
            else :
                
                width = (zones[0][1][0] - zones[0][0][0])
                height = (zones[0][1][1] - zones[0][0][1])
                position_x = 0;
                position_y = 0;

                if ref == self.TOP_LEFT :
                    position_x = zones[0][0][0]
                    position_y = zones[0][0][1]
                if ref == self.TOP :
                    position_x = zones[0][0][0]+(width/2)
                    position_y = zones[0][0][1]
                if ref == self.TOP_RIGHT :
                     position_x = zones[0][0][0]+width
                     position_y = zones[0][0][1]
                if ref == self.LEFT :
                     position_x = zones[0][0][0]
                     position_y = zones[0][0][1]+(height/2)
                if ref == self.CENTER :
                     position_x = zones[0][0][0]+(width/2)
                     position_y = zones[0][0][1]+(height/2)
                if ref == self.RIGHT :
                     position_x = zones[0][0][0]+width
                     position_y = zones[0][0][1]+(height/2)
                if ref == self.BOT_LEFT :
                    position_x = zones[0][0][0]
                    position_y = zones[0][0][1]+height
                if ref == self.BOT_RIGHT :
                    position_x = zones[0][1][0]
                    position_y = zones[0][1][1]
                if ref == self.BOT :
                    position_x = zones[0][0][0]+(width/2)
                    position_y = zones[0][1]+height

                positions = [[position_x+at[0],position_y+at[1]]]


            if self.VERBOSE_MODE == True :
                self.writeLog(text="getAllPosition(img=\""+str(img)+"\", timeout="+str(timeout)+", onError="+str(onError)+", ref="+str(ref)+", at="+str(at)+", correlation="+str(correlation)+", parentZone="+str(parentZone)+")", type=self.VERBOSE, comment="Positions : " + str(len(zones[0])))

            return positions

        except Exception as e :
            if onError != False :
                return onError
            self.writeLog(text="getAllPosition(img=\""+str(img)+"\", timeout="+str(timeout)+", onError="+str(onError)+", ref="+str(ref)+", at="+str(at)+", correlation="+str(correlation)+", parentZone="+str(parentZone)+")", type=self.ERROR, comment=str(e))
            raise NameError(str(e))


    def getFirstPosition(self, img=False, timeout=DefaultTimeout, onError=False, ref=CENTER, at=[0,0], correlation=DefaultCorrelation, parentZone=DefaultParentZone) :
        try :
            all_zones = self.getAllPosition(img=img,timeout=timeout,onError=onError,ref=ref,at=at,correlation=correlation,parentZone=parentZone)
            # pyautogui.moveTo(x =position_x, y =position_y)
            if self.VERBOSE_MODE == True :
                self.writeLog(text="getFirstPosition(img=\""+str(img)+"\", timeout="+str(timeout)+", onError="+str(onError)+", ref="+str(ref)+", at="+str(at)+", correlation="+str(correlation)+", parentZone="+str(parentZone)+")", type=self.VERBOSE)

            return all_zones[0]

        except Exception as e :
            if onError != False :
                return onError
            self.writeLog(text="getFirstPosition(img=\""+str(img)+"\", timeout="+str(timeout)+", onError="+str(onError)+", ref="+str(ref)+", at="+str(at)+", correlation="+str(correlation)+", parentZone="+str(parentZone)+")", type=self.ERROR, comment=str(e))
            raise NameError(str(e))



    def move(self, pos=False, fromTo=0):
        
        if pos == False :
            self.writeLog(text="move(pos="+str(pos)+", fromTo="+str(fromTo)+")", type=self.ERROR, comment=self.ERROR_SPECIFY_POSITION)
            raise NameError(self.ERROR_SPECIFY_POSITION)

        time.sleep(fromTo/1000)

        pyautogui.moveTo(x = pos[0], y = pos[1])

        if self.VERBOSE_MODE == True :
            self.writeLog(text="move(pos="+str(pos)+", fromTo="+str(fromTo)+")", type=self.VERBOSE)


    def click(self, pos=False) :
        if pos == False :
            self.writeLog(text="move(pos="+str(pos)+")", type=self.ERROR, comment=self.ERROR_SPECIFY_POSITION)
            raise NameError(self.ERROR_SPECIFY_POSITION)
        
        pyautogui.click(x = pos[0], y = pos[1], button='left')


        if self.VERBOSE_MODE == True :
            self.writeLog(text="click(pos="+str(pos)+")", type=self.VERBOSE)

    def getTextAt(self, pos=False, onError="default_returntxt") :
        #TODO

        self.click(pos)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        self.click(pos)
        copied = Tk().clipboard_get()

        print(copied)


        if self.VERBOSE_MODE == True :
            self.writeLog(text="getTextAt(pos="+str(pos)+", onError="+str(onError)+")", type=self.VERBOSE)

        return copied



    #TODO
    # def getOCRText(self, pos=False, onError="default_returntxt") :
        # pytesseract.pytesseract.tesseract_cmd=r'C:Program FilesTesseract-OCRtesseract.exe'
        # img = cv2.imread("./textarea.png")
        # img = cv2.resize(img, (400, 450))
        # cv2.imshow("Image", img)
        # text = pytesseract.image_to_string(img)
        # print(text)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return "text"


    def mouseUp(self, pos) :
        if pos != False :
            self.move(pos)
        pyautogui.mouseUp();
        
        if self.VERBOSE_MODE == True :
            self.writeLog(text="mouseUp(pos="+str(pos)+")", type=self.VERBOSE)

    def mouseDown(self, pos) :
        if pos != False :
            self.move(pos)
        pyautogui.mouseDown();

        if self.VERBOSE_MODE == True :
            self.writeLog(text="mouseDown(pos="+str(pos)+")", type=self.VERBOSE)

    def typeAt(self, pos,text="", interval=0) :
        self.click(pos)
        pyautogui.write(text, interval=interval)    

        if self.VERBOSE_MODE == True :
            self.writeLog(text="typeAt(pos="+str(pos)+", text="+str(text)+", interval="+str(interval)+")", type=self.VERBOSE)


    def scroll(self, pos, distance=0) :
        self.click(pos)
        pyautogui.scroll(distance)
        if self.VERBOSE_MODE == True :
            self.writeLog(text="scroll(pos="+str(pos)+", distance="+str(distance)+")", type=self.VERBOSE)

    def doubleClick(self, pos, interval=0) :
        # if pos == False :
        #     self.writeLog(text="move()", type=self.ERROR, comment=self.ERROR_SPECIFY_POSITION)
        #     raise NameError(self.ERROR_SPECIFY_POSITION)
        
        pyautogui.click(x = pos[0], y = pos[1], button='left')
        time.sleep(interval/1000)
        pyautogui.click(x = pos[0], y = pos[1], button='left')


        if self.VERBOSE_MODE == True :
            self.writeLog(text="click(pos="+str(pos)+", distance="+str(interval)+")", type=self.VERBOSE)
    # OutPut #



    def initLog(self):
        # if self.VERBOSE_MODE == True :
            # self.writeLog(text="INIT SCRIPT", type=self.INIT)

        self.incrementLine = 0;

        f = open(self.base_path + self.LOG_FILE_NAME, "a")
        f.write("=====NEW EXECUTION=====\n")
        f.close()


    def setVerbose(self, bool) :
        if self.VERBOSE_MODE == True :
            self.writeLog(text="Verbose disables", type=self.VERBOSE)

        self.VERBOSE_MODE = bool

    def writeLog(self, text=False, type=False, comment=False):
        
        f = open(self.base_path + self.LOG_FILE_NAME, "a")
        
        if type == False :
            type = self.DEBUG

        if text != False :
            self.incrementLine = self.incrementLine + 1

            e = datetime.datetime.now()
            dateString = "%s:%s:%s - %s:%s:%s" % (e.day, e.month, e.year, e.hour, e.minute, e.second)
            if comment != False :
                f.write(str(self.incrementLine) + " | " + dateString + " : (" + type + ") "+ text + " - (information : " + comment + ")\n")
            else :
                f.write(str(self.incrementLine) + " | " + dateString + " : (" + type + ") "+ text +"\n")

        f.close()



    def setOutPutState(self, output_state):
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == False :
            os.mkdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)

            if os.path.exists(self.base_path + self.OUTPUT_PARAMS_DIR_NAME + "/" + self.OUTPUT_STATE_FILE_NAME)  == True :
                if self.VERBOSE_MODE == True :
                    self.writeLog(text="setOutPutState(\""+output_state+"\")", type=self.VERBOSE)
            else :
                if self.VERBOSE_MODE == True :
                    self.writeLog(text="setOutPutState(\""+output_state+"\")", type=self.VERBOSE, comment="New OutPutState")


        f = open(self.base_path + self.OUTPUT_PARAMS_DIR_NAME + "/" + self.OUTPUT_STATE_FILE_NAME, "w")
        f.write(output_state)
        f.close()

        if self.VERBOSE_MODE == True :
            self.writeLog(text="setOutPutState(\""+str(output_state)+"\")", type=self.VERBOSE)


    


    def addOutPutParam(self, param, value):
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == False :
            os.mkdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)


        f = open(self.base_path + self.OUTPUT_PARAMS_DIR_NAME + "/" + param, "w")
        f.write(value)
        f.close()

        if self.VERBOSE_MODE == True :
            self.writeLog(text="addOutPutParam(\""+param+"\",\""+value+"\")", type=self.VERBOSE)



    def addOutPutImage(self, path_image):
        if os.path.isdir(self.base_path + self.IMAGE_DIR_NAME) == False :
            os.mkdir(self.base_path + self.IMAGE_DIR_NAME)

        if os.path.exists(path_image) :
            shutil.copy(path_image, self.base_path + self.IMAGE_DIR_NAME)
        else :
            print("Error : image not found !")

        if self.VERBOSE_MODE == True :
            self.writeLog(text="addOutPutImage(\""+path_image+"\")", type=self.VERBOSE)

    def clearAll(self):
        #remove log file

        if os.path.exists(self.base_path + self.LOG_FILE_NAME) :
            os.remove(self.base_path + self.LOG_FILE_NAME)

        #output state file
        if os.path.exists(self.base_path + self.OUTPUT_STATE_FILE_NAME) :
            os.remove(self.base_path + self.OUTPUT_STATE_FILE_NAME)

        #output param dir
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == True :
            shutil.rmtree(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)

        #images dir
        if os.path.isdir(self.base_path + self.IMAGE_DIR_NAME) == True :
            shutil.rmtree(self.base_path + self.IMAGE_DIR_NAME)

        if os.path.isdir("./tmp") == True :
            shutil.rmtree("./tmp")


    def getKalifastVar(self, var_name) :
        if os.path.isdir("./input") == True :
            if os.path.exists("./input/"+var_name) :
                f = open("./input/"+var_name, "r")
                var_value = f.read()
                f.close()
                return var_value

        return False
    








    def getImageFromURL(self, image_url) :
        image = False
        if os.path.isdir("./tmp") == False :
            os.mkdir("./tmp")

        parsed_url = urlparse(image_url)
        captured_value = parse_qs(parsed_url.query)['id'][0]

        path_img = "./tmp/"+captured_value+".png"
        try :
            urllib.request.urlretrieve(image_url, path_img)
        except Exception as e:
            print(e)

        return path_img





class KFT_Zone() :
    def __init__(self,x=False,y=False,width=False,height=False, top_left_x = False,  top_left_y = False, bot_right_x = False, bot_right_y = False) :
        self.x = x;
        self.y = y;
        self.width = width;
        self.height = height;


        self.top_left_x = top_left_x
        self.top_left_y = top_left_y

        self.bot_right_x = bot_right_x
        self.bot_right_y = bot_right_y
    
