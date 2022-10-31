import pygame
import random

class Peli:
    def __init__(self):
        pygame.init()
        self.näyttö = pygame.display.set_mode((640, 480))
        self.suunta = None

        self.piste_x = 80
        self.piste_y = 100
        self.piste_väri = 255, 69, 0
        self.pisteen_koko = 25

        self.este_väri = 255,255,255
        self.este_sijainti = 50, 390, 130
        self.hahmo = self.luo_hahmo()
        
        self.laskuri = 0
        self.vauhti = 2
        self.i = 0
        self.värit = [(47, 93, 94), (214, 105, 2), (59, 1, 102), (255,69,0), (107, 66, 4), (117, 148, 24), (237, 205, 19)]
        self.fontti_1 = pygame.font.SysFont("Bauhaus 93", 40, False)
        self.fontti_2 = pygame.font.SysFont("Consolas", 17, False)
        pygame.display.set_caption("R E A K T I O P E L I")
        self.kello = pygame.time.Clock()
        self.silmukka()

    def luo_hahmo(self):
        self.hahmon_koko = (70, 10)
        tyhjä_surface = pygame.Surface(self.hahmon_koko)
        tyhjä_surface.fill((0,0,0))
        self.hahmo_x = 320-35
        self.hahmo_y = 415-35
        return tyhjä_surface

    def ohje(self):
        teksti = self.fontti_1.render(f"R E A K T I O P E L I", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 140))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"V", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 185))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"liiku nuolilla", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 220))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"kerää palloja", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 250))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"väistä viivaa", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 280))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"älä osu reunaan", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 310))
        self.näyttö.blit(teksti, teksti_rect)
        teksti = self.fontti_2.render(f"V", True, (220, 200, 16))
        teksti_rect = teksti.get_rect(center=(320, 350))
        self.näyttö.blit(teksti, teksti_rect)

    def muuta_piste_värit(self):
        self.piste_väri = self.värit[self.i]

    def muuta_piste_sijainti(self):
        este = self.este_sijainti[-1]
        koko = self.pisteen_koko 
        self.piste_x = random.choice([luku for luku in range(6+self.pisteen_koko, 640-self.pisteen_koko-6)if luku < este-koko or luku+koko > este]) 
        self.piste_y = random.choice([luku for luku in range(6+self.pisteen_koko, 480-self.pisteen_koko-6)if luku < este-koko or luku+koko > este])
        return self.piste_x, self.piste_y

    def muuta_este_värit(self):
        self.este_väri = self.värit[self.i-1]

    def muuta_este_sijainti(self):
        # Määrittää pystyviivan (muuttujan c ehto varmistaa ettei este osu HETI pelaajaan)
        if self.laskuri % 2 == 0:
            a = random.choice([luku for luku in range(40, 80)])
            b = random.choice([luku for luku in range(300, 450)])
            c = random.choice([luku for luku in range(60, 570) if luku < self.hahmo_x - 30 or luku > self.hahmo_x + 90])
        # Määrittää vaakaviivan
        if self.laskuri % 2 != 0:
            a = random.choice([luku for luku in range(100, 130)])
            b = random.choice([luku for luku in range(350, 540)])
            c = random.choice([luku for luku in range(60, 430) if luku < self.hahmo_y - 60 or luku > self.hahmo_y + 70])
        self.este_sijainti = a, b, c
        
    def piirrä_näyttö(self):
        self.näyttö.fill((255, 220, 205))
                
        if self.suunta == None:
            self.ohje()

        self.näyttö.blit(self.hahmo, (self.hahmo_x, self.hahmo_y))

        # Pistelaskurin määritys.
        if self.suunta != None and self.laskuri >= 1:
            a = 550
            b = 570
            if self.laskuri > 9:
                b = 595
            teksti = self.fontti_1.render(str(self.laskuri), False, (255,255,255))
            pygame.draw.line(self.näyttö, (255,255,255), (a,428), (b,428), 2)
            self.näyttö.blit(teksti, (550, 390))

        # Piirtää pisteen eli kerättävän kohteen.
        pygame.draw.circle(self.näyttö, (self.piste_väri), (self.piste_x, self.piste_y), self.pisteen_koko)

        # Piirtää esteen, mikä täytyy kiertää.
        if self.laskuri % 2 != 0:
            pygame.draw.line(self.näyttö, (self.este_väri), (self.este_sijainti[0], self.este_sijainti[-1]), (self.este_sijainti[1], self.este_sijainti[-1]), 3)
        if self.laskuri % 2 == 0:
            pygame.draw.line(self.näyttö, (self.este_väri), (self.este_sijainti[-1], self.este_sijainti[0]), (self.este_sijainti[-1], self.este_sijainti[1]), 3)
        
        # Tarkistaa, että pelaaja pysyy reunojen sisällä.
        if self.tarkista_reunat() == True:
            self.suunta = 0
            self.lopetus()
            teksti = self.fontti_2.render("osuit reunaan pöh..", False, (220, 200, 16))
            teksti_rect = teksti.get_rect(center=(320, 200))
            self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri == 0:
                teksti = self.fontti_2.render(f"tällä kertaa et saanut pisteen pistettä, harmin paikka :/", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri == 1:
                teksti = self.fontti_2.render(f"sait kuitenkin yhden pisteen :/", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri > 1:
                teksti = self.fontti_2.render(f"** sait {self.laskuri} pistettä, wuhuu **", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)

        # Tarkistaa osuuko pelaaja pisteeseen.
        if self.tarkista_osuma_pisteeseen() == True:
            uusi_sijainti = self.muuta_piste_sijainti()
            self.laskuri += 1
            self.vauhti += 0.13
            if self.i == 6:
                self.i = 0
            else: self.i += 1
            self.pisteen_koko -= 1 
            self.muuta_piste_värit()
            self.muuta_este_värit()
            self.muuta_este_sijainti()
            self.piste_x = uusi_sijainti[0]
            self.piste_y = uusi_sijainti[1]

        # Tarkistaa osuuko pelaaja esteeseen.
        if self.tarkista_osuma_esteeseen() == True:
            self.suunta = 0
            self.lopetus()
            teksti = self.fontti_2.render("osuit esteeseen..", True, (220, 200, 16))
            teksti_rect = teksti.get_rect(center=(320, 200))
            self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri == 0:
                teksti = self.fontti_2.render(f"tällä kertaa et saanut yhtään pistettä, höh :/", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri == 1:
                teksti = self.fontti_2.render(f"** sait kuitenkin yhden pisteen **", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)
            if self.laskuri > 1:
                teksti = self.fontti_2.render(f"** sait silti {self.laskuri} pistettä, hieno homma! **", True, (220, 200, 16))
                teksti_rect = teksti.get_rect(center=(320, 230))
                self.näyttö.blit(teksti, teksti_rect)
            
        # Kun piste häviää näkyvistä, peli on suoritettu loppuun.
        if self.pisteen_koko < 1:
            self.suunta = 0
            self.fontti = pygame.font.SysFont("Arial", 30)
            pygame.draw.line(self.näyttö, (255,255,255), (0, 200), (640, 200), 50)
            teksti = self.fontti_2.render("** o n n i t t e l u t, läpi meni! **", True, (240, 76, 31))
            teksti_rect = teksti.get_rect(center=(320, 200))
            self.näyttö.blit(teksti, teksti_rect)

    def tarkista_osuma_esteeseen(self):
        # Este on aina pysty- tai vaakasuoraviiva. Muuttujat a ja b on viivan "kärjet"..
        # ..ja c määrittää viivan kohdan ruudulla pysty- tai vaakasuunnassa.
        a = self.este_sijainti[0]
        b = self.este_sijainti[1]
        c = self.este_sijainti[2]

        hahmon_leveys = self.hahmon_koko[0]
        hahmon_korkeus = self.hahmon_koko[1]
        
        # Tarkistaa osuman pystysuuntaiseen viivan
        if self.laskuri % 2 == 0:
            ehto1 = self.hahmo_x + hahmon_leveys >= c and self.hahmo_x <= c
            ehto2 = self.hahmo_y + hahmon_korkeus >= a and self.hahmo_y <= b
            if ehto1== True and ehto2 == True:
                return True
        # Tarkistaa osuman vaakasuuntaiseen viivaan
        if self.laskuri % 2 != 0:
            ehto1 = self.hahmo_x + hahmon_leveys >= a and self.hahmo_x <= b
            ehto2 = self.hahmo_y + hahmon_korkeus >= c and self.hahmo_y <= c + 3
            if ehto1== True and ehto2 == True:
                return True

    def tarkista_osuma_pisteeseen(self):
        # osuma leveyssuunnassa
        piste_ehto1 = self.hahmo_x < self.piste_x + self.pisteen_koko and self.hahmo_x + self.hahmon_koko[0] > self.piste_x - self.pisteen_koko
        # osuma pystysuunnassa
        piste_ehto2 = self.hahmo_y < self.piste_y + self.pisteen_koko and self.hahmo_y + self.hahmon_koko[1] > self.piste_y - self.pisteen_koko

        if piste_ehto1 == True and piste_ehto2 == True:
            return True

    def tarkista_reunat(self):
        if self.hahmo_x < 0 or self.hahmo_x > 640-self.hahmon_koko[0]:
            self.osuma_reunaan = True
            return True
        if self.hahmo_y < 0 or self.hahmo_y > 480-self.hahmon_koko[1]:
            self.osuma_reunaan = True
            return True

    def lopetus(self):
        pygame.draw.line(self.näyttö, (255,255,255), (0, 215), (640, 215), 95)
        teksti = self.fontti_2.render(f"F2 > uusi peli, ESC > poistu", True, (255, 174, 140))
        teksti_rect = teksti.get_rect(center=(500, 460))
        self.näyttö.blit(teksti, teksti_rect)

    def uusi_peli(self):
        self.suunta == None
        self.näyttö = pygame.display.set_mode((640, 480))
        self.suunta = None

        self.piste_x = 80
        self.piste_y = 100
        self.piste_väri = 255, 69, 0
        self.pisteen_koko = 25

        self.este_väri = 255,255,255
        self.este_sijainti = 50, 390, 130
        self.hahmo = self.luo_hahmo()
        
        self.laskuri = 0
        self.vauhti = 2
        self.i = 0

    def silmukka(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN and self.suunta != 0: 
                    self.suunta = tapahtuma.key
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                    if tapahtuma.key == pygame.K_F2:
                        self.uusi_peli()
                if tapahtuma.type == pygame.QUIT:
                    exit()
            
            if self.suunta == pygame.K_LEFT:
                self.hahmo_x -= self.vauhti
            if self.suunta == pygame.K_RIGHT:
                self.hahmo_x += self.vauhti
            if self.suunta == pygame.K_UP:
                self.hahmo_y -= self.vauhti
            if self.suunta == pygame.K_DOWN:
                self.hahmo_y += self.vauhti

            self.piirrä_näyttö()
            pygame.display.flip()
            self.kello.tick(60)

if __name__ == "__main__":
    Peli()