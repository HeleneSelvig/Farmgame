#nyeste forsøk startet 9. mars, kode kopiert fra funker_pughøne_musikk_hønsehus.py
#legger til kollisjon mellom høne og pug, og mellom høne og hønsehus, og en vinn-funksjon
#prøver å få kollisjon mellom pug og hønsehus

# bakgrunn av LuminousDragonGames, hentet fra https://opengameart.org/content/perfectly-seamless-grass
# pug-animasjon av AntumDeluge, hentet fra https://opengameart.org/content/pug-rework
# høne-animasjon av AntumDeluge, hentet fra https://opengameart.org/content/chick
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/  tekst

import pygame as pg
import spritesheet

# Konstanter
WIDTH = 1000  # bredden til vinduet
HEIGHT = 600 # høyden til vinduet
SIZE = (WIDTH, HEIGHT) # størrelsen til vinduet

#BLUE = (0,0,150)
BLUE = (80,210,240)
WHITE = (255,255,255)


# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)


# henter inn bakgrunnsbilde (med dimensjoner 384 × 224)
backgroundImg = pg.image.load("bilder/TileableBackGround.png")

#skalerer bakgrunnsbilde
backgroundImg = pg.transform.scale(backgroundImg, (1000,600))

#laster inn musikkfilen
#pg.mixer.music.load("Casual game track.ogg")
#spiller musikk (-1 ganger gir evig)
#pg.mixer.music.play(loops=-1)


#henter font og skriftstørrelse
font = pg.font.SysFont("Arial",48)


#SPRITESHEETS fra coding with russ youtube
sprite_sheet_image = pg.image.load("bilder/pug-001.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

sprite_sheet_image2 = pg.image.load("bilder/chick.png").convert_alpha()
sprite_sheet2 = spritesheet.SpriteSheetChick(sprite_sheet_image2)


# create animation list
animation_steps = 3
# lager en timer som sier hvor ofte animasjonen skal endre
last_update = pg.time.get_ticks()
# i millisekunder
animation_cooldown = 100










# klasse for karakteren
class Character:
    def __init__(self, x, y, image, direction, size, scale, sprite_sheet):
        self.x = x
        self.y = y
        self.image = image
        self.size = size
        self.scale = scale
        self.sprite_sheet = sprite_sheet
        
        #laster inn bilde
        self.characterImg = pg.image.load(image)
        
        #får høyden og bredden til karakteren
        self.characterRect = self.characterImg.get_rect()
        self.h = self.characterRect.height
        self.w = self.characterRect.width
        
        self.vx = 0
        self.vy = 0
        #retning den begynner i 
        self.direction = direction
        self.last_update = 0
        self.frame = 0
        
    
    def draw(self):
        #tom liste for hvilken frame vi skal vise
        animation_list = []
        for i in range(animation_steps):
            animation_list.append(self.sprite_sheet.get_image(i, self.size, self.size, self.scale, self.direction))
        
        
        # update animation
        current_time = pg.time.get_ticks()
        #oppdaterer seg hvis det har gått lengre tid enn cooldownen
        if current_time - self.last_update >= animation_cooldown:
            #sier at den kun skal endre frames om karakteren beveger seg
            if not(self.vy == 0 and self.vx == 0):
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(animation_list):
                    self.frame = 0
            
        surface.blit(animation_list[self.frame], (self.x, self.y))
        #surface.blit(self.characterImg, (self.x, self.y))
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
       


class Pug(Character):
    def __init__(self, x, y, image, direction, size, scale, sprite_sheet):
        super().__init__(x, y, image, direction, size, scale, sprite_sheet)
        self.hidden = False
    
    def move(self):
        self.vx = 0
        self.vy = 0
       
        
        keys  = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.direction = "left"
            #gir kollisjon med venstre vegg
            if self.x > 0:
                #gir fart mot venstre
                self.vx = -4
        
        #elif gjør at den ikke kan gå på skrå, men også at vi kun har én direction-verdi lagret
        elif keys[pg.K_RIGHT]:
            self.direction = "right"
            #gir kollisjon med høyre vegg
            if self.x + self.size + 11 < WIDTH:
                #gir fart mot høyre
                self.vx = 4
        
        elif keys[pg.K_UP]:
            self.direction = "up"
            #gir kollisjon med toppen
            if self.y + 11 > 0:
                #gir fart oppover
                self.vy = -4
        
        elif keys[pg.K_DOWN]:
            self.direction = "down"
            #gir kollisjon med bunnen
            if self.y + self.size + 11 < HEIGHT:
                #gir fart nedover
                self.vy = 4
        
        
        # sjekk om pug's rect etter flytting ville kollidert
        #ny_rect = self.characterRect.copy()
        #ny_rect.x = self.x + self.vx
        #ny_rect.y = self.y + self.vy
        ny_rect = pg.Rect(
            self.x + self.vx,
            self.y + self.vy,
            self.size * self.scale,
            self.size * self.scale)
        
        if pg.Rect.colliderect(ny_rect, honsehus.rektangelRect):
            if self.direction in ("up", "down"):
                self.vy = 0
            if self.direction in ("left", "right"):
                self.vx = 0
        
        
    




class Chick(Character):
    def __init__(self, x, y, image, direction, size, scale, sprite_sheet):
        super().__init__(x, y, image, direction, size, scale, sprite_sheet)
        self.hidden = False
    
    def move(self):
        self.vx = 0
        self.vy = 0
       
        
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction = "left"
            #gir kollisjon med venstre vegg
            if self.x > 0:
                #gir fart mot venstre
                self.vx = -4
            
        elif keys[pg.K_d]:
            self.direction = "right"
            #gir kollisjon med høyre vegg
            if self.x + self.size + 11 < WIDTH:
                #gir fart mot høyre
                self.vx = 4
        
        elif keys[pg.K_w]:
            self.direction = "up"
            #gir kollisjon med toppen
            if self.y + 11 > 0:
                #gir fart oppover
                self.vy = -4
        
        elif keys[pg.K_s]:
            self.direction = "down"
            #gir kollisjon med bunnen
            if self.y + self.size + 22 < HEIGHT:
                #gir fart nedover
                self.vy = 4




#pug objekt
pug = Pug(500, 300, "bilder/pug-001.png", "left", 32, 1.5, sprite_sheet)

#chick objekt
chick = Chick(200, 300, "bilder/chick.png", "right", 26, 2, sprite_sheet2)







class Rektangel:
    def __init__(self, x, y, w, h, image, scale):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.scale = scale
        self.rektangelImg = pg.image.load(self.image)
        self.rektangelImg = pg.transform.scale(self.rektangelImg, (self.w * self.scale, self.h * self.scale))
        self.rektangelRect = self.rektangelImg.get_rect()
        self.rektangelRect.x = x
        self.rektangelRect.y = y
        self.h = self.rektangelRect.height
        self.w = self.rektangelRect.width
        
    def draw(self):
        #self.rektangelImg = pg.transform.scale(self.rektangelImg, (self.w * self.scale, self.h * self.scale))
        surface.blit(self.rektangelImg, (self.x, self.y))



honsehus = Rektangel(700,200,50,50, "bilder/honsehus.png", 4)




textPug = font.render("Pug vinner!", True, WHITE,BLUE)
textRectPug = textPug.get_rect()
textRectPug.center = (WIDTH // 2, HEIGHT // 2)
textChick = font.render("Kylling vinner!", True, WHITE,BLUE)
textRectChick = textChick.get_rect()
textRectChick.center = (WIDTH // 2, HEIGHT // 2)



#kvadratet til kyllingen er smått avvikende fra kyllingens faktiske størrelse
#kyllingen er ikke inne i buret før pug forsvinner
def collisionChickHonsehus(chick, honsehus):
    if chick.x + chick.size - 11 >= honsehus.x and chick.x + 38 <= honsehus.x + honsehus.w:
        if chick.y + chick.size >= honsehus.y and chick.y + 38 <= honsehus.y + honsehus.h:
            #pug skal bli borte
            pug.hidden = True
            #skriver vinnertekst
            surface.blit(textChick, textRectChick)
     

#det er små problemer her i når pugen treffer kylling - tar litt tid før den treffer nedenfra
def collisionPugChick(pug, chick):
    if chick.x + chick.size >= pug.x and chick.x <= pug.x + pug.size:
        if chick.y + chick.size >= pug.y and chick.y <= pug.y + pug.size:
            #kylling blir borte
            chick.hidden = True
            #skriver vinnertekst
            surface.blit(textPug, textRectPug)
            






# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekket om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
        
    
    # legger bakgrunnsbilde på skjermen
    surface.blit(backgroundImg, (0,0))
    
    collisionChickHonsehus(chick, honsehus)
    collisionPugChick(pug, chick)
    
    #tegner hønsehus
    honsehus.draw()
    
    #så lenge høna ikke har tapt skal den vises og oppdateres
    if not chick.hidden:
        #oppdaterer posisjonen
        chick.update()
        if not pug.hidden:
            #beveger seg
            chick.move()
        #tegner høne til skjermen
        chick.draw()
    #hvis høna vinner skal den stå stille
    if pug.hidden:
        chick.vx = 0
        chick.vy = 0
    
    if not pug.hidden:
        pug.update()
        if not chick.hidden:
            pug.move()
        pug.draw()
    if chick.hidden:
        pug.vx = 0
        pug.vy = 0
    
    
    # Etter vi har tegner alt, "flipper" vi displayet
    pg.display.flip()



# Avslutter pygame
pg.quit()








#poengsystem, tilfeldig plassering av spillbrikker, resettes, bytte karakterer
#evt to forskjellige konfigurasjoner, at pug høne og hønsehus tilfeldig plasseres i en range
#pug skal ikke kunne gå inn i hønsehuset

#nevne i presentasjon at f.eks. tallet 11, 38 og så videre har med formen til kyllingen å gjøre og er regnet ut


