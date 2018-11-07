from pygame.locals import *
import sys, pygame
import sprites, world
from gameutils import *
import gameobjects

pygame.init()

loaded_sounds = {}

hues = [0,200,100,50,300]

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
    bg, tMask, bMask, blockSize, meta = world.buildLevel(level)
    sprites.scale = int(blockSize / 16)

    bgRect = bg.get_rect()
    bgRect.center = DISPLAYSURF.get_rect().center
    sprites.bulletMask.add(sprites.Mask(bgRect, bMask))
    sprites.tankMask.add(sprites.Mask(bgRect, tMask))

    keys = [[K_w,K_s,K_a,K_d,K_q,K_e,K_f],[K_i,K_k,K_j,K_l,K_u,K_o,K_h]]
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

        ms = clock.tick()

        rects = []
        DISPLAYSURF.fill((0, 0, 0))
        rects.append(DISPLAYSURF.blit(bg, bgRect))

        runTime = pygame.time.get_ticks()
        if fpsUpdate <= 0:
            fpsUpdate = 200
            fps = clock.get_fps()
            pygame.display.set_caption(str(clock.get_fps()))
        else:
            fpsUpdate -= ms

        text.startingPoint(0, 0)
        text.drawText(str(fps), DISPLAYSURF, (255, 0, 0))

        for player in players:
            player.update()


        sprites.tanks.update(ms)
        sprites.bullets.update(ms)
        sprites.airParticles.update(ms)
        sprites.groundParticles.update(ms)
        sprites.groundParticles.draw(DISPLAYSURF)
        sprites.tanks.draw(DISPLAYSURF)
        sprites.bullets.draw(DISPLAYSURF)
        sprites.airParticles.draw(DISPLAYSURF)

        pygame.display.flip()



if __name__ == "__main__":
    DISPLAYSURF = pygame.display.set_mode((1920,1080), DOUBLEBUF | HWSURFACE | FULLSCREEN)
    pygame.display.set_caption('Caption Text...')
    loadImageDirectory(sprites.allImages,"assets//images//sprite",".png")
    loadImageDirectory(world.terrain_images,"assets//images//terrain",".png")


    for i in range(2):
        game(1)