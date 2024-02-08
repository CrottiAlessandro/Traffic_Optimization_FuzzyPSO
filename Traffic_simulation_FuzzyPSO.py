

import pygame
import random
import numpy as np
import pandas as pd
from itertools import count
import copy
from fstpso import FuzzyPSO

# Costanti
"""SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 200
MAP_WIDTH = int(SCREEN_WIDTH * 2 / 3)
MAP_HEIGHT = int(SCREEN_HEIGHT)
MAX_SPEED = 100
SAFE = True
ACCMAX=10
AUTOPILOT=True
STOP=False
MAX_SPEED = 100
A=1.0 #costante che diminuisce la dist di sicurezza
n_maxagent =5"""

#MAX_SPEED, A e n_maxagent sono parametri che vogliamo ottimizzare come fitness determiniamo che la velocità media in strada deve restare il più alta possibile 
#mantenendo comunque massimizzata la velocità e il numero di auto in strada
dims = 2
FP = FuzzyPSO()
FP.set_search_space( [[80, 150],[0.5,1.3]])	

def example_fitness( cost):
    k1,k2=cost
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 200
    MAP_WIDTH = int(SCREEN_WIDTH * 2 / 3)
    MAP_HEIGHT = int(SCREEN_HEIGHT)
    SAFE = False
    ACCMAX=10
    AUTOPILOT=True
    STOP=False
    MAX_SPEED = k1
    A=k2 #costante che diminuisce la dist di sicurezza
    #n_maxagent =int(k3)
    # Classe Agent per rappresentare un'auto
    class Agent:
        _ids = count(0)
        def __init__(self, x, y, speed):
            self.id = next(self._ids) 
            self.x = x
            self.y = y
            self.speed = speed
            self.ax = random.randint(0,5)
            self.safety_dist = self.safety_distance()
            #self.safe = True
            self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.radius=20


        def update(self, time_passed):
            self.x += self.speed * time_passed # aggiorniamo la posizione dell'agente
            

        def safety_distance(self):
            return (self.speed/10)**2
        
        def notsafe(self):
            return A*(self.speed/10)**2

        def control_speed(self, time_passed):
            front_agent = agent.front_agent()
            if  front_agent is not None and abs(front_agent.x - self.x) <  (self.speed/10)**2:
                self.text("ALLERT", (255, 0, 0), bg_color=None, x_offset=-self.radius, y_offset=-self.radius-20)
            if front_agent is not None and self.ax< front_agent.ax and self.speed< front_agent.speed:
                self.text("CODA", (0, 128, 128), bg_color=None, x_offset=-self.radius, y_offset=-self.radius-10)
            
            # Se l'agente davanti è troppo vicino, rallenta
            if front_agent is not None and (abs(front_agent.x - self.x) <  self.safety_dist or abs(front_agent.x - self.x) <25):
                self.speed = (front_agent.speed-1)*0.99  #facciamo tendere la velocità dell'agente alla velocità dell'agente di fronte
                self.ax = (front_agent.ax) *0.99       #facciamo lo stesso per l'accelerazione
                #self.safety_dist = self.safety_distance() #inoltre se abbiamo tolto le distanze di sicurezza, se ci avviciniamo troppo le

            # Altrimenti, se la velocità è inferiore alla velocità massima consentita, la aumentiamo
            elif 0<= self.speed < MAX_SPEED:
                #se l'accelerazione non è al massimo, aumentiamola gradualmente ad ogni iterazione
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

        #questa funzione ritorna l'agente di fronte
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
        
        #questo metodo è stato preso da un progetto di Leornardo Cortiana
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

    #questo metodo è stato preso da un progetto di Leornardo Cortiana
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

    #questa funzione ritorna il numero di agenti presenti sullo schermo attraverso il quale possiamo regolare il flusso
    def n_agents(agents):
        n_agent=0
        for i,agent in enumerate(agents):
            if 0<=agent.x<=SCREEN_WIDTH:
                n_agent +=1
        return n_agent     
        



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
    agents = []  #lista in cui inserisco gli agenti
    speedmean=[]  #lista in cui inserisco la velocità media ad ogni iterazione
    total_time=0   #variabile utilizzata per tenere il tempo totale
    # Ciclo principale del gioco
    while total_time<40:
        index =int(len(agents)/2) #identifichiamo l'indice di un agente nel mezzo su cui poi potremmo agire
        
        #ora creaimo i nostri agenti, se il numero totale di agenti sullo schermo è minore del massimo valore che abbiamo determinato

        # e se la lista di agenti non è vuota
        if  agents:
                #e se l'agente davanti ha una certa distanza dal bordo se la distanza di sicurezza è minore di 25 le auto si scontrerebbero quindi aspettiamo che ci siano almeno 25 pixels liberi
                if agents[-1].x > A*(agents[-1].speed/10)**2 and agents[-1].x > 25:  
                    x = 0
                    y = 3*SCREEN_HEIGHT/4           #introduciamo un nuovo agente che avrà la stessa velocità dell'agente di fronte a lui
                    speed = agents[-1].speed
                    agents.append(Agent(x, y, speed))
            #se invece la lista di agenti è vuota, creiamo  il primo agente
        else:
                x = 0
                y = 3*SCREEN_HEIGHT/4
                speed = 3*MAX_SPEED/4 
                agents.append(Agent(x, y, speed))
        
        #riempiamo lo schermo di colore nero (0,0,0)
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, (50,50,50), (0, 4*SCREEN_HEIGHT/6,SCREEN_WIDTH,40))       #disegnamo un rettangolo grigio che rappresenta la strada
        pygame.draw.rect(screen, (255,255,255), (0, 4*SCREEN_HEIGHT/6+5,SCREEN_WIDTH,2))   #disegnamo due rettangoli bianchi che rappresentano le strisce
        pygame.draw.rect(screen, (255,255,255), (0, 4*SCREEN_HEIGHT/6+32,SCREEN_WIDTH,2))  
        d_pressed=0    #variabile che tiene conto se è stata effettuata una frenata cosi quando andremo a guardare i dati raccolti sapremo quando è stata effettuata la frenata

        if int(total_time)==15 and d_pressed==0:
                    agents[index].speed = 0.99*MAX_SPEED/2
                    agents[index].ax = 0
                    STOP = True
                    d_pressed=1
       
                        
        text_to_screen("velocità massima: " + str("%.1f" %MAX_SPEED), x=5, y=10)
        text_to_screen("distanza di sicurezza: " + str(SAFE), x=300, y=10)
        text_to_screen("velocità agente " +str(index) +": " + str("%.1f" %agents[index].speed), x=600, y=10)
        agents[index].text("*", (255, 255, 255), bg_color=None, x_offset=-agents[0].radius+18, y_offset=-agents[0].radius-35)

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
            speedmean.append(tmpspeed/n_agent)
            text_to_screen("velocità massima: " + str("%.1f" % (tmpspeed/n_agent)), x=1200, y=10)
     


        #aggiorniamo le posizioni, le velocità e le accerazioni degli agenti in base al contesto
        for i, agent in enumerate(agents):
                agent.update(time_passed)
                agent.control_speed(time_passed)

        # Disegna gli agenti sullo schermo
        for agent in agents:
            pygame.draw.rect(screen, agent.color, (agent.x, agent.y,20,10))
        
        pygame.display.flip()
        
    # Limit the frame rate to 60 FPS
    clock.tick(60)
    # Chiudi Pygame
    pygame.quit()
    return (-np.mean(speedmean))*float(max(speedmean))-float(min(speedmean))-k1*10+k2*1000+np.var(speedmean)
    #(a1/np.mean(speedmean))*float(max(speedmean))-float(min(speedmean))*(a2/k1)*(a3/k2)*(a4/k3)
    #float(max(speedmean))-float(min(speedmean))



FP.set_fitness(example_fitness)

result =  FP.solve_with_fstpso(max_iter=10)
print("Best solution:", result[0])
print("Whose fitness is:", result[1])

