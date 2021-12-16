import sys
import eel
from screen_search import *
import os
from tkinter import *
import time

from PIL import ImageGrab
import win32gui
import win32api
import win32con

currentDirectory = os.path.dirname(os.path.abspath(__file__))
picturesDirectory = currentDirectory + "/gui/pictures/"

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
    
    for picture in pictures:

        search = Search( picturesDirectory + picture )
        
        while 1:
            pos = search.imagesearch();
            print(pos)
            if pos[0] != -1:
                print("début clique")
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)
                print("fin clique")
                time.sleep(3)
            else:
                print("break")
                break
    

if __name__ == '__main__':
    sys.exit(main())