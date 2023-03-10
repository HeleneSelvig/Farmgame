import pygame as pg

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
        
    def get_image(self, frame, width, height, scale, direction):
        if direction == "up":
            y = height*0
        if direction == "right":
            y = height*1
        if direction == "down":
            y = height*2
        if direction == "left":
            y = height*3
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width), y, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
    
    
        return image


#vi sier rektangelet rundt høna er 26x26
#hvert rektangel er 48x64 eller 62
    #64-26 = 38
    #48-26 = 22, 22/2 = 11


class SpriteSheetChick():
    def __init__(self, image):
        self.sheet = image
        
    def get_image(self, frame, width, height, scale, direction):
        if direction == "up":
            y = 38
        if direction == "right":
            y = 38+62
        if direction == "down":
            y = 38+124
        if direction == "left":
            y = 38+184
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame*48 + 11), y, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
    
    
        return image