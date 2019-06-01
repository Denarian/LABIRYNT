import pygame
import generator


pygame.font.init()


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('red')
FONT = pygame.font.Font(None, 32)


class Input:
    def __init__(self, x, y, w, h, text='', fun=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.fun = fun
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class InputBox(Input):

    def __init__(self, x, y, w, h, text='', fun=None, interactable=True):
        Input.__init__(self, x, y, w, h, text, fun)
        self.interactable = interactable

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN  and self.interactable:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.fun is not None:
                    self.fun()
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.txt_surface = FONT.render(self.text, True, self.color)

        if event.type == pygame.KEYDOWN  and self.interactable:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                #                 # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                self.update()

    def text_to_int(self):
        # temp = ''
        #         # for x in self.text:
        #         #     if x in '-0123456789':
        #         #         temp += x
        temp  = [x for x in self.text if x in '-0123456789']
        #print(''.join(temp))
        return int(''.join(temp))

    def update(self):
        # Resize the box if the text is too long.
        width = max(10, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button(Input):
    def __init__(self, x, y, w, h, text='', fun=None, switch=0):
        Input.__init__(self, x, y, w, h, text, fun)
        self.switch = switch

    def handle_event(self, event):
         if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.fun is not None:
                    self.fun()

         elif not self.switch:
            self.active = False

         self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
         self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class CheckBox(Input):
    def __init__(self, x, y, w, h, text='', fun=None):
        Input.__init__(self, x, y, w, h, text, fun)
        if text != '':
            self.rect.x += self.txt_surface.get_width() + 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.fun is not None:
                    self.fun()
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def draw(self, screen):
        # Blit the text.
        width = max(10, self.txt_surface.get_width() + 5)
        screen.blit(self.txt_surface, (self.rect.x - width, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.active:
            pygame.draw.line(screen, self.color, self.rect.bottomleft, self.rect.topright, 2)
            pygame.draw.line(screen, self.color, self.rect.bottomright, self.rect.topleft, 2)


class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class Menu(SceneBase):
    def __init__(self, x=10, y=10, rozm=30):
        SceneBase.__init__(self)
        self.rozmiar_x = 230
        self.rozmair_y = 300
        self.screen = pygame.display.set_mode((self.rozmiar_x, self.rozmair_y))
        self.obiekty = {}
        self.rozmiar_pol = rozm
        self.obiekty["rozm_x"] = InputBox(10, 10, 210, 30, "Rozmiar x: "+str(int(x)))
        self.obiekty["rozm_y"] = InputBox(10, 50, 210, 30, "Rozmiar y: "+str(int(y)))
        self.obiekty["rozm"] = InputBox(10, 90, 210, 30, "Rozmiar pola: "+str(int(rozm)),None)
        #self.obiekty["+"] = Button(10,130,30,30," + ",lambda: pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{"key" : pygame.K_KP_PLUS})))
        #self.obiekty["-"] = Button(50, 130, 30, 30, " - ", lambda: pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_KP_MINUS})))
        self.obiekty["info"] = Button(10,130,210,30,'', lambda: pygame.event.post(pygame.event.Event(pygame.USEREVENT,{"usun":'info'})) ,1)
        self.obiekty["generuj 1"] = Button(10,170,210,30,"Depth-First Search", lambda: pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{"key" : pygame.K_RETURN})))
        self.obiekty["generuj 2"] = Button(10,210,210,30,"Recursive Division", lambda: pygame.event.post(pygame.event.Event(pygame.KEYDOWN,{"key" : pygame.K_KP_ENTER})))
       # self.obiekty['bu'] = CheckBox(10,240,30,30,"bu: ",lambda: print("bu"))
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    x = self.obiekty["rozm_x"].text_to_int()
                    y = self.obiekty["rozm_y"].text_to_int()
                    rozm = self.obiekty["rozm"].text_to_int()
                    if x < 0 or y < 0 or rozm < 0:
                        self.obiekty['info'].text = "err: x,y,rozm < 0"
                        self.obiekty['info'].active = True
                    elif x > 30 or y > 30:
                        self.obiekty['info'].text = "err: x,y > 30"
                        self.obiekty['info'].active = True
                    else:
                        self.SwitchToScene(Labirynt(x, y, rozm, 1))

                if event.key == pygame.K_KP_ENTER:
                    x = self.obiekty["rozm_x"].text_to_int()
                    y = self.obiekty["rozm_y"].text_to_int()
                    rozm = self.obiekty["rozm"].text_to_int()
                    if x < 1 or y < 1 or rozm < 1:
                        self.obiekty['info'].text = "err: x,y,rozm < 1"
                        self.obiekty['info'].active = True
                    elif x > 30 or y > 30 :
                        self.obiekty['info'].text = "err: x,y > 30"
                        self.obiekty['info'].active = True
                    else:
                        self.SwitchToScene(Labirynt(x, y, rozm, 0))

                if event.key == pygame.K_KP_PLUS:
                    if self.rozmiar_pol < 100:
                        self.rozmiar_pol += 5
                    pole = self.obiekty["rozm"]
                    pole.text = "Rozmiar pola: "+str(int(self.rozmiar_pol))
                    pole.txt_surface = FONT.render(pole.text, True, pole.color)
                    #pole.update()
                if event.key == pygame.K_KP_MINUS:
                    if self.rozmiar_pol > 10:
                        self.rozmiar_pol -= 5
                    pole = self.obiekty["rozm"]
                    pole.text = "Rozmiar pola: " + str(int(self.rozmiar_pol))
                    pole.txt_surface = FONT.render(pole.text, True, pole.color)
                    #pole.update()
            if event.type == pygame.USEREVENT and event.usun == 'info':
                self.obiekty['info'].text = ''
            for okno in self.obiekty.values():
                okno.handle_event(event)

    def Update(self):
        pass

    def Render(self, screen):

        screen.fill((255, 255, 255))
        for okno in self.obiekty.values():
            okno.draw(screen)


class Labirynt(SceneBase):
    def __init__(self, x, y, rozm, algorytm=1):
        SceneBase.__init__(self)
        self.rozmair_x = x * rozm
        self.rozmair_y = y * rozm
        self.rozmiar_pola = rozm
        self.screen = pygame.display.set_mode((self.rozmair_x, self.rozmair_y))
        self.lab = generator.Labirynt(x, y, rozm)
        self.stan = ''
        self.algorytm=algorytm

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and( event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                if self.stan is 'rozwiazane':
                    self.SwitchToScene(Menu(self.rozmair_x/self.rozmiar_pola, self.rozmair_y/self.rozmiar_pola,self.rozmiar_pola))
                    continue
                if self.stan in 'koniec' or self.stan is 'start' or self.stan is '':
                    if self.algorytm:
                        self.lab.generuj()
                        while not self.lab.rozwiaz(1):
                            self.lab.generuj()
                    else:
                        self.lab.generator_rekurencyjny()
                        while not self.lab.rozwiaz(1):
                            self.lab.generator_rekurencyjny()
                    self.stan = 'wygenerowane'
                    continue
                if self.stan is 'wygenerowane':
                    self.lab.rozwiaz()
                    self.stan = 'rozwiazane'
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.stan is '':
                    if self.lab.zmien_pole(pos[0], pos[1], -1):
                        self.stan = 'start'
                        continue
                if self.stan is 'start':
                    if self.lab.zmien_pole(pos[0], pos[1], 2):
                        self.stan = 'koniec'
                        continue
                if self.stan is 'wygenerowane':
                    self.lab.zmien_pole(pos[0], pos[1], -2)
                    continue

    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        self.lab.rysuj(screen)
