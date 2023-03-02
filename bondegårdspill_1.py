import pygame as pg

# Konstanter
WIDTH = 1000  # bredden til vinduet
HEIGHT = 600 # høyden til vinduet
SIZE = (WIDTH, HEIGHT) # størrelsen til vinduet

FPS = 60 # frames per second (bilder per sekund)

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# henter inn bakgrunnsbilde (med dimensjoner 384 × 224)
backgroundImg = pg.image.load("TileableBackGround.png")

#skalerer bakgrunnsbilde
backgroundImg = pg.transform.scale(backgroundImg, (1000,600))


def load_sprite_sheets(dir1,dir2, width, height, direction=False):


# klasse for karakteren
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.characterImg = pg.image.load("hatman.png")
        
        #får høyden og bredden til karakteren
        self.characterRect = self.characterImg.get_rect()
        self.h = self.characterRect.height
        self.w = self.characterRect.width
        
        self.vx = 0
        self.vy = 0
        
    
    def draw(self):
        surface.blit(self.characterImg, (self.x, self.y))
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    
    def move(self):
        self.vx = 0
        self.vy = 0
        
        keys  = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -5
            
        if keys[pg.K_RIGHT]:
            self.vx = 5
        
        if keys[pg.K_UP]:
            self.vy = -5
        
        if keys[pg.K_DOWN]:
            self.vy = 5


#hatman objekt
hatman = Character(40, 430)





# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
    # Løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekket om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
        
    
    # legger bakgrunnsbilde på skjermen
    surface.blit(backgroundImg, (0,0))
    
    
    #oppdaterer posisjonen
    hatman.update()
    #beveger seg
    hatman.move()
    #tegner hatman til skjermen
    hatman.draw()
    
    # Etter vi har tegner alt, "flipper" vi displayet
    pg.display.flip()


# Avslutter pygame
pg.quit()



