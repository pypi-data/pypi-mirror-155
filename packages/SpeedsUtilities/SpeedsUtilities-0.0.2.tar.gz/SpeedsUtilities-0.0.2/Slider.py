import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 30)

class slider:
    def __init__(self,x,y,text,colorOfText,screen,sliderIMG,barIMG):
        super().__init__()
        self.image = sliderIMG
        self.bar = barIMG
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.barRect = self.bar.get_rect()
        self.barRect.center = [x,y]
        self.value = 127.5
        self.held = False
        self.text = font.render(text,True,colorOfText)
        self.valueText = font.render(str(self.value),True,colorOfText)
        self.valueString = "value here"
        self.screen = screen
        self.colorOfText = colorOfText
    def update(self):
        self.rect.clamp_ip(self.barRect)
        self.screen.blit(self.bar,(self.barRect.x,self.barRect.y))
        self.screen.blit(self.image,(self.rect.x,self.rect.y))
        self.screen.blit(self.text , (self.barRect.right + 20, self.barRect.y - 10))
        pos = pygame.mouse.get_pos()

        self.value = (self.rect.x - self.barRect.left) * 2
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.held = True

        if pygame.mouse.get_pressed()[0] == 0:
                self.held = False

        if (self.held):
                self.rect.x = pos[0] - 8
                if self.rect.x > self.barRect.right - 14:
                    self.rect.x = self.barRect.right - 14
                    self.value = 255

                if self.rect.x < self.barRect.left:
                    self.rect.x = self.barRect.left
        self.valueString = str(self.value)
        self.valueText = font.render(self.valueString,True,self.colorOfText)

        self.screen.blit(self.valueText , (self.barRect.x + 50, self.barRect.y - 40))