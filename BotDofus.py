import sys
import eel
import cv2
import os
from tkinter import *
import time

from PIL import ImageGrab
import numpy as np  
import win32gui
import win32api
import win32con

currentDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'
picturesDirectory = currentDirectory + 'pictures/'
dofusWindow = 0

def main():
    
    win32gui.EnumWindows( winEnumHandler, None )
    if dofusWindow != 0:
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

    while True:
        ressourcesPos = search_pictures(selectedPictures)
        # print(ressourcesPos)
        if not len(ressourcesPos):
            break
        
        for pos in ressourcesPos:
            # print(pos)
            


def search_pictures(pictures):

    ressourcesPos = []
    
    # hwnd = win32gui.FindWindow( None, 'pictures' )
    # win32gui.SetForegroundWindow(hwnd)
    # bbox = win32gui.GetWindowRect(hwnd)
    # img = ImageGrab.grab(bbox)
    
    img_rgb = cv2.imread(currentDirectory + 'testPictures/6.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    threshold = 0.9

    for picture in pictures:
        template = cv2.imread(picturesDirectory + picture,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        loc = np.where( res >= threshold)        
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            ressourcesPos.append([pt, (pt[0] + w, pt[1] + h)])
        
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(0)
    return ressourcesPos
    
    def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True

def clique(x, y): 

    lParam = win32api.MAKELONG(x, y)

    hwnd = win32gui.FindWindowEx(0, 0, None, 'Boîte de réception - jb.chanut@amari-metal.Fr - Outlook')
    hwnds = {}
    win32gui.EnumChildWindows(hwnd, callback, hwnds)
    for h in hwnds:
        win32gui.SendMessage(hwnds[h], win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hwnds[h], win32con.WM_LBUTTONUP, None, lParam)
        
        
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        if win32gui.GetWindowText( hwnd ).find('Dofus') != -1:
            dofusWindow = hwnd

if __name__ == '__main__':
    sys.exit(main())