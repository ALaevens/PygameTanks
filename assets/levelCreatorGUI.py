import pickle, sys, os, json
import pygame
import threading
from pygame.locals import *
import gameutils
import gameobjects

pygame.init()

def makeArray(xMax,yMax):
    array = []
    emptyBlock = {"block": None, "rotation": 0}
    for y in range(yMax):
        row = []
        for x in range(xMax):
            row.append([emptyBlock,emptyBlock,emptyBlock])
        array.append(row)
    return array

def makeMetaArray(xMax, yMax):
    array = []
    for y in range(yMax):
        row = []
        for x in range(xMax):
            row.append(None)
        array.append(row)
    return array

def convertMetaOut(meta):
    newMeta = {"spawns" : [None,None,None,None]}
    for y in range(len(meta)):
        for x in range(len(meta[0])):
            if meta[y][x] is not None:
                if "spawn" in meta[y][x]:
                    newMeta["spawns"][int(meta[y][x][-1])-1] = (x,y)
    print(newMeta)
    return newMeta

def convertMetaIn(xSize, ySize, meta):
    array = makeMetaArray(xSize, ySize)
    for i in range(len(meta['spawns'])):
        if meta['spawns'][i] != None:
            spawn = meta["spawns"][i]
            array[spawn[1]][spawn[0]] = "spawn"+str(i+1)
    return array

def drawLevel(height):
    levelSurf.fill((255, 255, 255))
    for y in range(0,ySize):
        for x in range(0,xSize):
            column = worldArray[y][x]
            for i in range(height+1):
                item = column[i]
                block = item["block"]
                rot = item["rotation"]
                if block is not None and block != "":
                    levelSurf.blit(pygame.transform.scale(pygame.transform.rotate(images[block + ".png"], rot),
                                                          (blockSize, blockSize)), (x * blockSize, y * blockSize))
                pygame.draw.rect(levelSurf,(0,0,0),(x*blockSize,y*blockSize,blockSize,blockSize),1)

            meta = metaArray[y][x]
            if meta is not None:
                levelSurf.blit(pygame.transform.scale(pygame.transform.rotate(images[meta + ".png"], rot),
                                                      (blockSize, blockSize)), (x * blockSize, y * blockSize))

def buildPalette():
    terrainPath = ".//images//terrain"
    paletteItems = ["delete"]
    palette.fill((100,100,100))
    for file in os.listdir(terrainPath):
        paletteItems.append(file.split(".")[0])

    paletteItems += metaItems

    pblockSize = int(paletteRect.width/4)
    for i in range(len(paletteItems)):
        x = i%4
        y = i//4
        palette.blit(pygame.transform.scale(images[paletteItems[i]+".png"],(pblockSize,pblockSize)),(x*pblockSize,y*pblockSize))
    return paletteItems

mode,fileName = input("mode flename: ").split()
if mode.lower() == "new":
    xSize = int(input("X Size: "))
    ySize = int(input("Y Size: "))
    worldArray = makeArray(xSize, ySize)
    metaArray = makeMetaArray(xSize, ySize)
elif mode.lower() == "load":
    with open(".//data//levels//{}.lvl".format(fileName), "rb") as f:
        worldData = pickle.load(f)
        print(worldData[1])
        worldArray = worldData[0]
        ySize = len(worldArray)
        xSize = len(worldArray[0])
        metaArray = convertMetaIn(xSize, ySize, worldData[1])

largestSide = max(xSize,ySize)
levelRatio = xSize/ySize
displayRatio = 750/550

if levelRatio >= displayRatio:
    blockSize = int(750/xSize)
else:
    blockSize = int(550/ySize)

DISPLAYSURF = pygame.display.set_mode((1000,600), pygame.DOUBLEBUF)

images = {}
gameutils.loadImageDirectory(images,".//images//terrain",".png")
gameutils.loadImageDirectory(images,".//images//editor",".png")

metaItems = ["metadelete","spawn1", "spawn2", "spawn3", "spawn4"]

levelSurf = pygame.Surface((blockSize*xSize,blockSize*ySize))
levelRect = levelSurf.get_rect()
levelRect.bottomleft = DISPLAYSURF.get_rect().bottomleft

palette = pygame.Surface((250,550))
paletteRect = palette.get_rect()
paletteRect.bottomright = (1000,600)
paletteItems = buildPalette()

slider = gameobjects.Slider(10,10,min=0,max=2)
slider.value = 0
fillButton = gameobjects.Button("Fill",250,10,height=30,centered=False,colors=((0,0,200),(0,0,250),(0,0,0)))
saveButton = gameobjects.Button("Save",450,10,height=30,centered=False)
GUI = [slider,fillButton,saveButton]

with open(".//data//terrain.json") as f:
    jsonData = json.load(f)

mouseHeld = [0,0,0]
selectedBlock = None

rotationIndex = 0
rotations = [0]

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mousePos = pygame.mouse.get_pos()


    DISPLAYSURF.fill((255,255,255))
    gameobjects.updateAll(GUI, events, DISPLAYSURF, DISPLAYSURF.get_rect())
    drawLevel(2)
    DISPLAYSURF.blit(levelSurf, levelRect)
    DISPLAYSURF.blit(palette, paletteRect)

    if levelRect.collidepoint(mousePos):
        if selectedBlock != None:
            DISPLAYSURF.blit(pygame.transform.rotate(gameutils.loadImage(selectedBlock+".png",images,scale=2),rotations[rotationIndex]),mousePos)
        if pygame.mouse.get_pressed()[0]:
            mouseRel = gameutils.subTuple(mousePos, levelRect.topleft)
            locX = mouseRel[0]//blockSize
            locY = mouseRel[1]//blockSize
            if selectedBlock not in metaItems:
                worldArray[locY][locX][slider.value] = {"block":selectedBlock, "rotation": rotations[rotationIndex]}
            else:
                if selectedBlock != "metadelete":
                    metaArray[locY][locX] = selectedBlock
                else:
                    metaArray[locY][locX] = None

    if paletteRect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] and not mouseHeld[0]:
        mouseHeld[0] = 1
        mouseRel = gameutils.subTuple(mousePos, paletteRect.topleft)
        locX = mouseRel[0]//(paletteRect.width//4)
        locY = mouseRel[1]//(paletteRect.width//4)
        selectedIndex = locY*4+locX
        if selectedIndex < len(paletteItems):
            if selectedIndex == 0:
                selectedBlock = None
            else:
                selectedBlock = paletteItems[selectedIndex]
                if selectedBlock in jsonData["rotations"]:
                    rotations = jsonData["rotations"][selectedBlock]
                    print(rotations)
                    rotationIndex = 0
                else:
                    rotations = [0]
                    rotationIndex = 0

    if pygame.mouse.get_pressed()[2] and not mouseHeld[2]:
        rotationIndex += 1
        rotationIndex = rotationIndex%len(rotations)
        mouseHeld[2] = 1

    if not pygame.mouse.get_pressed()[0]:
        mouseHeld[0] = 0

    if not pygame.mouse.get_pressed()[2]:
        mouseHeld[2] = 0

    if saveButton.active:
        print("Clicked")
        with open(".//data//levels//{}.lvl".format(fileName), "wb") as f:
            levelData = [worldArray,convertMetaOut(metaArray)]
            pickle.dump(levelData, f)

    if fillButton.active:
        for row in worldArray:
            for pos in row:
                pos[slider.value] = {"block":selectedBlock, "rotation": rotations[rotationIndex]}

    pygame.display.flip()