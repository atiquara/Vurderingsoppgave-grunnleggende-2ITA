#Initialisering
import pygame
import pygame.freetype
import sys
import random
from threading import Timer
from pygame import mixer
import tkinter as tk
from tkinter import simpledialog
import mysql.connector
from mysql.connector import Error
pygame.init()
mixer.init()

#try
connection = mysql.connector.connect(host='localhost',
                                     database='pyquiz',
                                     user='root',
                                     password='password')
if connection.is_connected():
        #tabell = connection.get_server_info()
        #print("Connected to MySQL Server version ", tabell)
    cursor = connection.cursor(buffered=True)
    cursor.execute("select database();")
        #record = cursor.fetchone()
        #print("Du er Koblet til databasen: ", record)
#except Error as i:
    #print("Problem Med MySQL Kobling", i)





#Farger
lightblue = (35, 57, 93)
darkgray = (90, 90, 90)
lightgray = (169, 169, 169)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

color_light = (170,170,170)
color_dark = (100,100,100)
  

#Verdier
Sekunder = 20
GlobalTid = Sekunder
QuizStart = False
Ledertavle = False
Navn = "Anon"

#Lyder
KlikkLyd = pygame.mixer.Sound('lyder/Klikk.wav')
KlokkeLyd = pygame.mixer.Sound('lyder/Klokke.wav')
TappeLyd = pygame.mixer.Sound('lyder/Tappe.wav')
VinneLyd = pygame.mixer.Sound('lyder/Vinne.wav')
FeilLyd = pygame.mixer.Sound('lyder/feil.wav')
RiktigLyd = pygame.mixer.Sound('lyder/riktig.wav')
BeepLyd = pygame.mixer.Sound('lyder/beeping.wav')

def SpillerNavn():
    ROOT = tk.Tk()
    ROOT.withdraw()
    Input = simpledialog.askstring(
            title = "Navn",
            prompt = "Hva heter du?"
        )
    global Navn
    Navn = Input
    if (Navn == ""):
        Navn = "Anon"
    elif (Navn is None):
        Navn = "Anon"

class NøytralSkjerm:
    def __init__(self, NesteSkjerm, *tekst):
        self.bakgrunn = pygame.Surface((640, 480))
        self.bakgrunn.fill(pygame.Color(lightblue))
        HøydePosisjon = 80
        if tekst:
            NøytralSkjerm.FONT = pygame.freetype.SysFont(None, 32)
            for i in tekst:
                NøytralSkjerm.FONT.render_to(
                    self.bakgrunn, 
                    (120, HøydePosisjon),
                    i,
                    pygame.Color(white)
                )
                HøydePosisjon += 50

        self.NesteSkjerm = NesteSkjerm
        self.EkstraTekst = None

    def start(self, text):
        self.EkstraTekst = text

    def draw(self, Skjerm):
        Skjerm.blit(self.bakgrunn, (0, 0))
        #FONT = pygame.font.SysFont(None, 55)
        #Tekst = FONT.render('lederavle', True, white)
        #Skjerm.blit(Tekst, (30, 410))

        if self.EkstraTekst:
            HøydePosisjon = 180
            for i in self.EkstraTekst:
                NøytralSkjerm.FONT.render_to(
                        Skjerm,
                        (120, HøydePosisjon),
                        i,
                        pygame.Color(white)
                    )
                HøydePosisjon += 50

    def update(self, Hendelser, dt):
        for i in Hendelser:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    return (self.NesteSkjerm, None)

class Status:
    def __init__(self):
        self.spørsmål = [
            ('Hvor mange hovedstater har Malaysia?', 2),
            ('Hva er 1*(3)+5/12*10*0+1?', 1),
            ('Hvor mange hav er i Norge?', 4),
            ('Hvor mange bra sanger har Ice Spice?', 1),
            ('Hvilken dag er etter Aprilsnarr?', 2),
            ('Python ble lagd i 199...', 1),
            ('Hvilken error code er "path not found"', 3),

        ]
        self.currentspørsmål = None
        self.riktig = 0
        self.feil = 0

    def genererspørsmål(self):
        tilfeldigvailg = random.choice(self.spørsmål)
        self.spørsmål.remove(tilfeldigvailg)
        self.currentspørsmål = tilfeldigvailg
        return tilfeldigvailg

    def svar(self, svar):
        global GlobalTid
        KlikkLyd.play()
        if svar == self.currentspørsmål[1]:
            self.riktig += 1
            RiktigLyd.play()
            if (GlobalTid != 0):
                GlobalTid += 5
        else:
            self.feil += 1
            GlobalTid -= 5
            if (GlobalTid < 1):
                GlobalTid = 0
            else:
                FeilLyd.play()
                
    def Resultat(self):
        global GlobalTid
        sql = "INSERT INTO Persons (navn, score, tid) VALUES (%s, %s, %s)"
        val = (Navn, self.riktig, GlobalTid)
        cursor.execute(sql, val)
        connection.commit()
        GlobalTid = Sekunder
        if (self.riktig > self.feil):
            VinneLyd.play()
        else:
            TappeLyd.play()
        return f'{self.riktig} svar riktig', f'{self.feil} svar feil','','Bra jobbet!' if self.riktig > self.feil else'Du klarer bedre!' 

class TimerSkjerm:
    def __init__(self):
        self.bakgrunn = pygame.Surface((640, 480))
        self.bakgrunn.fill(lightblue)
        NøytralSkjerm.FONT.render_to(
                self.bakgrunn,
                (150, 100),
                '    NAVNET DITT ER:',
                pygame.Color(white)
            )
        NøytralSkjerm.FONT.render_to(
            self.bakgrunn,
            (120, 250),
            '          ER DU KLAR?',
            pygame.Color(white)
        )
        self.Tabell = []
        rect = pygame.Rect(65, 300, 500, 80)
        self.Tabell.append(rect)
        SpillerNavn()
        
        text = Navn
        text_størrelse = 35
        text_rect = NøytralSkjerm.FONT.get_rect(text, size = text_størrelse)
        text_rect.centerx = self.bakgrunn.get_rect().centerx
        text_rect.y = (150)
        NøytralSkjerm.FONT.render_to(
            self.bakgrunn,
            text_rect,
            text,
            white,
            size = text_størrelse
        )


    def start(self, *args):
        pass

    def draw(self, Skjerm):
        Skjerm.blit(self.bakgrunn, (0, 0))
        Tekst = "START"
        for i in self.Tabell:
            if i.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(Skjerm, pygame.Color(green), i)
            pygame.draw.rect(Skjerm, pygame.Color(white), i, 5)           
            NøytralSkjerm.FONT.render_to(
                Skjerm,
                (i.x + 200, i.y + 30),
                str(Tekst),
                pygame.Color(white)
            )
    def update(self, Hendelser, dt):
        for i in Hendelser:
            if i.type == pygame.MOUSEBUTTONDOWN:
                for v in self.Tabell:
                    if v.collidepoint(i.pos):
                        global QuizStart
                        QuizStart = True
                        StopWatch()
                        return ('QuizSpill', Status())

class SpillSkjerm:
    def __init__(self):
        if NøytralSkjerm.FONT == None:
            NøytralSkjerm.FONT = pygame.freetype.SysFont(None, 32)

        self.Tabell = []
        BreddePosisjon = 120
        HøydePosisjon = 120
        for i in range(4):
            Tabell = pygame.Rect(BreddePosisjon, HøydePosisjon, 80, 80)
            self.Tabell.append(Tabell)
            BreddePosisjon += 100

    def start(self, Status):
        self.bakgrunn = pygame.Surface((640, 480))
        self.bakgrunn.fill(darkgray)
        self.Status = Status
        spørsmål, svar = Status.genererspørsmål()

        text = spørsmål
        text_størrelse = 35
        text_rect = NøytralSkjerm.FONT.get_rect(text, size = text_størrelse)
        text_rect.centerx = self.bakgrunn.get_rect().centerx
        text_rect.y = (50)
        NøytralSkjerm.FONT.render_to(
            self.bakgrunn,
            text_rect,
            text,
            white,
            size = text_størrelse
        )

    def draw(self, Skjerm):
        Skjerm.blit(self.bakgrunn, (0, 0))
        Tall = 1
        for i in self.Tabell:
            if i.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(Skjerm, pygame.Color(lightgray), i)
            pygame.draw.rect(Skjerm, pygame.Color(lightgray), i, 5)
            NøytralSkjerm.FONT.render_to(
                    Skjerm,
                    (i.x + 30, i.y + 30),
                    str(Tall),
                    pygame.Color(white)
                )
            Tall += 1

    def update(self, Hendelser, dt):
        for i in Hendelser:
            if i.type == pygame.MOUSEBUTTONDOWN:
                Verdi = 1
                for v in self.Tabell:
                    if v.collidepoint(i.pos):
                        self.Status.svar(Verdi)
                        if self.Status.spørsmål:
                            return ('QuizSpill', self.Status)
                        else:
                            global QuizStart
                            global GlobalTid
                            QuizStart = False
                            #GlobalTid = Sekunder
                            return ('Resultat', self.Status.Resultat())
                    Verdi += 1

def main():
    global QuizStart
    global GlobalTid
    global KlikkLyd
    Skjerm = pygame.display.set_mode((640, 480))
    Ramme = 0
    Skjermer = {
        'StartSide':    NøytralSkjerm(
            'TimerStart',
            ' Velkommen til Leos pyQuiz',
            '',
            '',
            'Trykk [SPACE] for å fortsette'
        ),
        'TimerStart':  TimerSkjerm(),
        'QuizSpill':     SpillSkjerm(),
        'Resultat':   NøytralSkjerm(
            'StartSide',
            'Dette er Resultatene dine:',
            '',
            '',
            '',
            '',
            '',
            'Trykk [SPACE] for å restarte'
        )
    }
    Scene = Skjermer['StartSide']
    FONT = pygame.font.SysFont(None, 55)
    FONT2 = pygame.font.SysFont("Arial Bold", 38)
    debounce = False

    while True:
        GlobalString = str(GlobalTid)
        Tekst1 = FONT.render("Tid Igjen:", True, (255, 255, 255))
        if GlobalTid == 0:
            Tekst2 = FONT.render(GlobalString, True, (red))
            if (debounce == False):
                debounce = True
                BeepLyd.play()
        else:
            Tekst2 = FONT.render(GlobalString, True, (255, 255, 255))

        Hendelser = pygame.event.get()
        for i in Hendelser:
            if i.type == pygame.QUIT:
                pygame.quit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if (QuizStart == False):
                    global Ledertavle
                    if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40:
                        if (Ledertavle == True):
                            Ledertavle = False
                        else:
                            Ledertavle = True
                    elif (Ledertavle == True):
                        if (Ledertavle == True):
                            Ledertavle = False
                        else:
                            Ledertavle = True
        mouse = pygame.mouse.get_pos()
        if (QuizStart == False):
            if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40:
                pygame.draw.rect(Skjerm,color_light,[20, 20, 140, 40])            
            else:
                pygame.draw.rect(Skjerm,color_dark,[20, 20, 140, 40])
            text = FONT2.render('ledertavle' , True , white)
            Skjerm.blit(text , (27, 26))
        if (Ledertavle == True):
            sample_surface = pygame.display.set_mode((640,480))
            color = (0, 0, 0)
            pygame.draw.rect(sample_surface, color, pygame.Rect(0, 0, 0, 0))
            sample_surface.fill(pygame.Color(lightblue))
            pygame.Color(lightblue)
            if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40:
                pygame.draw.rect(Skjerm,color_light,[20, 20, 140, 40])            
            else:
                pygame.draw.rect(Skjerm,color_dark,[20, 20, 140, 40])
            text = FONT2.render('ledertavle' , True , white)
            Skjerm.blit(text , (27, 26))

            cursor.execute("select * from Persons order by Tid desc")
            leaderboard = cursor.fetchmany(size=10)

            text1 = FONT.render('Navn' , True , white)
            text2 = FONT.render('Score' , True , white)
            text3 = FONT.render('Tid' , True , white)
            Skjerm.blit(text1, (180, 50))
            Skjerm.blit(text2, (340, 50))
            Skjerm.blit(text3, (520, 50))
            count = 1
            topvalue = 90
            for i in leaderboard:
                leaderstring = f"{str(count)}: {i[0]}             {i[1]}            {i[2]}"
                leader = FONT.render(leaderstring, True, white)
                leaderrect = leader.get_rect()
                leaderrect.right = (1145 // 2)
                leaderrect.top = topvalue
                Skjerm.blit(leader, leaderrect)
                count += 1
                topvalue += 37.5

        if (Ledertavle == False):
            Skjerm.blit(Tekst1,(415, 435))
            Skjerm.blit(Tekst2,(595, 435))
        Result = Scene.update(Hendelser, Ramme)
        pygame.display.flip()

        if Result:
            if (GlobalTid == 0):
                TappeLyd.play()
                NesteSkjerm, Status = ('Resultat',
                    ('1 svar riktig',
                    '2 svar feil',
                    '',
                    'Du klarer bedre!'
                    )
                )
            else:
                NesteSkjerm, Status = Result
            if NesteSkjerm:
                Scene = Skjermer[NesteSkjerm]
                if (GlobalTid == 0):
                    if (QuizStart == True):
                        QuizStart = False
                        #GlobalTid = Sekunder
                        NesteSkjerm == "Resultat"
                        Scene.start(Status)
                    else:
                        Scene.start(Status)
                else:
                    Scene.start(Status)

        Scene.draw(Skjerm)

def StopWatch():
    if (QuizStart == True):
        global GlobalTid
        Forsinkelse = Timer( 1, StopWatch)
        Forsinkelse.start()
        GlobalTid -= 1
        KlokkeLyd.play()
        if(GlobalTid <= 0):
            Forsinkelse.cancel()

#if __name__ == '__main__':
main()