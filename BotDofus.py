import sys
import eel
import cv2
import os
from tkinter import *
import time

from PIL import ImageGrab
import win32gui
import win32api
import win32con

currentDirectory = os.path.dirname(os.path.abspath(__file__))
picturesDirectory = currentDirectory + "/pictures/"

def main():

    gui_init()


def gui_init():

    # if(win32gui.FindWindow( None, 'Dofus' ) == 0):
        # return
    
    eel.init(currentDirectory + "/gui")
    
    if not os.path.exists(picturesDirectory):
        os.makedirs(picturesDirectory)
    else:
        print("dossier pictures trouvé au chemin : " + picturesDirectory)
        
    pictures = os.listdir(picturesDirectory)    
    
    eel.get_pictures(pictures)
    eel.start("index.html", mode='chrome', size=(1024, 720))
    
    
@eel.expose
def start(selectedPictures):

    search_pictures(selectedPictures)


def search_pictures(pictures):

    method = cv2.TM_SQDIFF_NORMED

    hwnd = win32gui.FindWindow( None, 'pictures' )
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    
    for picture in pictures:
        
        p = cv2.imread( picturesDirectory + picture )
        res = cv2.matchTemplate(p, img, method)
        mn,_,mnLoc,_ = cv2.minMaxLoc(res)
        MPx,MPy = mnLoc
        
        print(MPx, MPy)

        # search = Search( picturesDirectory + picture )
        
        # pos = search.imagesearch();
        # print(pos)
        # if pos[0] != -1:
        
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)
            # time.sleep(3)
    

if __name__ == '__main__':
    sys.exit(main())