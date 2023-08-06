from operator import truediv
import pyautogui
import os
import shutil
import pyscreeze
import validators
# from pynput import mouse
from array import array


import io
import PIL.Image as Image

import numpy as np
import urllib.request
from urllib.parse import urlparse
from urllib.parse import parse_qs

import cv2

import sys

#import win32api

import logging
import threading
from threading import Event, Thread
import time

#py -m pip install pyautogui
#py -m pip install pillow   
#py -m pip install opencv-python
class KFT_ImageDetector :
    
    #Actions constants
    ACTION_MOVE_TO = 1
    ACTION_CLICK = 2
    ACTION_DOUBLE_CLICK = 3
    ACTION_RIGHT_CLICK = 4
    ACTION_COPY_AREA = 5
    ACTION_WRITE_TEXT = 11

    LISTENER_CLICK = 6
    LISTENER_DOUBLECLICK = 7
    LISTENER_MOUSEENTER = 8
    LISTENER_MOUSEOUT = 9
    LISTENER_MOUSEMOVED = 10

    def __init__(self, path_image):
        self.listeningImage = False;

        self.mouseIsAlreadyEntered = False;

        self.thread_stop = False;
        self.listenerThread = threading.Thread(target=self.threadFunction, args=("listeners",))
        self.listenerThread.start()

        self.eventOnVisible = Event()
        self.eventOnInvisible = Event()

        self.path_image = False


        self.onMouseEnter = self.defaultOnFunc;
        self.onMouseOut = self.defaultOnFunc;
        self.onMouseMoved = self.defaultOnFunc;
        self.onMouseClick = self.defaultOnFunc;
        self.onMouseDoubleClick = self.defaultOnFunc;


        # listenerOn = mouse.Listener(on_click=on_click)
        # self.listenerOn = listenerOn
        # listenerOn.start()
        if validators.url(path_image) == True :
            self.setListeningImage(self.getImageFromURL(path_image))
        else :
            self.setListeningImage(path_image)


    def setListeningImage(self, path_image) :


            if path_image == False :
                self.path_image = path_image
                self.listeningImage = False
            else :
                if os.path.exists(path_image) :
                    self.path_image = path_image
                    self.listeningImage = pyautogui.locateOnScreen(self.path_image, confidence=0.9)
                else :
                    print("Error : image not found !")
                    self.listeningImage = False


    def getLocation(self) :
        if self.listeningImage != False :
            return self.listeningImage
        else :
            print("Error : Location not found !")
            return False


    def getCenterPosition(self) :
        #TODO
        print()
        return any

    def isVisible(self) :
        if self.listeningImage != False :
            if isinstance(self.listeningImage, pyscreeze.Box) :
                return True
            else :
                return False
        else :
            print("Error : Image not found !")
            return False


    def threadFunction(self, threadName) :
        while self.thread_stop == False :
            if(self.listeningImage != False) :
                if self.isVisible() == True :
                    self.eventOnVisible.set()
                else :
                    self.eventOnInvisible.set()

               
                if self.mouseIsInImage() :
                    if self.mouseIsAlreadyEntered == False : 
                        self.mouseIsAlreadyEntered = True
                        self.onMouseEnter()
                else :
                    if self.mouseIsAlreadyEntered == True : 
                        self.mouseIsAlreadyEntered = False
                        self.onMouseOut()

                if self.mouseIsInImage() : 
                    self.onMouseMoved()


                #print( win32api.GetKeyState(0x01))
    	        #key = cv2.waitKey(1) & 0xFF

                #key == ord("r")

                try :
                    self.listeningImage = pyautogui.locateOnScreen(self.path_image, confidence=0.9)
                except OSError as err:
                    self.listeningImage = False
                #print (self.getLocation())



    def mouseIsInImage(self) :
        mP = pyautogui.position()
        iP = self.getLocation()

        if(self.isVisible()) :
            if mP.x >= iP.left and mP.x <= iP.left + iP.width and mP.y >= iP.top and mP.y <= iP.top+iP.height :
                return True

        return False 
                

    def waitVisible(self) :
       self.eventOnVisible.wait()
       
    def waitInvisible(self) :
        self.eventOnInvisible.wait()

    def clearKFT_ImageDetector(self) :
        self.thread_stop = True

        if os.path.isdir("./tmp") == True :
            shutil.rmtree("./tmp")



    def setListener(self, listener, function) : 
        if listener == self.LISTENER_CLICK :
            self.onMouseClick = function #Todo
        if listener == self.LISTENER_DOUBLECLICK :
            self.onMouseDoubleClick = function #Todo
        if listener == self.LISTENER_MOUSEENTER :
            self.onMouseEnter = function
        if listener == self.LISTENER_MOUSEMOVED :
            self.onMouseMoved = function #Todo
        if listener == self.LISTENER_MOUSEOUT :
            self.onMouseOut = function


    def doAction(self, action, text=False) :
        if self.isVisible() :
            if action == self.ACTION_MOVE_TO :
                pyautogui.moveTo(self.listeningImage)
                
            if action == self.ACTION_CLICK :
                pyautogui.click(self.listeningImage, button='left')
            
            if action == self.ACTION_DOUBLE_CLICK :
                pyautogui.doubleClick(self.listeningImage, button='left')

            if action == self.ACTION_RIGHT_CLICK :
                pyautogui.click(self.listeningImage, button='right')

            if action == self.ACTION_COPY_AREA : 
                pyautogui.click(self.listeningImage)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('ctrl', 'c')

            if action == self.ACTION_WRITE_TEXT :
                if text != False :
                    pyautogui.doubleClick(self.listeningImage)
                    pyautogui.write(text)
                else :
                    print("You need text to add text !")

        else :
            print("Error : image not visible")

    def defaultOnFunc(self) :
        print("")


    def getImageFromURL(self, image_url) :
        image = False
        # try : 
        #     #arr = np.asarray(bytearray(urllib2.urlopen("http://img.kalifast.com/?id=227861").read()), dtype=np.uint8)
        #     #arr = np.asarray(bytearray(urllib2.urlopen(image_url).read()), dtype=np.uint8)
        #     #image_byte = cv2.imdecode(arr,-1) # 'load it as it is'
        #     #cv2.imwrite('difference/s2.png', imageSrc)
        #     #print(image_byte)
        # except Exception as inst:

        #     print(inst)





        if os.path.isdir("./tmp") == False :
            os.mkdir("./tmp")


        #image = Image.open(io.BytesIO(image_byte))

        parsed_url = urlparse(image_url)
        captured_value = parse_qs(parsed_url.query)['id'][0]
        path_img = "./tmp/"+captured_value+".png"

        # f = open(path_img, 'wb')
        # f.write(image_byte)
        # f.close()

        urllib.request.urlretrieve(image_url, path_img)


        return path_img


