import pygame, json, pickle
import gameutils

pygame.init()

terrain_images = {}

def checkClearance(column,json):
    blocking = None
    blockingType = None
    for i in range(3):
        block = column[i]["block"]
        if block is not None:
            if block not in json["block"]:
                blocking = None
            else:
                blocking = json["block"][block]
                blockingType = column[i]
    return (blocking,blockingType)

def buildLevel(levelID):

    resolution = pygame.display.get_surface().get_size()
    displayRatio = resolution[0]/resolution[1]
    path = './/assets//data//levels//{}'.format(levelID)

    levelF = open(path,"rb")
    levelData = pickle.load(levelF)
    level = levelData[0]
    meta = levelData[1]
    levelF.close()

    jsonF = open('.//assets//data//terrain.json')
    jsonData = json.load(jsonF)
    jsonF.close()

    print(jsonData)

    xSize, ySize = len(level[0]), len(level)
    levelRatio = xSize/ySize

    if levelRatio >= displayRatio:
        blockSize = int(resolution[0]/xSize)
    else:
        blockSize = int(resolution[1]/ySize)

    bg = pygame.Surface((blockSize*xSize,blockSize*ySize))
    tankMask = pygame.Surface((blockSize*xSize,blockSize*ySize),pygame.SRCALPHA)
    bulletMask = pygame.Surface((blockSize*xSize,blockSize*ySize),pygame.SRCALPHA)
    for y in range(ySize):
        for x in range(xSize):
            column = level[y][x]
            for h in range(3):
                item = level[y][x][h]
                block = item["block"]
                rot = item["rotation"]
                if block is not None:
                    bg.blit(pygame.transform.scale(pygame.transform.rotate(terrain_images[block + ".png"],rot), (blockSize, blockSize)), (x * blockSize, y * blockSize))

                blocking, blockingBlock = checkClearance(column,jsonData)

                if blocking == 'bullet':
                    bulletMask.blit(pygame.transform.scale(pygame.transform.rotate(terrain_images[blockingBlock["block"]+".png"],blockingBlock["rotation"]), (blockSize, blockSize)),
                            (x * blockSize, y * blockSize))
                    tankMask.blit(pygame.transform.scale(pygame.transform.rotate(terrain_images[blockingBlock["block"]+".png"],blockingBlock["rotation"]), (blockSize, blockSize)),
                            (x * blockSize, y * blockSize))
                elif blocking == 'tank':
                    tankMask.blit(pygame.transform.scale(pygame.transform.rotate(terrain_images[blockingBlock["block"]+".png"],blockingBlock["rotation"]), (blockSize, blockSize)),
                            (x * blockSize, y * blockSize))

    tankMask = pygame.mask.from_surface(tankMask)
    bulletMask = pygame.mask.from_surface(bulletMask)
    return (bg, tankMask, bulletMask, blockSize, meta)