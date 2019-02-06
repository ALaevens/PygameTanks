from pygame.locals import *
import sys, pygame
import sprites, world
from gameutils import *
import gameobjects

pygame.init()

loaded_sounds = {}

hues = [0, 200, 100, 50, 300]

class Player(object):
    def __init__(self,hue,pos,keys):
        self.keys = {
            keys[0]: "forward",
            keys[1]: "back",
            keys[2]: "turnLeft",
            keys[3]: "turnRight",
            keys[4]: "aimLeft",
            keys[5]: "aimRight",
            keys[6]: "fire"
        }
        self.sprite = sprites.Tank(pos,hue)

    def update(self):
        pressed = pygame.key.get_pressed()
        for key in self.keys:
            if pressed[key]:
                self.sprite.interact(self.keys[key])


def game(level):
    sprites.reset()
    bg, tMask, bMask, blockSize, meta = world.buildLevel(level)
    sprites.scale = int(blockSize / 16)

    bgRect = bg.get_rect()
    bgRect.center = DISPLAYSURF.get_rect().center

    sprites.bgRect = bgRect
    sprites.bulletMask.add(sprites.Mask(bgRect, bMask))
    sprites.tankMask.add(sprites.Mask(bgRect, tMask))

    keys = [[K_w, K_s, K_a, K_d, K_q, K_e, K_f], [K_i, K_k, K_j, K_l, K_u, K_o, K_h]]
    players = []
    fpsUpdate = 0

    for i in range(2):
        spawnPos = meta["spawns"][i]
        players.append(Player(hues[i],(spawnPos[0]*blockSize+bgRect.left+blockSize/2,spawnPos[1]*blockSize+bgRect.top+blockSize/2),keys[i]))

    for player in players:
        sprites.tanks.add(player.sprite)

    clock = pygame.time.Clock()

    text = gameobjects.ScreenText()

    fps = 0

    play = True
    while play:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RIGHT:
                    play = False

        ms = clock.tick()

        DISPLAYSURF.fill((0, 0, 0))
        DISPLAYSURF.blit(bg, bgRect)

        runTime = pygame.time.get_ticks()
        if fpsUpdate <= 0:
            fpsUpdate = 200
            fps = clock.get_fps()
        else:
            fpsUpdate -= ms

        text.startingPoint(0, 0)
        text.drawText("FPS: {}".format(int(fps)), DISPLAYSURF, (255, 0, 0))

        for player in players:
            player.update()


        if len(sprites.tanks.sprites()) <= 1 and len(sprites.airParticles.sprites()) == 0:
            play = False

        sprites.tanks.update(ms)
        sprites.bullets.update(ms)
        sprites.airParticles.update(ms)
        sprites.groundParticles.update(ms)
        sprites.groundParticles.draw(DISPLAYSURF)
        sprites.tanks.draw(DISPLAYSURF)
        sprites.bullets.draw(DISPLAYSURF)
        sprites.airParticles.draw(DISPLAYSURF)

        pygame.display.flip()

def controls():
    displaySize = pygame.display.get_surface().get_size()
    backButton = gameobjects.Button("Back", displaySize[0] //2,
                                    displaySize[1]-25,
                                    displaySize[0]//6,
                                    colors=(colors["DRED"], colors["LRED"],
                                            colors["BLACK"]))
    gui = [backButton]

    textLayer = pygame.Surface(displaySize, SRCALPHA)
    textWriter = gameobjects.ScreenText()
    textWriter.startingPoint(0,0)
    with open("assets//data//controls.txt") as f:
        for line in f:
            textWriter.printText(line.rstrip(), textLayer)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        DISPLAYSURF.fill((colors["SKYBLUE"]))
        DISPLAYSURF.blit(textLayer,(0,0))

        if backButton.active:
            break

        gameobjects.updateAll(gui, events, DISPLAYSURF, DISPLAYSURF.get_rect())
        pygame.display.flip()

def menu():
    displaySize = pygame.display.get_surface().get_size()

    bottom = pygame.image.load("assets//images//extra//menufloor.png").convert_alpha()
    scaleAmount = displaySize[0]/bottom.get_width()
    bottom = pygame.transform.scale(bottom,(displaySize[0],int(bottom.get_height()*scaleAmount)))

    title = pygame.image.load("assets//images//extra//title.png").convert_alpha()
    scaleAmount = (3*displaySize[0]//4) / title.get_width()
    title = pygame.transform.scale(title, (3*displaySize[0]//4, int(title.get_height() * scaleAmount)))
    titleRect = title.get_rect()
    titleRect.center = (displaySize[0]//2, displaySize[1]//4)

    startButton = gameobjects.Button("Start", 1*displaySize[0]//3, 2*displaySize[1]//3,
                                     displaySize[0]//4)
    helpButton = gameobjects.Button("Controls", 2 * displaySize[0]//3,
                                    2*displaySize[1]//3, displaySize[0]//4,
                                    colors=(colors["DRED"], colors["LRED"], colors["BLACK"]))
    gui = [startButton, helpButton]

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        DISPLAYSURF.fill((colors["SKYBLUE"]))
        DISPLAYSURF.blit(bottom,(0,displaySize[1]-bottom.get_height()))
        DISPLAYSURF.blit(title, titleRect)

        if startButton.active:
            for i in os.listdir("assets//data//levels"):
                game(i)
            startButton.active = False

        if helpButton.active:
            controls()
            helpButton.active = False

        gameobjects.updateAll(gui, events, DISPLAYSURF, DISPLAYSURF.get_rect())
        pygame.display.flip()


if __name__ == "__main__":
    DISPLAYSURF = pygame.display.set_mode((1280,720), DOUBLEBUF)
    pygame.display.set_caption('Tanks')
    loadImageDirectory(sprites.allImages,"assets//images//sprite",".png")
    loadImageDirectory(world.terrain_images,"assets//images//terrain",".png")

    menu()
