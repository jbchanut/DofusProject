import os
import win32api
import win32con
import win32gui
import time

# Définition des chemins absolue
currentDir = os.path.dirname(os.path.abspath(__file__))
savesDir = currentDir + '\saves'

def Load_Save(save):
    hwnd = win32gui.GetDC(0)
    
    print('Ouverture du fichier ' + savesDir + '\\' + save)
    f = open(savesDir + '\\' + save, "r")
    for line in f:
        print(line)
        col = line.split(';')
        sleepTime = 0.01 * int(col[0])
        time.sleep(sleepTime / 2)
        win32api.SetCursorPos((int(col[2]), int(col[3])))
        time.sleep(sleepTime / 2)
        win32api.mouse_event(int(col[1]) ,0, 0, 0, 0)
        
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP ,0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP ,0, 0, 0, 0)


def New_Save(saveName):
    path = savesDir + '\\' + saveName + '.xml'
    
    f = open(path, "x")
    
    i = 0
    l = left = win32api.GetKeyState(0x01)
    r = right = win32api.GetKeyState(0x02)
    while left >= 0 or right >= 0:
        if left != l:
            x, y = win32api.GetCursorPos()
            line = str(i) + ';' + str(win32con.MOUSEEVENTF_LEFTDOWN if l < 0 else win32con.MOUSEEVENTF_LEFTUP) + ';' + str(x) + ';' + str(y) + '\n'
            f.write(line)    
            print(line, end="")
            i = 0
            left = l
        elif right != r:
            if not r < 0:
                x, y = win32api.GetCursorPos()
                line = str(i) + ';' + str(win32con.MOUSEEVENTF_RIGHTDOWN if r < 0 else win32con.MOUSEEVENTF_RIGHTUP) + ';' + str(x) + ';' + str(y) + '\n'
                f.write(line)    
                print(line, end="")      
                i = 0       
            right = r        
        else:
            time.sleep(0.01)
            i = i + 1
            
        l = win32api.GetKeyState(0x01)
        r = win32api.GetKeyState(0x02)
    
    
    f.close()
    

def Main():
    # Créer le fichier de sauvegardes s'il n'existe pas
    if not os.path.isdir(savesDir):
        os.mkdir(savesDir)
        print('Création du dossier \"saves\" car inexistant')

    # Demande quoi faire
    saves = os.listdir(savesDir)
    print('0. Créer une nouvelle sauvegarde')
    if len(saves):
        i = 1
        for save in saves:
            print(i, ". ", save.split('.')[0])
            i = i + 1
    try:
        resp = int(input('\n'))
    except ValueError:
        print(ValueError)
    finally:
    
        if(resp):
            # Lancer la sauvegarde demandé
            Load_Save(saves[resp - 1])
        else:
            # Création d'une nouvelle sauvegarde
            saveName = input('\nNom de la nouvelle sauvegarde ?\n')
            ret = New_Save(saveName)
            if not ret:
                print(saveName, ' a bien été créé.')
            else: 
                print('Erreur de création: ', ret, '.')
            
    
if __name__ == '__main__':
    while True:
        Main()