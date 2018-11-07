import pickle, sys, os
import pygame
import threading
from pygame.locals import *
import gameutils

pygame.init()

xSize = int(input("X Size: "))
ySize = int(input("Y Size: "))


largestSide = max(xSize,ySize)
blockSize = int(600/largestSide)

images = {}

def makeArray(xMax,yMax):
    array = []
    for y in range(yMax):
        row = []
        for x in range(xMax):
            row.append([None,None,None])
        array.append(row)
    return array

def blockPreview(spot):
    shortHand = ""
    for layer in spot:
        if layer is None:
            shortHand += " "
        else:
            shortHand += str(layer)[0].upper()
    return shortHand

def printArray(array):
    for row in array:
        for item in row:
            print("[{}]".format(blockPreview(item)),end="")
        print()

worldArray = makeArray(xSize,ySize)

def commandHandler():
    while True:
        command = input("> ")
        #fill 0 1 6 6 0 mud
        if command !=  "":
            command = command.split()
            if command[0] == "fill":
                for y in range(int(command[2])-1, int(command[4])):
                    for x in range(int(command[1])-1, int(command[3])):
                        if command[6] == "None":
                            worldArray[y][x][int(command[5])] = None
                        else:
                            worldArray[y][x][int(command[5])] = command[6]

            if command[0] == "save":
                with open(".//images//terrain//{}.lvl".format(command[1]),"wb") as f:
                    pickle.dump(worldArray,f)

        else:
            break


DISPLAYSURF = pygame.display.set_mode((800,600), pygame.DOUBLEBUF)
gameutils.loadImageDirectory(images,".//images//terrain",".png")

t = threading.Thread(target=commandHandler)
t.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill((255,255,255))

    for y in range(0,ySize):
        for x in range(0,xSize):
            column = worldArray[y][x]
            for item in column:
                if item is not None:
                    DISPLAYSURF.blit(pygame.transform.scale(images[item+".png"],(blockSize,blockSize)),(x*blockSize,y*blockSize))
                pygame.draw.rect(DISPLAYSURF,(0,0,0),(x*blockSize,y*blockSize,blockSize,blockSize),2)


    pygame.display.flip()