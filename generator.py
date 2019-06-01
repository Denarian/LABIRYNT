from typing import List, Tuple
import random
import pygame

pygame.font.init()


class Pole(object):

    def __init__(self):
        self.typ = 1  # 1 to ściana 0 to scierzka -1 start 2 koniec
        self.odwiedzona = False
        self.droga = False
        self.kierunek = []
        self.numer = 0

    def rysuj(self, x, y, rozmiar, obszar):
        if self.typ==1:
            kolor = (0,0,0)
        elif self.typ== -1:
            kolor = (0, 255, 0)
        elif self.typ == 2:
            kolor = (255, 0, 0)
        elif self.typ == -2:
            kolor = (0, 0, 255)
        else:
            kolor = (255,255,255)
            if self.odwiedzona:
                kolor = (192, 192, 192)
            if self.droga:
                kolor = (255, 255, 0)
        rect = pygame.Rect(x*rozmiar, y*rozmiar, rozmiar, rozmiar)
        pygame.draw.rect(obszar, kolor, rect )
        if self.typ == 1:
            pygame.draw.line(obszar,(192, 192, 192),rect.bottomleft, rect.bottomright)
            pygame.draw.line(obszar, (192, 192, 192), rect.bottomright, rect.topright)
            pygame.draw.line(obszar, (192, 192, 192), rect.topright, rect.topleft)
            pygame.draw.line(obszar, (192, 192, 192), rect.topleft, rect.bottomleft)
        if rozmiar >= 15:
            for kier in self.kierunek:
                punkty = []
                if kier is 'lewo':
                    start = rect.midleft
                    punkty = [start, (start[0] + 3, start[1] - 3), (start[0] + 3, start[1]), (start[0] + 8, start[1]),
                              (start[0] + 8, start[1] + 1), (start[0] + 3, start[1] + 1), (start[0] + 3, start[1] + 4),
                              (start[0], start[1] + 1)]

                if kier is 'prawo':
                    start = rect.midright
                    punkty = [start, (start[0] - 3, start[1] - 3), (start[0] - 3, start[1]), (start[0] - 8, start[1]),
                              (start[0] - 8, start[1] + 1), (start[0] - 3, start[1] + 1), (start[0] - 3, start[1] + 4),
                              (start[0], start[1] + 1)]

                if kier is 'gora':
                    start = rect.midtop
                    punkty = [start, (start[0] - 3, start[1] + 3), (start[0], start[1] + 3), (start[0], start[1] + 8),
                              (start[0] + 1, start[1] + 8), (start[0] + 1, start[1] + 3), (start[0] + 4, start[1] + 3),
                              (start[0] + 1, start[1])]
                if kier is 'dol':
                    start = rect.midbottom
                    punkty = [start, (start[0] - 3, start[1] - 3), (start[0], start[1] - 3), (start[0], start[1] - 8),
                            (start[0] + 1, start[1] - 8), (start[0] + 1, start[1] - 3), (start[0] + 4, start[1] - 3),
                            (start[0] + 1, start[1])]
                if len(punkty):
                    if kolor is (0, 0, 255) or kolor is (255,255,255) :
                        kolor = (255,255,255)
                    else:
                        kolor = (0, 0, 0)
                    pygame.draw.polygon(obszar,kolor,punkty,0)
            if self.numer > 0:
                txt_surface = pygame.font.Font(None, int(rozmiar*0.75)).render(str(self.numer), True, (255, 0, 0))
                obszar.blit(txt_surface, (rect.centerx-rozmiar//6, rect.centery-rozmiar//6))


class Labirynt(object):

    def __init__(self, x, y, rozm_pol=10):
        self.rozmiar_y = y
        self.rozmiar_x = x
        self.start = (0, 0)
        self.koniec = (x-1, y-1)
        self.mapa: List[List[Pole]] = [[]]
        self.rozm_pol = rozm_pol
        self.punkty_posrednie = [self.start,self.koniec]

        for x in range(0,self.rozmiar_x):
            temp = []
            self.mapa.append(temp)
            for y in range(0,self.rozmiar_y):
                self.mapa[x].append(Pole())

        self.mapa[self.start[0]][self.start[1]].typ = -1
        self.mapa[self.koniec[0]][self.koniec[1]].typ = 2

    def rysuj(self, obszar):
        for x in range(0,self.rozmiar_x):
            for y in range(0,self.rozmiar_y):
                self.mapa[x][y].rysuj(x, y, self.rozm_pol, obszar)

    def sasiedzi(self, pozycja: Tuple):
        x = pozycja[0]
        y = pozycja[1]
        temp: List[Tuple] = []
        mapa = self.mapa

        #print("x: ", x ,"y: ",y)

        if x > 0 and not mapa[x-1][y].odwiedzona: #lewo
            sasiedzi = self.sasiedzi_sciezki(x - 1, y)
            if len(sasiedzi) < 2:
                temp.append((x-1, y))

        if x < self.rozmiar_x - 1 and not mapa[x+1][y].odwiedzona:  # prawo
            sasiedzi = self.sasiedzi_sciezki(x + 1, y)
            if len(sasiedzi) < 2:
                temp.append((x+1, y))

        if y > 0 and not mapa[x][y-1].odwiedzona: #góra
            sasiedzi = self.sasiedzi_sciezki(x, y - 1)
            if len(sasiedzi) < 2:
                temp.append((x, y-1))

        if y < self.rozmiar_y - 1 and not mapa[x][y+1].odwiedzona: #lewo
            sasiedzi = self.sasiedzi_sciezki(x, y + 1)
            if len(sasiedzi) < 2:
                temp.append((x, y+1))

        return temp

    def sasiedzi_sciezki(self, x, y):

        temp: List[Tuple] = []
        mapa = self.mapa

        if x > 0 and  mapa[x-1][y].typ < 1: #lewo
            temp.append((x-1, y))

        if x < self.rozmiar_x - 1 and mapa[x+1][y].typ < 1:  # prawo
            temp.append((x+1, y))

        if y > 0 and mapa[x][y-1].typ < 1: #góra
            temp.append((x, y-1))

        if y < self.rozmiar_y - 1 and mapa[x][y+1].typ < 1: #lewo
            temp.append((x-1, y))

        for i in temp:
            t = 0
            if i == self.start: #jesli jednym z sasiadow jest start to poszukaj konca
                if x > 0 and mapa[x - 1][y].typ == 2:  # lewo
                    temp.append((x - 1, y))

                if x < self.rozmiar_x - 1 and mapa[x + 1][y].typ == 2:  # prawo
                    temp.append((x + 1, y))

                if y > 0 and mapa[x][y - 1].typ == 2:  # gora
                    temp.append((x, y - 1))

                if y < self.rozmiar_y - 1 and mapa[x][y + 1].typ == 2:  # lewo
                    temp.append((x - 1, y))
        return temp

    def generuj(self):
        for i in self.mapa:
            for j in i:
                if j.typ == 0:
                    j.typ = 1

        pozycja = self.start
        mapa = self.mapa
        mapa[pozycja[0]][pozycja[1]].odwiedzona = True
        stos = [pozycja]
        while len(stos):
            sasiedzi = self.sasiedzi(pozycja)
            if len(sasiedzi):
                i = random.randint(0, len(sasiedzi)-1)

                pozycja = sasiedzi[i]

                mapa[pozycja[0]][pozycja[1]].odwiedzona = True
                if mapa[pozycja[0]][pozycja[1]].typ != 2:
                    mapa[pozycja[0]][pozycja[1]].typ = 0
                stos.append(pozycja)
            else:
                pozycja = stos.pop()

    def generator_rekurencyjny(self):
        for i in self.mapa:
            for j in i:
                if j.typ == 1:
                    j.typ = 0

        max_x = self.rozmiar_x - 1
        max_y = self.rozmiar_y - 1
        if self.start[0] % 2 or self.start[1] % 2:
            reverted = False
        else:
            reverted = True

        self.generator_rekura(0, 0, max_x, max_y, reverted)

        odleglosc_x = abs(self.start[0] - self.koniec[0])
        odleglosc_y = abs(self.start[1] - self.koniec[1])

        if self.start[1] == self.koniec[1] : #zabezpieczenie przed prostą ścieżką w poziomie
             if self.start[0] - self.koniec[0] > 0:
                 self.mapa[self.start[0]-1][self.start[1]].typ = 1
             else:
                 self.mapa[self.start[0]+1][self.start[1]].typ = 1
        elif self.start[0] == self.koniec[0] :#zabezpieczenie przed prostą ścieżką w pionie
            if self.start[1] - self.koniec[1] > 0:
                self.mapa[self.start[0]][self.start[1]-1].typ = 1
            else:
                self.mapa[self.start[0]][self.start[1]+1].typ = 1

    def generator_rekura(self, x, y, max_x, max_y, reverted=False):
        w = max_x - x
        h = max_y - y
        if w < 1 or h < 1:
            return
        if w < h:
            kierunek = 1
        elif w > h:
            kierunek = 0
        else:
            kierunek = random.randint(0,1)
        if kierunek:

            if reverted:
                sciana = random.randint(y,max_y)
                while sciana % 2:
                    sciana = random.randint(y, max_y)
                drzwi = random.randint(x, max_x)
                while not drzwi % 2:
                    drzwi = random.randint(x, max_x)
            else:
                sciana = random.randint(y,max_y)
                while not sciana % 2:
                    sciana = random.randint(y, max_y)
                drzwi = random.randint(x, max_x)
                while drzwi % 2:
                    drzwi = random.randint(x, max_x)

            #print(x, y, w, h, " | ",sciana,drzwi)
            for i in range(x,max_x+1):
                if i != drzwi:
                    if self.mapa[i][sciana].typ == 0:
                        self.mapa[i][sciana].typ = 1
            self.generator_rekura(x , y, max_x, sciana - 1, reverted)
            self.generator_rekura(x, sciana + 1, max_x , max_y, reverted)


        else:
            if reverted:
                sciana = random.randint(x, max_x)
                while sciana % 2:
                    sciana = random.randint(x, max_x)

                drzwi = random.randint(y, max_y)
                while not drzwi % 2:
                    drzwi = random.randint(y, max_y)
            else:
                sciana = random.randint(x, max_x)
                while not sciana % 2:
                    sciana = random.randint(x, max_x)

                drzwi = random.randint(y, max_y)
                while drzwi % 2:
                    drzwi = random.randint(y, max_y)


            #print(x, y, w, h, " | ", sciana, drzwi)
            for i in range(y, max_y+1):
                if i != drzwi:
                    if self.mapa[sciana][i].typ == 0:
                        self.mapa[sciana][i].typ = 1
            self.generator_rekura(x, y, sciana - 1, max_y, reverted)
            self.generator_rekura(sciana + 1, y, max_x, max_y, reverted)

    def rozwiaz_rekurencja(self,pozycja: Tuple, koniec: Tuple, nr_scierzki):

        if pozycja == koniec: # jesli koniec
            return True
        x = pozycja[0]
        y = pozycja[1]
        mapa = self.mapa

        if mapa[x][y].typ == 1 or mapa[x][y].odwiedzona == nr_scierzki: # jesli sciana lub juz tu bylismy
            return False

        mapa[x][y].odwiedzona = nr_scierzki
        kierunki = list(range(1, 5))
        while kierunki:
            kierunek = random.choice(kierunki)

            if x != 0 and kierunek == 1: # jesli nie na lewej krawedzi
                if self.rozwiaz_rekurencja((x-1, y), koniec,nr_scierzki):
                    mapa[x][y].droga = True
                    mapa[x][y].kierunek.append('lewo')
                    return True
            if x != self.rozmiar_x - 1 and kierunek == 2:# jesli nie na prawej krawedzi
                if self.rozwiaz_rekurencja((x+1, y), koniec,nr_scierzki):
                    mapa[x][y].droga = True
                    mapa[x][y].kierunek.append('prawo')
                    return True
            if y != 0  and kierunek == 3: # jesli nie na gornej krawedzi
                if self.rozwiaz_rekurencja((x, y-1), koniec, nr_scierzki):
                    mapa[x][y].droga = True
                    mapa[x][y].kierunek.append('gora')
                    return True
            if y != self.rozmiar_y - 1 and kierunek == 4:# jesli nie na dolnej krawedzi
                if self.rozwiaz_rekurencja((x, y+1), koniec, nr_scierzki):
                    mapa[x][y].droga = True
                    mapa[x][y].kierunek.append('dol')
                    return True
            kierunki.remove(kierunek)
        return False

    def rozwiaz(self, wyczysc='0'):
        #print("max_x : ", len(self.mapa), "max_y : ", len(self.mapa[0]) )
        for x in range(0, self.rozmiar_x):
            for y in range(0, self.rozmiar_y):
               #print("x: ", x, "y: ", y)
                self.mapa[x][y].odwiedzona = 0
        for i in list(range(len(self.punkty_posrednie)-1)):
            if self.rozwiaz_rekurencja(self.punkty_posrednie[i], self.punkty_posrednie[i+1], i+1):
                print("Ścierzka do punktu", i+1,"OK")
            else:
                print("Ścierzka do punktu", i, "BŁĄD")
                return False

        if wyczysc==1:
            for i in self.mapa:
                for j in i:
                    j.odwiedzona = False
                    j.kierunek = []
                    j.droga = False
        return True

    def zmien_pole(self, xx, yy, typ):
        x = xx//self.rozm_pol
        y = yy//self.rozm_pol

        if typ == -1 and self.mapa[x][y].typ == 2:
                return 0
        if typ == 2 and (self.mapa[x][y].typ == -1 or len(self.sasiedzi_sciezki(x, y))):
                return 0

        if typ == -1 or typ == 2:
            for i in self.mapa:
                for j in i:
                    if j.typ == typ:
                        j.typ = 1

        if typ == -1:
            self.start = (x, y)
            self.punkty_posrednie[0] = (x, y)

        if typ == 2:
            self.koniec = (x, y)
            self.punkty_posrednie[-1] = (x, y)

        if typ == -2 :
            if self.mapa[x][y].typ == 0:
                self.punkty_posrednie.insert(-1,(x, y))
                self.mapa[x][y].numer = self.punkty_posrednie.index((x, y))
            elif self.mapa[x][y].typ == -2:
                self.mapa[x][y].typ = 0
                self.mapa[x][y].numer = 0
                self.punkty_posrednie.remove((x, y))
                for i in range(1,len(self.punkty_posrednie) -1 ):
                    self.mapa[self.punkty_posrednie[i][0]][self.punkty_posrednie[i][1]].numer = i
                return 1
            else:
                return 0

        self.mapa[x][y].typ = typ
        return 1
