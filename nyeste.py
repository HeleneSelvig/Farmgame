# nyeste forsøk startet 10. mars, kode kopiert fra funker_manglerhøyball.py
# prøver å legge til høyballer og kollisjon mellom høyball, pug og kylling

# bakgrunn av LuminousDragonGames, hentet fra https://opengameart.org/content/perfectly-seamless-grass
# pug-animasjon av AntumDeluge, hentet fra https://opengameart.org/content/pug-rework
# høne-animasjon av AntumDeluge, hentet fra https://opengameart.org/content/chick
# musikk av Alexandr Zhelanov, hentet fra https://opengameart.org/content/casual-game-track
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/  tekst
# høyballer og hønsehus tegnet av Thea

#disclaimer: noen av tallene i kollisjonene og for karakterene (spesielt i spritesheet-klassene), som at vi sier +11 og +38 osv., er regnet ut fordi det i spritesheetene er mellomrom mellom karakterene som gjør rektanglene deres større enn ønskelig
    #tallene har derfor kun betydning for akkurat de bildene vi bruker, og utregningene vi har gjort


"""
OM SPILLET:
Dette er et spill for to spillere. En spiller er kyllingen, og en er hunden.
De to karakterene har forskjellige mål for å vinne spillet:
    Kyllingen sitt mål er å komme seg gjennom gjerdet i hønsehuset, slik at den er trygg
    Hundens mål er å ta kyllingen, og stoppe den fra å komme til hønsehuset
Underveis ligger det hindringer som karakterene må komme seg forbi.

Lykke til!
"""






# importerer pygame-biblioteket
import pygame as pg
# importerer filen der spritesheet-klassen ligger
import spritesheet

# Konstanter
WIDTH = 1000  # bredden til vinduet
HEIGHT = 600 # høyden til vinduet
SIZE = (WIDTH, HEIGHT) # størrelsen til vinduet

BLUE = (80,210,240)
WHITE = (255,255,255)


# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)


# henter inn bakgrunnsbilde (med dimensjoner 384 × 224)
backgroundImg = pg.image.load("bilder/TileableBackGround.png")

#skalerer bakgrunnsbilde til ønsket størrelse
backgroundImg = pg.transform.scale(backgroundImg, (1000,600))


#laster inn musikkfilen
pg.mixer.music.load("Casual game track.ogg")
#spiller musikken (-1 ganger gir at den loopes evig)
pg.mixer.music.play(loops=-1)


#henter font og skriftstørrelse
font = pg.font.SysFont("Arial",48)


#SPRITESHEETS, med hjelp fra coding with russ på youtube
#henter først spritesheetet med 12 pug-bilder (convert_alpha gjør at bildet bruker samme pixel-format som skjermen)
sprite_sheet_image = pg.image.load("bilder/pug-001.png").convert_alpha()
#sender spritesheetet gjennom SpriteSheet-klassen, slik at det blir skalert og delt opp i 12 enkeltbilder
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

#henter spritesheetet med 12 kylling-bilder
sprite_sheet_image2 = pg.image.load("bilder/chick.png").convert_alpha()
#skalerer og deler opp spritesheetet i 12 enkeltbilder
sprite_sheet2 = spritesheet.SpriteSheetChick(sprite_sheet_image2)


# lager en liste som sier hvor mange bilder det er i hver animasjon
animation_steps = 3
# lager en timer som sier hvor ofte animasjonen skal endre
last_update = pg.time.get_ticks()
# i millisekunder
animation_cooldown = 100






# klasse for karakteren
class Character:
    # konstruktør
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
        
        #setter en x- og y-fart til karakteren
        self.vx = 0
        self.vy = 0
        
        #retning den begynner å peke i
        self.direction = direction
        #lengde siden sist gang animasjonen oppdaterte seg begynner på 0 millisekunder når programmet kjøres
        self.last_update = 0
        #begynner på det første bildet i animasjonen
        self.frame = 0
        
    
    #lager en metode som tegner karakteren til skjermen
    def draw(self):
        #tom liste for hvilken frame vi skal vise
        animation_list = []
        #itererer gjennom bildene i animasjonen og legger det til i listen, slik at vi vet hvor langt vi er kommet i animasjonen
        for i in range(animation_steps):
            animation_list.append(self.sprite_sheet.get_image(i, self.size, self.size, self.scale, self.direction))
        
        
        # henter hvor lang tid det har gått akkurat nå
        current_time = pg.time.get_ticks()
        #oppdaterer seg hvis det har gått lengre tid enn cooldownen
        if current_time - self.last_update >= animation_cooldown:
            #sier at den kun skal endre frames om karakteren beveger seg
            if not(self.vy == 0 and self.vx == 0):
                #sier at vi skal til neste frame
                self.frame += 1
                #oppdaterer tiden slik at cooldown starter på nytt
                self.last_update = current_time
                #hvis vi er på siste frame, starter animasjonen på nytt
                if self.frame >= len(animation_list):
                    self.frame = 0
        
        #tegner animasjonen til skjerm
        surface.blit(animation_list[self.frame], (self.x, self.y))
       
    
    #metode som oppdaterer posisjonen til karakteren
    def update(self):
        self.x += self.vx
        self.y += self.vy
       


#lager en klasse for pug-karakteren som arver av karakter-klassen
class Pug(Character):
    #konstruktør
    def __init__(self, x, y, image, direction, size, scale, sprite_sheet):
        super().__init__(x, y, image, direction, size, scale, sprite_sheet)
        # sier at karakteren ikke er skjult, og den skal derfor vises - bruker dette lengre ned i programmet
        self.hidden = False
        
    
    #metode som gjør at karakteren kan bevege seg
    def move(self):
        #gir fart = 0 her slik at figuren står stille når ingen knapper trykkes
        self.vx = 0
        self.vy = 0
       
        #henter inn status på tastaturknappene - om de blir trykket på
        keys  = pg.key.get_pressed()
        
        #sjekker om venstre piltast trykkes på
        if keys[pg.K_LEFT]:
            #setter karakterens retning til å gå mot venstre
            self.direction = "left"
            #gir kollisjon med venstre vegg
            if self.x > 0:
                #gir fart mot venstre
                self.vx = -4
        
        #elif gjør at den ikke kan gå på skrå, men også at vi kun har én direction-verdi lagret om gangen
        #sjekker om høyre piltast trykkes på
        elif keys[pg.K_RIGHT]:
            #setter karakterens retning til å gå mot høyre
            self.direction = "right"
            #gir kollisjon med høyre vegg
            if self.x + self.size + 11 < WIDTH:
                #gir fart mot høyre
                self.vx = 4
        
        #sjekker om piltast opp trykkes på
        elif keys[pg.K_UP]:
            #setter karakterens retning til å gå opp
            self.direction = "up"
            #gir kollisjon med toppen
            if self.y + 11 > 0:
                #gir fart oppover
                self.vy = -4
        
        #sjekker om piltast ned trykkes på
        elif keys[pg.K_DOWN]:
            #setter karakterens retning til å gå ned
            self.direction = "down"
            #gir kollisjon med bunnen
            if self.y + self.size + 11 < HEIGHT:
                #gir fart nedover
                self.vy = 4
        

#lager en klasse for kylling-karakteren som arver av karakter-klassen
class Chick(Character):
    #konstruktør
    def __init__(self, x, y, image, direction, size, scale, sprite_sheet):
        super().__init__(x, y, image, direction, size, scale, sprite_sheet)
        self.hidden = False
    
    def move(self):
        self.vx = 0
        self.vy = 0
       
        
        keys = pg.key.get_pressed()
        
        #sjekker om knappen "a" blir trykket på
        if keys[pg.K_a]:
            self.direction = "left"
            #gir kollisjon med venstre vegg
            if self.x > 0:
                #gir fart mot venstre
                self.vx = -4
        
        #sjekker om knappen "d" blir trykket på
        elif keys[pg.K_d]:
            self.direction = "right"
            #gir kollisjon med høyre vegg
            if self.x + self.size + 11 < WIDTH:
                #gir fart mot høyre
                self.vx = 4
        
        #sjekker om knappen "w" blir trykket på
        elif keys[pg.K_w]:
            self.direction = "up"
            #gir kollisjon med toppen
            if self.y + 11 > 0:
                #gir fart oppover
                self.vy = -4
        
        #sjekker om knappen "s" blir trykket på
        elif keys[pg.K_s]:
            self.direction = "down"
            #gir kollisjon med bunnen
            if self.y + self.size + 22 < HEIGHT:
                #gir fart nedover
                self.vy = 4




#pug objekt
pug = Pug(500, 300, "bilder/pug-001.png", "left", 32, 1.5, sprite_sheet)

#kylling objekt
chick = Chick(200, 300, "bilder/chick.png", "right", 26, 2, sprite_sheet2)






#lager en klasse for rektangler/firkanter
class Rektangel:
    #konstruktør
    def __init__(self, x, y, w, h, image, scale):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.scale = scale
        #henter inn bildet til objektet
        self.rektangelImg = pg.image.load(self.image)
        #skalerer objektet
        self.rektangelImg = pg.transform.scale(self.rektangelImg, (self.w * self.scale, self.h * self.scale))
        #lager et rektangel rundt objektet
        self.rektangelRect = self.rektangelImg.get_rect()
        #henter x- og y-verdien til det skalerte objektet (brukt i kollisjonene)
        self.rektangelRect.x = x
        self.rektangelRect.y = y
        #henter høyden og bredden til det skalerte objektet
        self.h = self.rektangelRect.height
        self.w = self.rektangelRect.width
    
    #metode som tegner objektet
    def draw(self):
        surface.blit(self.rektangelImg, (self.x, self.y))


#hønsehus objekt
honsehus = Rektangel(700,200,50,50, "bilder/honsehus.png", 4)

#høyball objekter
hoyball1 = Rektangel(500,100,64,64, "bilder/hoyball.png", 1)
hoyball2 = Rektangel(500,100+64,64,64, "bilder/hoyball.png", 1)



#lager en tekst dersom hunden vinnersom kan vises til skjerm med hvit skrift og blå bakgrunn
textPug = font.render("Pug vinner!", True, WHITE,BLUE)
#finner rektangelet rundt teksten
textRectPug = textPug.get_rect()
#setter midten til tekstens rektangel = midten av hele skjermen
textRectPug.center = (WIDTH // 2, HEIGHT // 2)

#lager tekst dersom kyllingen vinner
textChick = font.render("Kylling vinner!", True, WHITE,BLUE)
textRectChick = textChick.get_rect()
textRectChick.center = (WIDTH // 2, HEIGHT // 2)



#lager en metode som sjekker kollisjon mellom kyllingen og hønsehuset
def collisionChickHonsehus(chick, honsehus):
    #sjekker om kyllingens x-verdi kolliderer med hønsehusets x-verdi
    if chick.x + chick.size - 11 >= honsehus.x and chick.x + 38 <= honsehus.x + honsehus.w:
        #sjekker om kyllingens y-verdi kolliderer med hønsehusets y-verdi
        if chick.y + chick.size >= honsehus.y and chick.y + 38 <= honsehus.y + honsehus.h:
            #pug skal bli borte dersom kylling vinner
            pug.hidden = True
            #skriver vinnertekst for kyllingen
            surface.blit(textChick, textRectChick)
     

#lager en metode som sjekker kollisjon mellom hunden og kyllingen
def collisionPugChick(pug, chick):
    #sjekker om kyllingens x-verdi kolliderer med hundens x-verdi
    if chick.x + chick.size >= pug.x and chick.x <= pug.x + pug.size:
        #sjekker om kyllingens y-verdi kolliderer med hundens y-verdi
        if chick.y + chick.size >= pug.y and chick.y <= pug.y + pug.size:
            #kylling blir borte dersom hunden vinner
            chick.hidden = True
            #skriver vinnertekst for hunden
            surface.blit(textPug, textRectPug)
            

#lager en metode som sjekker kollisjon mellom hunden og hønsehuset
def collisionPugHonsehus(pug, honsehus):
    #lager et nytt rektangel rundt hunden med de skalerte x- og y-verdiene
    ny_rect = pg.Rect(
            pug.x + pug.vx,
            pug.y + pug.vy,
            pug.size * pug.scale,
            pug.size * pug.scale)
    
    #sjekker for kollisjon mellom hund og hønsehus
    if pg.Rect.colliderect(ny_rect, honsehus.rektangelRect):
        #hvis hunden treffer overnfra eller nedenfra skal fart i y-retning stoppe
        if pug.direction in ("up", "down"):
            pug.vy = 0
        #hvis hunden treffer fra siden skal fart i x-retning stoppe
        if pug.direction in ("left", "right"):
            pug.vx = 0


#lager en metode for kollisjon mellom høyballene og karakterene
def collisionHoyballPugChick(hoyball1, hoyball2, pug, chick):
    #lager et nytt rektangel rundt hunden med de skalerte x- og y-verdiene
    ny_rect = pg.Rect(
            pug.x + pug.vx,
            pug.y + pug.vy,
            pug.size * pug.scale,
            pug.size * pug.scale)
    
    #lager et nytt rektangel rundt kyllingen med de skalerte x- og y-verdiene
    ny_rect2 = pg.Rect(
            chick.x + chick.vx,
            chick.y + chick.vy,
            chick.size * chick.scale,
            chick.size * chick.scale)
    
    #sjekker for kollisjon mellom hund og høyball1
    if pg.Rect.colliderect(ny_rect, hoyball1.rektangelRect):
        #hvis hunden treffer overnfra eller nedenfra skal fart i y-retning stoppe
        if pug.direction in ("up", "down"):
            pug.vy = 0
        #hvis hunden treffer fra siden skal fart i x-retning stoppe
        if pug.direction in ("left", "right"):
            pug.vx = 0
    
    #sjekker for kollisjon mellom hund og høyball2
    if pg.Rect.colliderect(ny_rect, hoyball2.rektangelRect):
        #hvis hunden treffer overnfra eller nedenfra skal fart i y-retning stoppe
        if pug.direction in ("up", "down"):
            pug.vy = 0
        #hvis hunden treffer fra siden skal fart i x-retning stoppe
        if pug.direction in ("left", "right"):
            pug.vx = 0
    
    #sjekker for kollisjon mellom kylling og hoyball1
    if pg.Rect.colliderect(ny_rect2, hoyball1.rektangelRect):
        #hvis kyllingen treffer overnfra eller nedenfra skal fart i y-retning stoppe
        if chick.direction in ("up", "down"):
            chick.vy = 0
        #hvis kyllingen treffer fra siden skal fart i x-retning stoppe
        if chick.direction in ("left", "right"):
            chick.vx = 0
    
    #sjekker for kollisjon mellom kylling og hoyball2
    if pg.Rect.colliderect(ny_rect2, hoyball2.rektangelRect):
        #hvis kyllingen treffer overnfra eller nedenfra skal fart i y-retning stoppe
        if chick.direction in ("up", "down"):
            chick.vy = 0
        #hvis kyllingen treffer fra siden skal fart i x-retning stoppe
        if chick.direction in ("left", "right"):
            chick.vx = 0
    




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
    
    
    #sjekker kollisjon mellom kylling og hønsehus
    collisionChickHonsehus(chick, honsehus)
    #sjekker kollisjon mellom pug og kylling
    collisionPugChick(pug, chick)
    #sjekker kollisjon mellom pug og hønsehus
    collisionPugHonsehus(pug, honsehus)
    #sjekker kollisjon mellom karakterene og høyballene
    collisionHoyballPugChick(hoyball1,hoyball2,pug,chick)
    
    
    #tegner hønsehus
    honsehus.draw()
    
    #tegner første høyball
    hoyball1.draw()
    #tegner andre høyball
    hoyball2.draw()
    
    #så lenge høna ikke har tapt skal den vises og oppdateres
    if not chick.hidden:
        #oppdaterer posisjonen
        chick.update()
        #sier at kyllingen kan bevege seg så lenge hunden er med i spillet
        if not pug.hidden:
            #beveger seg
            chick.move()
        #tegner høne til skjermen
        chick.draw()
    #hvis høna vinner skal den stå stille
    if pug.hidden:
        chick.vx = 0
        chick.vy = 0
    
    
    #så lenge hunden ikke har tapt skal den vises og oppdateres
    if not pug.hidden:
        #oppdaterer posisjonen
        pug.update()
        #sier at hunden kan bevege seg så lenge kyllingen er med i spillet
        if not chick.hidden:
            #beveger seg
            pug.move()
        #tegner hunden til skjermen
        pug.draw()
    #hvis hunden vinner skal den stå stille
    if chick.hidden:
        pug.vx = 0
        pug.vy = 0
    
    
    # Etter vi har tegner alt, "flipper" vi displayet
    pg.display.flip()



# Avslutter pygame når spilløkken ikke lenger kjøres
pg.quit()








#poengsystem, tilfeldig plassering av spillbrikker, resettes, bytte karakterer
#evt to forskjellige konfigurasjoner, at pug høne og hønsehus tilfeldig plasseres i en range
#pug skal ikke kunne gå inn i hønsehuset

#nevne i presentasjon at f.eks. tallet 11, 38 og så videre har med formen til kyllingen å gjøre og er regnet ut



