import pygame

class ScreenText(object):
    #Default x & y values
    x = 0
    y = 0

    #funtion used when initiating the class. Has default values which can be overridden
    def __init__(self, font="Arial", size=20, antiAlias=True, sysFont=True):
        self.fontName = font
        self.size = size
        self.sysFont = sysFont

        self.changeFont(font, size, sysFont)

        self.height = self.font.get_height()
        self.antiAlias = antiAlias

    #Sets exact starting point
    def startingPoint(self, newX, newY):
        self.x = newX
        self.y = newY
        
    #sets relatie starting point
    def moveStartingPoint(self, incrementX, incrementY):
        self.x += incrementX
        self.y += incrementY

    #Prints and starts a new line
    def printText(self, text, surface, color=(0, 0, 0)):
        renderedText = self.font.render(text, self.antiAlias, color)
        surface.blit(renderedText, (self.x, self.y))

        self.moveStartingPoint(0, self.height)

    def drawCentered(self, text, surface, color=(0, 0, 0)):
        renderedText = self.font.render(text, self.antiAlias, color)
        textRect = renderedText.get_rect()
        textRect.center = (self.x,self.y)
        surface.blit(renderedText,textRect)

    def printCentered(self, text, surface, color=(0, 0, 0)):
        renderedText = self.font.render(text, self.antiAlias, color)
        textRect = renderedText.get_rect()
        textRect.center = (self.x,self.y)
        surface.blit(renderedText,textRect)

        self.moveStartingPoint(0, self.height)

    #Prints and stays on the same line
    def drawText(self, text, surface, color=(0, 0, 0),onlyY = False):
        renderedText = self.font.render(text, self.antiAlias, color)
        width, height = self.font.size(text)
        if onlyY:
            surface.blit(renderedText, (self.x, self.y - height/2))
        else:
            surface.blit(renderedText, (self.x, self.y))



        self.moveStartingPoint(width, 0)

    #Adjust font properties
    def changeFont(self,fontName = None,size = None,sysFont = None):

        if fontName is None:
            fontName = self.fontName

        if size is None:
            size = self.size

        if sysFont is None:
            sysFont = self.sysFont

        if sysFont:
            self.font = pygame.font.SysFont(fontName, size)
        else:
            self.font = pygame.font.Font(fontName, size)

        self.height = self.font.get_height()

class Button(object):
    pressed = False
    lastState = False
    active = False
    def __init__(self,message,x,y,width = 150,height = 50,centered = True,pulse = True,colors = ((0,130,0),(0, 250, 0),(0,0,0))):

        self.msg = message
        self.colors = colors
        self.pulse = pulse

        self.shape = pygame.Rect(x, y, width, height)
        if centered:
            self.shape.center = (x, y)
        else:
            self.shape.topleft = (x, y)

    def update(self,events,surf,rect):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        mouseX = mouse[0] - rect.x
        mouseY = mouse[1] - rect.y
        if self.shape.left <= mouseX <= self.shape.right and self.shape.top <= mouseY <= self.shape.bottom:
            pygame.draw.rect(surf, self.colors[1], self.shape)

            self.lastState = self.pressed
            if click[0] == 1:
                self.pressed = True
            elif click[0] == 0:
                self.pressed = False

            if self.pulse:
                if self.pressed and self.lastState:
                    self.active = False
                elif self.pressed and not self.lastState:
                    self.active = True
                else:
                    self.active = False
            else:
                self.active = self.pressed

        else:
            pygame.draw.rect(surf, self.colors[0], self.shape)


        pygame.draw.rect(surf, (0,0,0), self.shape, 2)
        buttontext = ScreenText("ARLRDBD.TTF", 25)
        buttontext.startingPoint(self.shape.centerx, self.shape.centery)
        buttontext.drawCentered(self.msg, surf, self.colors[2])

class InputBox(object):
    selected = False
    text = ""
    def __init__(self,x,y,label = "",width = 150,height = 30,centered = False,colors = ((200,200,200),(255, 255, 255),(0,0,0))):
        self.shape = pygame.Rect(x,y,width,height)
        if centered:
            self.shape.center = (x,y)
        else:
            self.shape.topleft = (x,y)
        self.colors = colors
        self.label = label

    def update(self,events,surf,rect):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        display = pygame.display.get_surface()

        if self.shape.left <= mouse[0] <= self.shape.right and self.shape.top <= mouse[1] <= self.shape.bottom:
            if click[0] == 1 and self.selected == False:
                self.selected = True
        else:
            if click[0] == 1:
                self.selected = False

        if self.selected:
            pygame.draw.rect(display, self.colors[1], self.shape)
            keys = get_key(events)
            if keys:
                key, unicode = keys
                if key == "backspace":
                    self.text = self.text[:-1]
                elif key == "return" or key == "escape":
                    self.selected = False
                else:
                    self.text += unicode
        else:
            pygame.draw.rect(display, self.colors[0], self.shape)

        pygame.draw.rect(display, self.colors[2], self.shape, 2)
        buttontext = ScreenText("ARLRDBD.TTF", 25)
        buttontext.startingPoint(self.shape.left + 5, self.shape.centery)
        if self.label:
            buttontext.drawText(self.label+": "+self.text, display, self.colors[2],onlyY=True)
        else:
            buttontext.drawText(self.text, display, self.colors[2], onlyY=True)

class Slider(object):
    def __init__(self,x,y,width=100,height=30,min=0,max=10,interval=1,labelinterval=1):
        self.shape = pygame.Rect(x,y,width,height)
        self.min = min
        self.max = max
        self.difference = max-min
        self.interval = interval
        self.labelinterval = labelinterval
        self.value = int(self.difference/2)+self.min

    def update(self,events,surf,rect):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        display = pygame.display.get_surface()
        labels = ScreenText("ARLRDBD.TTF", 20)

        if self.shape.left <= mouse[0] <= self.shape.right and self.shape.top <= mouse[1] <= self.shape.bottom:
            if click[0] == 1:
                self.value = round((self.difference * (mouse[0]-self.shape.left)/self.shape.width)+self.min)
            pygame.draw.rect(display,(255,255,255),self.shape)
        else:
            pygame.draw.rect(display, (200,200,200),self.shape)

        pygame.draw.rect(display, (150,150,150), self.shape,1)

        fontHeight = labels.font.get_ascent()

        valueX = ((self.value - self.min) * (self.shape.width / self.difference)) + self.shape.left
        pygame.draw.line(display, (50, 50, 255), (valueX, self.shape.top), (valueX, self.shape.bottom - fontHeight - 2), 5)

        for i in range(0,self.max-self.min+1,self.interval):
            xpos = self.shape.left + (i * self.shape.width / self.difference)
            pygame.draw.line(display, (0, 0, 0),
                             (xpos, self.shape.top),
                             (xpos, self.shape.bottom-fontHeight-2))
            if i % self.labelinterval == 0:
                labels.startingPoint(xpos,self.shape.bottom-5)
                labels.drawCentered(str(self.interval*(i+self.min)),display)

def getFonts():
    return pygame.font.get_fonts()

def updateAll(objects, events, surf,rect):
    for obj in objects:
        obj.update(events, surf, rect)

def get_key(events):
    pressed = None
    for event in events:
        if event.type == pygame.KEYDOWN:
            pressed = [pygame.key.name(event.key),event.unicode]
    return pressed
