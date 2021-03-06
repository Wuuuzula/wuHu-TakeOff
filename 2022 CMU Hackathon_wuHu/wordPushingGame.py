###TartanHacks 2022
###Team: wuhuTakeOff
###github: https://github.com/Wuuuzula/wuHu-TakeOff

from tkinter import *
from tkinter.messagebox import *
import copy, string, time, sys
import pygame
from PIL import Image, ImageTk

root = Tk()
root.title("WordPushingGame - Space to Restart")

pygame.init()
#Load music
bgm = "music/Equinoxe.mp3"
wuhu = "music/wuhu.mp3"
moveBox = "music/moveBox.mp3"
walk = "music/walk.mp3"
melting = "music/melting.mp3"
doorOpen = "music/doorOpen.mp3"
pygame.mixer.init()
pygame.mixer.music.load(bgm)
pygame.mixer.Channel(0).play(pygame.mixer.Sound(bgm))

letters=list(string.ascii_uppercase)
walls=['W2','A2','L2','S2','N2','D2','W5','A5','V5','E5','S5']
ice=['I3','C3','E3']
door=['D4','O4','R4','O4-20']

allLetters=dict()
for i in letters:
    allLetters[i]=PhotoImage(file=f"image/UpperLetterImages-White/{i}.png")
for special in [walls,ice,door]:
    for i in special:
        allLetters[i]=PhotoImage(file=f"image/specialBlocks/{i}.png")

allLetters['0']=PhotoImage(file="image/Black.png")
allLetters['me']=PhotoImage(file="image/specialBlocks/me.png")

mes = [PhotoImage(file=("image/specialBlocks/me.gif"),format = 'gif -index %i' % (i)) for i in range(2)]

# Original Map
level = 0
allMapList = [
    [
    ['0', 'W2', 'A2', 'L2', 'L2', 'S2', '0'], 
    ['W2', '0', '0', '0', '0', '0', 'W2'], 
    ['A2', '0', 'M', '0', 'L', '0', 'A2'], 
    ['L2', '0', 'Y', '0', 'I', '0', 'L2'], 
    ['L2', '0', '0', '0', 'K', '0', 'L2'], 
    ['S2', '0', 'H', '0', 'E', '0', 'S2'], 
    ['A2', '0', 'E', '0', '0', '0', 'I3'], 
    ['N2', '0', 'A', '0', 'F', '0', 'C3'], 
    ['D2', '0', 'R', '0', 'R', '0', 'E3'], 
    ['W2', '0', 'T', '0', 'O', '0', 'W2'], 
    ['A2', '0', '0', '0', 'Z', '0', 'A2'], 
    ['L2', '0', 'me', '0', 'E', '0', 'L2'], 
    ['L2', '0', 'S', '0', 'N', '0', 'L2'], 
    ['S2', '0', '0', '0', '0', '0', 'S2'], 
    ['0', 'W2', 'A2', 'L2', 'L2', 'S2', '0']
    ],
    [
    ['0', 'W2', 'A2', 'L2', 'L2', 'S2', '0'], 
    ['W2', '0', '0', '0', '0', '0', 'W2'], 
    ['A2', '0', 'me', '0', 'M', '0', 'A2'], 
    ['L2', '0', '0', '0', 'Y', '0', 'L2'], 
    ['L2', '0', 'L', '0', 'S', '0', 'L2'], 
    ['S2', '0', 'O', '0', 'E', '0', 'S2'], 
    ['A2', '0', 'C', '0', 'L', '0', 'A2'], 
    ['N2', '0', 'K', '0', 'F', '0', 'N2'], 
    ['D2', '0', 'E', '0', '0', '0', 'D2'], 
    ['0', 'W2', 'D', '0', 'U', '0', 'W2'], 
    ['0', 'A2', '0', '0', 'P', '0', 'A2'], 
    ['0', 'L2', 'D4', 'O4', 'O4', 'R4', 'L2'], 
    ['0', 'L2', '0', '0', '0', '0', 'L2'], 
    ['0', 'S2', '0', '0', '0', '0', 'S2'], 
    ['0', '0', '0', '0', '0', '0', '0']
    ],
    [
    ['W5', 'S5', 'E5', 'V5', 'A5', 'W5', 'S5'], 
    ['A5', 'W5', 'S5', 'E5', 'V5', 'A5', 'W5'], 
    ['V5', '0', 'D', '0', 'E5', 'V5', 'A5'], 
    ['E5', '0', 'R', '0', 'S5', 'E5', 'V5'], 
    ['S5', '0', 'O', '0', 'T', '0', 'E5'], 
    ['W5', '0', 'W', '0', 'H', '0', 'S5'], 
    ['A5', '0', 'N', '0', 'E', '0', 'W5'], 
    ['V5', '0', '0', '0', '0', '0', 'A5'], 
    ['E5', '0', 'me', '0', 'S', '0', 'V5'], 
    ['S5', '0', 'N', '0', 'E', '0', 'E5'], 
    ['W5', 'S5', '0', '0', 'A', '0', 'S5'], 
    ['A5', 'W5', 'S5', 'E5', '0', '0', 'W5'], 
    ['V5', 'A5', 'W5', 'S5', 'E5', 'V5', 'A5'], 
    ['E5', 'V5', 'A5', 'W5', 'S5', 'E5', 'V5'], 
    ['S5', 'E5', 'V5', 'A5', 'W5', 'S5', 'E5']
    ]
]

#Letters = boxes
#Letters2/5 = wall/sea
#Letters3 = ice
#Lettera4 = door
#me = player

mapLength, mapWidth = len(allMapList[level]),len(allMapList[level][0])

#create fading effect
images = []  
def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        cv.create_image(x1, y1, image=images[-1], anchor='nw')
    cv.create_rectangle(x1, y1, x2, y2, **kwargs)

def updateIce(): 
    global icy
    create_rectangle(325, 325, 475, 375, fill='black', alpha= 0.2)
    icy = root.after(100,updateIce)

def updateDoor(): 
    global doory
    cv.create_image((650, 150), image=allLetters['O4-20'])
    cv.create_image((650, 300), image=allLetters['O4-20'])
    create_rectangle(575, 175, 625, 275, fill='black', alpha= 0.2)
    doory = root.after(100,updateDoor)

trigger = 0
# Paint the landscape

def drawGameImage():
    global posX, posY
    cv.delete('all')
    for row in range(mapLength):
        for col in range(mapWidth):
            if mapList[row][col] == 'me':
                # Player's position
                posX = row  
                posY = col
            img = allLetters[mapList[row][col]]
            cv.create_image((row * 50+50, col * 50+50), image=allLetters['0'])
            cv.create_image((row * 50+50, col * 50+50), image=img)
            cv.pack()

def update(ind):
    me = mes[ind]
    ind += 1
    if ind >= 2:
        ind = 0
    allLetters['me'] = me
    if trigger!=1: drawGameImage()
    root.after(200, update, ind)

def callback(event):  # Keyboard Control
    global posX, posY, mapList, trigger, icy, doory
    keyPressed = event.keysym
    #Player's current position(posX,y)
    positionDict = {
        "Up" : [0,-1,0,-2],
        "Down" : [0,1,0,2],
        "Left" : [-1,0,-2,0],
        "Right" : [1,0,2,0],
    }

    if keyPressed == "Escape":
        pygame.mixer.Channel(0).stop()
        root.destroy()

    if keyPressed in positionDict:
        moveScale = positionDict[keyPressed]
        x1 = posX+moveScale[0]
        y1 = posY+moveScale[1]
        x2 = posX+moveScale[2]
        y2 = posY+moveScale[3]
        coordinateMove(x1, y1, x2, y2) 

    elif keyPressed == "space": # Press SPACE
        print("Press Space", event.char)
        trigger = 0
        icy = doory = None
        mapList = copy.deepcopy(allMapList[level]) # Reset the map
        drawGameImage()

# Determine whether position is within the frame
def validArea(row, col):
    return (row >= 0 and row < mapLength and col >= 0 and col < mapWidth)

def coordinateMove(x1, y1, x2, y2):
    global posX, posY, trigger, icy, doory
    moveTo = None
    behindeMoveTo = None
    if validArea(x1, y1): 
        moveTo = mapList[x1][y1] 
    if validArea(x2, y2):
        behindeMoveTo = mapList[x2][y2]
    if moveTo == '0':  # Able to move to moveTo
        MoveMan(posX, posY) 
        posX = x1 
        posY = y1 
        mapList[x1][y1] = 'me' 
        pygame.mixer.music.load(walk)
        pygame.mixer.music.play(loops = 0, start=0.0, fade_ms=0)


    if (moveTo in walls) or not validArea(x1, y1):
        # moveTo is wall or out of the game area
        return 
    if moveTo in letters:  # moveTo has a letter
        if (behindeMoveTo in walls) or not validArea(x1, y1) or behindeMoveTo in letters:  ##behindeMoveTo is wall or out of the game area
            return 
    if moveTo in letters and behindeMoveTo == '0':
        MoveMan(posX, posY) 
        posX = x1 
        posY = y1 
        mapList[x2][y2] = moveTo 
        mapList[x1][y1] = 'me'
        pygame.mixer.music.load(moveBox)
        pygame.mixer.music.play(loops = 0, start=0.0, fade_ms=0)

    if level == 0:
        if trigger == 0 and triggerEffect() == True:
            pygame.mixer.music.load(melting)
            pygame.mixer.music.play(loops = 0, start=0.0, fade_ms=0)
            trigger += 1
            updateIce()
            
        elif trigger == 1:
            root.after_cancel(icy)
            icy = None
            trigger += 1
            mapList[6][6] = '0'
            mapList[7][6] = '0'
            mapList[8][6] = '0'

    elif level == 1:
        if trigger == 0 and triggerEffect() == True:
            pygame.mixer.music.load(doorOpen)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(doorOpen))
            trigger += 1
            updateDoor()
            
        elif trigger == 1:
            root.after_cancel(doory)
            doory = None
            trigger += 1
            mapList[12][2] = 'O4'
            mapList[11][3] = '0'
            mapList[11][4] = '0'
            mapList[12][5] = 'O4'
    
    elif level == 2:
        if triggerEffect() == True:
            pygame.mixer.music.stop()
            pygame.mixer.Channel(0).stop()
            pygame.mixer.music.load(wuhu)
            pygame.mixer.music.play(loops = -1, start=0.0, fade_ms=0)
            showinfo(message = f"Wuhu! You've past the whole game!")

    if IsFinish():
        showinfo(message = f"You've Passed Level {level+1}! ")
        nextLevel()
    drawGameImage()
    
def MoveMan(posX, posY):
    if mapList[posX][posY] == 'me':
        mapList[posX][posY] = '0' 

def triggerEffect():
    target = [["HEAT","FIRE"],["KEY"],["AIR"]]
    for words in target[level]:
        length = len(words)
        for col in range(len(mapList[0])):
            for row in range(len(mapList)-length+1):
                secret = ''.join([mapList[row+i][col] for i in range(length)])
                if secret == words:
                    return True
                elif secret == "AmeR" and words == "AIR":
                    return True
                elif secret == "FmeRE" and words == "FIRE":
                    return True
    return False

def IsFinish():  # Whether finish
    global level
    bFinish = False 
    if level == 0:
        if(mapList[6][6] == 'me' or
        mapList[7][6] == 'me'or
        mapList[8][6] == 'me'):
            bFinish = True
    elif level == 1:
        if(mapList[11][3] == 'me' or
        mapList[11][4] == 'me'):
            bFinish = True
    return bFinish

def nextLevel():
    global mapList, level, trigger
    trigger = 0
    level += 1
    mapList = copy.deepcopy(allMapList[level])
    drawGameImage()

cv = Canvas(root, bg='black', width=800, height=400)
mapList = copy.deepcopy(allMapList[level])
drawGameImage()
cv.bind("<KeyPress>", callback)
cv.pack()
cv.focus_set()  # Focus on cv
root.after(0, update, 0)
root.update
root.mainloop()
#Gameover stop the music
