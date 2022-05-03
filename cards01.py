import random
import pygame
import sys
class Cartas(pygame.sprite.Sprite):
    figuras = ["trebol", "picas","diamante", "corazon"]
    numeros = ["A","2","3","4","5","6","7","8","9","10",
               "J","Q","K"]
    def __init__(self, figura, numero=0, face="",color=""):
        super().__init__()
        self._figura = figura
        self._numero = numero
        self.face=face
        if self.figura ==0 or self.figura ==1:
            self.color= "negro"
        elif self.figura==2 or self.figura==3:
            self.color="rojo"
    @property
    def figura(self):
        return self._figura
    @property
    def numero(self):
        return self._numero   
    def __str__(self):
       return (f'{self.numeros[self.numero]} de {self.figuras[self.figura]}, color: {self.color}, está {self.face}')
class Baraja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.baraja =[]
        self.baraja_arriba=[]
        for figura in range(4):
            for numero in range(13):   
                lado=random.choice(["boca_abajo", "boca_arriba"])
                if lado=="boca_arriba":
                    if len(self.baraja_arriba)<7:
                        carta = Cartas(random.randint(0, 3), random.randint(0, 12), lado)
                        while carta in self.baraja_arriba and carta in self.baraja:
                               carta = Cartas(random.randint(0, 3), random.randint(0, 12), lado)
                        self.baraja_arriba.append(carta)       
                    else:
                        lado= "boca_abajo"
                        carta = Cartas(figura, numero, lado)
                        while carta in self.baraja and carta in self.baraja_arriba:
                               carta = Cartas(random.randint(0, 3), random.randint(0, 12), lado)
                        self.baraja.append(carta)            
                else:
                    carta=Cartas(figura,numero,lado)
                    while carta in self.baraja and carta in self.baraja_arriba:
                           carta = Cartas(random.randint(0, 3), random.randint(0, 12), lado)
                    self.baraja.append(carta) 
    def imagen (self):
        x=40
        y=70
        x1=700
        y1=30
        wn=pygame.display.set_mode((800,500))#longitudes de ventana
        green=51,162,0
        clock=pygame.time.Clock()
        wn.fill(green) #color de fondo
        while len(self.baraja_arriba)>0 and len(self.baraja)>0:
            for carta in self.baraja_arriba:
                fig=carta.figura
                num=carta.numero
                card=pygame.image.load("cards/{0}{1}.png".format(fig,num)).convert()#buscar la carta
                x+=40    
                y+=20
                wn.blit(card,[x,y]) #ubicación y ancho/largo
                self.baraja_arriba.remove(carta)
            for carta2 in self.baraja:
                figu=carta2.figura
                nume=carta2.numero
                cards=pygame.image.load("cards/boca_abajo.png").convert()#buscar la carta
                #x1-=20   
                y1+=0
                wn.blit(cards,[x1,y1]) #ubicación y ancho/largo
                self.baraja.remove(carta2)
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            clock.tick(60)
baraja=Baraja()
wn=baraja.imagen()

