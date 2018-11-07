import pygame, os, math

pygame.init()

colors = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "DGREY": (45, 45, 45),
    "LGREY": (175, 175, 175),
    "DRED": (160, 0, 0),
    "LRED": (255, 0, 0),
    "ORANGE": (255, 165, 0),
    "YELLOW": (255, 255, 0),
    "LGREEN": (0, 255, 0),
    "DGREEN": (7, 112, 0),
    "CYAN": (0, 255, 200),
    "LBLUE": (0, 97, 255),
    "DBLUE": (0, 0, 114),
    "MAGENTA": (183, 0, 159),
    "SKYBLUE": (9, 16, 28)
}

def loadImage(filename, loaded_images, colorKey=None, scale=None):
    if filename in loaded_images:
        image = loaded_images[filename]

    else:
        image = pygame.image.load(filename)
        loaded_images[filename] = image

    imageRect = image.get_rect()

    if colorKey:
        image.set_colorkey(colors[colorKey])

    if scale:
        image = pygame.transform.scale(image, (int(imageRect.width * scale), int(imageRect.height * scale)))

    return image


def loadImageDirectory(loaded_images, directory, imType):
    # print("Loading Directory...." + directory)
    for file in os.listdir(directory):
        checkFolder = file.split(".")
        if len(checkFolder) <= 2:
            splitFile = file.split("//")
            fileName = file.split("//")[len(splitFile) - 1]
            if imType in fileName:
                image = pygame.image.load(os.path.join(directory, fileName))
                image.convert_alpha()
                loaded_images[fileName] = image
                print("Loaded Image:", fileName)

def loadSoundDirectory(loaded_sounds, directory, fType):
    for file in os.listdir(directory):
        checkFolder = file.split(".")
        if len(checkFolder) <= 2:
            splitFile = file.split("//")
            fileName = file.split("//")[len(splitFile) - 1]
            if fType in fileName:
                sound = pygame.mixer.Sound(os.path.join(directory, fileName))
                loaded_sounds[fileName] = sound
                print("Loaded Sound:", fileName)

def scalePx(pos,scale):
    new = []
    for dim in pos:
        new.append(dim*scale)

    return tuple(new)

def hsvHue(greyimage,hue):
    image = greyimage.copy()
    xMax, yMax = image.get_size()
    for x in range(xMax):
        for y in range(yMax):
            color = image.get_at((x,y))
            if color != (0,0,0,0):
                if color.r == color.b and color.r == color.g:
                    color.hsva = (hue, 100, color.r,100)
            image.set_at((x,y),color)

    return image

def hsvRGB(h,s,v):
    color = pygame.Color(0,0,0,255)
    color.hsva = (h,s,v,100)

    return color

def trigOffset(length,angle):
    offset = (length*math.cos(math.radians(angle)),-1*length*math.sin(math.radians(angle)))
    return offset

def addTuple(a,b):
    new = []
    for i in range(len(a)):
        new.append(a[i]+b[i])
    return tuple(new)

def subTuple(a,b):
    new = []
    for i in range(len(a)):
        new.append(a[i] - b[i])
    return tuple(new)

def colorWithAlpha(colorName, opacity):
    return pygame.Color(colors[colorName][0], colors[colorName][1], colors[colorName][2], opacity)

def checkAlive(spriteGroup):
    aliveList = []
    for sprite in spriteGroup.sprites():
        if sprite.alive:
            aliveList.append(sprite)
    return aliveList