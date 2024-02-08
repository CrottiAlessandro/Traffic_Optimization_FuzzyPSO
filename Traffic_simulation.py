

import pygame
import random
import numpy as np
import pandas as pd
from itertools import count
import copy

# Costanti
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 200
MAP_WIDTH = int(SCREEN_WIDTH * 2 / 3)
MAP_HEIGHT = int(SCREEN_HEIGHT)
MAX_SPEED = 150
SAFE = False
ACCMAX=10
AUTOPILOT=True
STOP=False
A=1.0 #costante che diminuisce la dist di sicurezza

# Classe Agent per rappresentare un'auto
class Agent:
    _ids = count(0)

    #inizializziamo alcuni elementi per ogni agente
    def __init__(self, x, y, speed):
        self.id = next(self._ids) 
        self.x = x                                  #la posizione di partenza che andremo poi a variare secondo le leggi del moto
        self.y = y                                  #la posizione lungo y resterà invariata 
        self.speed = speed                          #la velocità che varierà secondo le leggi del moto
        self.ax = random.randint(0,ACCMAX/2)        #l'accelerazione parte da un valore random tra 0 e l'accelerazione massima consentita diviso 2
        self.safety_dist = self.safety_distance()   #definiamo la distanza distanza di sicurezza
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))  #il colore con cui verrà disegnato l'agente lo determiniamo casualemente
        self.radius=20                              

    #la posizione degli agenti viene modificata ad ogni iterazione secondo le leggi del moto
    def update(self, time_passed):
        self.x += self.speed * time_passed#
        
    #valutiamo le distanze di sicurezza 
    def safety_distance(self):
        return (self.speed/10)**2
    
    def notsafe(self):
        return A*(self.speed/10)**2 #potremmo agire sulla variabile "A" per variare le distanze di sicurezza

    def control_speed(self, time_passed):
        front_agent = agent.front_agent()  #questa funzione determina l'agente di fronte più vicino
        #se l'agente di fronte è più vicino della distanza di sicurezza mettiamo l'avviso "ALLERT" 
        if  front_agent is not None and abs(front_agent.x - self.x) <  (self.speed/10)**2:  #notare che che questa distanza di sicurezza è quello che andrebbe sempre rispettata che può essere diversa da quello attualemente rispettata dagli agenti
            self.text("ALLERT", (255, 0, 0), bg_color=None, x_offset=-self.radius, y_offset=-self.radius-20)
        #l'avviso "CODA" compare quando la velocità e l'accelerazione del nostro agente è minore di quella dell'agente di fronte 
        if front_agent is not None and self.ax< front_agent.ax and self.speed< front_agent.speed:
            self.text("CODA", (0, 128, 128), bg_color=None, x_offset=-self.radius, y_offset=-self.radius-10)
        
        # Se l'agente davanti è troppo vicino, rallenta
        if front_agent is not None and (abs(front_agent.x - self.x) <  self.safety_dist or abs(front_agent.x - self.x) <25):
            self.speed = (front_agent.speed-1)*0.99  #facciamo tendere la velocità dell'agente alla velocità dell'agente di fronte
            self.ax = (front_agent.ax) *0.99       #facciamo lo stesso per l'accelerazione

        # Altrimenti, se la velocità è inferiore alla velocità massima consentita, aumentala
        elif 0<= self.speed < MAX_SPEED:
            #se l'accelerazione non è al massimo, aumentiamola gradualmente, ogni incremento di 0.1 dovrebbe avvenire circa ogni 0.02secondi
            if self.ax< ACCMAX:
                self.ax += 0.02
            #controlliamo che l'incremento di velocità non ci faccia superare il limite
            if (self.speed + self.ax*time_passed)<=MAX_SPEED:
                self.speed += self.ax*time_passed
            #se il passaggio precedente non avviene significa che stiamo superando il limite, quindi settiamo la velocità dell'agente al limite e l'accelerazione a zero
            else:
                self.speed = MAX_SPEED
                self.ax = 0
        
        # evitiamo velocità negative.
        if self.speed<0:
            self.speed=1

    #questa funzione ritorna l'agente di fronte più vicino
    def front_agent(self):
        min_dist = 10000
        front_agent=None
        for inc in agents:
            if inc!=self:
                    dist= inc.x-self.x
                    if dist >0 and dist<min_dist:
                        min_dist=dist
                        front_agent=inc
        return front_agent
    
    #questo metodo è stato preso da un progetto di Leornardo Cortiana ed è utilizzato per scrivere i messaggi dell'agente
    def text(self, text, text_color=(255, 255, 255), bg_color=None, x_offset=0, y_offset=0):
        """
        write text on boid

        :param text: string type
        :param text_color: tuple(r,g,b)
        :param bg_color: tuple(r,g,b)
        :param x_offset: offset from boid center
        :param y_offset: offset from boid center
        :return: Nothing
        """
        text = str(text)
        white = (255, 255, 255)
        black = (0, 0, 0,)
        lines = text.splitlines()

        for i, l in enumerate(lines):
            text = font.render(l, True, text_color, bg_color)
            textRect = text.get_rect()
            h = textRect.height
            # textRect.center = (self.x, self.y + (h*i))
            textRect.topleft = (self.x + x_offset, self.y + y_offset + (h * i))
            screen.blit(text, textRect)

#questo metodo è stato preso da un progetto di Leornardo Cortiana ed è utilizzato per scrivere messaggi generici sullo schermo
def text_to_screen(text, text_color=(255, 255, 255), bg_color=None, x=0, y=0):
    """
    place a text on surface
    :param text: string
    :param text_color: tuple(r,g,b)
    :param bg_color: tuple(r,g,b)
    :param x: x
    :param y: y
    :return: Nothing
    """

    text = str(text)
    white = (255, 255, 255)
    black = (0, 0, 0)
    lines = text.splitlines()

    for i, l in enumerate(lines):
        text = font_menu.render(l, True, text_color, bg_color)
        textRect = text.get_rect()
        h = textRect.height
        # textRect.center = (self.x, self.y + (h*i))
        textRect.topleft = (x, y + (h * i))
        screen.blit(text, textRect)


# Inizializza Pygame
pygame.init()
# definisco colori e font utili
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font("freesansbold.ttf", 12)
font_menu = pygame.font.Font("freesansbold.ttf", 20)

#creo uno schermo di un dimensione determinate tra le variabili globali
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Crea un orologio per gestire il frame rate
clock = pygame.time.Clock()
agents = [] #lista in cui inserisco gli agenti
speedmean=[]#lista in cui inserisco la velocità media ad ogni iterazione
total_time=0 #variabile utilizzata per tenere il tempo totale

# Ciclo principale del gioco
running = True
while running:
    index =int(len(agents)/2) #identifichiamo l'indice di un agente nel mezzo e agiamo su di lui
    
    #ora creaimo i nostri agenti
    #se la lista di agenti non è vuota
    if  agents:
        #e se l'agente davanti ha una certa distanza dal bordo se la distanza di sicurezza è minore di 25 le auto si scontrerebbero quindi aspettiamo che ci siano almeno 25 pixels liberi
        if agents[-1].x > A*(agents[-1].speed/10)**2 and agents[-1].x > 25:
            x = 0
            y = 3*SCREEN_HEIGHT/4       #introduciamo un nuovo agente che avrà la stessa velocità dell'agente di fronte a lui
            speed = agents[-1].speed
            agents.append(Agent(x, y, speed))
    #se invece la lista di agenti è vuota, creiamo  il primo agente
    else:
        x = 0
        y = 3*SCREEN_HEIGHT/4
        speed = 2*MAX_SPEED/3
        agents.append(Agent(x, y, speed))

    #riempiamo lo schermo di colore nero (0,0,0)
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (50,50,50), (0, 4*SCREEN_HEIGHT/6,SCREEN_WIDTH,40))            #disegnamo un rettangolo grigio che rappresenta la strada
    pygame.draw.rect(screen, (255,255,255), (0, 4*SCREEN_HEIGHT/6+5,SCREEN_WIDTH,2))        #disegnamo due rettangoli bianchi che rappresentano le strisce
    pygame.draw.rect(screen, (255,255,255), (0, 4*SCREEN_HEIGHT/6+32,SCREEN_WIDTH,2))
    d_pressed=0     #variabile che tiene conto se è stata effettuata una frenata cosi quando andremo a guardare i dati raccolti sapremo quando è stata effettuata la frenata

    # Gestisci gli eventi di input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:  # detect one key pressed

            #prendendo "S" possiamo decidere o meno che vengano rispettate le distanze di sicurezza
            if event.key == pygame.K_s:
                if SAFE == True:
                    SAFE = False
                else:
                    SAFE = True
                    A=1.0
                for i in range(len(agents)):
                    if SAFE == False:
                        #if random.randrange(0,1)<0.75:
                            agents[i].safety_dist = agents[i].notsafe()
                        #else:
                        #    agents[i].safety_dist = agents[i].safety_distance()
                    else:
                            agents[i].safety_dist = agents[i].safety_distance()
            
            #premendo il pulsande "D", dimezziamo la velocità di un agent posto più o meno a metà schermo
            if event.key == pygame.K_d:
                agents[index].speed = 0.99*MAX_SPEED/2
                agents[index].ax = 0
                STOP = True
                d_pressed=1
                """for i in range(index, len(agents)):
                    agents[i].safe = False"""
            #dopo aver premudo "S" quindi con SAFE=False possiamo variare il parametro A che regola quanto rispettiamo la distanza di sicurezza
            if event.key == pygame.K_UP:
                A+=0.05
            if event.key == pygame.K_DOWN:
                A-=0.05
     

    text_to_screen("velocità massima: " + str(MAX_SPEED), x=5, y=10)
    text_to_screen("distanza di sicurezza: " + str(SAFE), x=300, y=10)
    text_to_screen("velocità agente " +str(index) +": " + str("%.1f" %agents[index].speed), x=600, y=10)
    agents[index].text("*", (255, 255, 255), bg_color=None, x_offset=-agents[0].radius+18, y_offset=-agents[0].radius-35)
    text_to_screen("premere D per fermare la macchina ", x=300, y=40)
    if SAFE == False:
        text_to_screen("dist di sicurezza " + str("%.1f" %A)+"%", x=900, y=10)
    # Aggiorna la posizione degli agenti
    time_passed = clock.tick(60) / 1000.0 # 0.02

    #creiamo una copia della lista cosi che quando un agente esce dallo spazio di simulazione, noi possiamo eliminarlo senza creare errori
    for obj in copy.copy(agents):
        if obj.x >= SCREEN_WIDTH:
            agents.remove(obj)
    total_time+=time_passed
    #analizziamo la velocità media
    if agents:
        tmpspeed=0
        n_agent=0
        for i,agent in enumerate(agents):
            if 0<=agent.x<=SCREEN_WIDTH:
                tmpspeed += agent.speed
                n_agent +=1
        #dopo aver calcolato la velocità media degli agenti sullo schermo lo scriviamo sullo schermo
        text_to_screen("velocità massima: " + str("%.1f" % (tmpspeed/n_agent)), x=900, y=40)
        speedmean.append([total_time,tmpspeed/n_agent,d_pressed,SAFE,A])

    #aggiorniamo le posizioni, le velocità e le accerazioni degli agenti in base al contesto
    for i, agent in enumerate(agents):
            agent.update(time_passed)           #per ogni agente aggiorniamo posizione
            agent.control_speed(time_passed)    #e controlliamo a aggiorniamo la velocità

    # Disegna gli agenti sullo schermo
    for agent in agents:
        pygame.draw.rect(screen, agent.color, (agent.x, agent.y,20,10))
    
    pygame.display.flip()
    text_to_screen("velocità massima: " + str(MAX_SPEED), x=5, y=10)
# Limit the frame rate to 60 FPS
clock.tick(60)
# Chiudi Pygame
pygame.quit()

"""data= pd.DataFrame(speedmean)
data.to_csv('speedmean.csv', index=False, quoting=1)"""


