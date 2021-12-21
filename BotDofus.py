import sys
import eel
import cv2
import os
from tkinter import *
import time

from PIL import ImageGrab, Image
import numpy as np  
from pytesseract import pytesseract
import win32gui
import win32api
import win32con


path_to_tesseract = r"C:\Users\CHANUTJB\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

currentDirectory = os.path.dirname(os.path.abspath(__file__)) + '/'
picturesDirectory = currentDirectory + 'pictures/'
dofusHwnd = 0

def main():
    
    win32gui.EnumWindows( winEnumHandler, None )
    if dofusHwnd != 0:
        gui_init()
    
    pos = get_pos(cv2.imread(currentDirectory + 'testPictures/3.png'))
    print(pos)
    if pos:
        print(pos)


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
            print(pos[0][0], " ; ", pos[0][1])
            clique(pos[0][0], pos[0][1])
            time.sleep(3)


def search_pictures(pictures):

    ressourcesPos = []
            
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    
    img_rgb = ImageGrab.grab(bbox)
    img_rgb = cv2.imread(currentDirectory + 'testPictures/4.png')
    
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    threshold = 0.8

    for picture in pictures:
        template = cv2.imread(picturesDirectory + picture,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        loc = np.where( res >= threshold)        
        for pt in zip(*loc[::-1]):
            # Ajouter un if pour éviter de cliquer sur les ressources hors map
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            ressourcesPos.append([(pt[0] + (0.5 * w), pt[1] + (0.5 * h))])
        
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(0)
    return ressourcesPos
    
def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True

def clique(x, y): 

    # hwnd = win32gui.FindWindowEx(0, 0, None, 'Boîte de réception - jb.chanut@amari-metal.Fr - Outlook')
    lParam = win32api.MAKELONG(x, y)
    # hwnds = {}
    # win32gui.EnumChildWindows(hwnd, callback, hwnds)
    # for h in hwnds:
    win32gui.SendMessage(dofusHwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(dofusHwnd, win32con.WM_LBUTTONUP, None, lParam)
        
        
def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        # print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        if win32gui.GetWindowText( hwnd ).find('Dofus') != -1:
            dofusHwnd = hwnd
            
def get_pos(img_rgb):
    
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = img_gray.shape
    
    x1 = int(0.015 * w)
    x2 = int(0.12 * w)
    y1 = int(0.033 * h)
    y2 = int(0.05 * h)
    # print(x1, x2, y1, y2 )
    
    pos_img = img_gray[y1:y2, x1:x2]
    
    to_black = np.where(
        pos_img[:, :] < 228
    )
    pos_img[to_black] = [0]
    
    text = pytesseract.image_to_string(pos_img)
          
    pos_text = text[:-1]
    # pos_text = "15,-156dazdzadza"
        
    # print(res_text, pos)
    
    # cv2.imshow('crop', pos_img)
    # cv2.waitKey(0)

    autorized_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ',']

    res_text = ""

    for i in range(0, len(pos_text)):
        flag = False
        for c in autorized_char:
            if c == pos_text[i]:
                res_text += pos_text[i]
    # print(res_text)
    
    pos_string = res_text.split(',')
    # print(pos_split)
    
    try:
        pos = []
        pos.append(int(pos_string[0]))
        pos.append(int(pos_string[1]))
        return pos
    except:
        return False

if __name__ == '__main__':
    sys.exit(main())