import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 30)

class button:
    def __init__(self,x,y,text_x,text_y,text,colorOfText,screen,image,startingValue,codeToExecute,isTextInCentre):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.displayed_text = font.render(text,True,colorOfText)
        self.text = text
        self.screen = screen
        self.value = startingValue
        self.onPress = codeToExecute
        self.colorOftext = colorOfText
        self.text_x = text_x
        self.text_y = text_y
        self.rectText = self.displayed_text.get_rect()
        self.rectText.center = [x,y]
        self.isHeld = False
        self.isTextInCentre = isTextInCentre
    def update(self):
        self.screen.blit(self.image,(self.rect.x,self.rect.y))

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.isHeld == False:
                    self.onPress()
                    self.isHeld = True

        if  pygame.mouse.get_pressed()[0] == 0:
            self.isHeld = False

        
        if self.isTextInCentre ==  True:
            self.screen.blit(self.displayed_text , (self.rectText.x, self.rectText.y))
        else:
            self.screen.blit(self.displayed_text , (self.text_x, self.text_y))