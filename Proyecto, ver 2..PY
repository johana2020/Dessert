import random
import sys
import pygame as pyg
#from pygame.locals import *
import pygame

#figuras
trebol = "T"
pica = "P"
corazon = "C"
diamante = "D"
figuras = [trebol, pica, corazon, diamante]

#areas del tablero
palo = 0
maz_arriba = 1
mazo = 2
carta_boca_arriba = 3

#estado
abajo = 0
arriba = 1

#colores
negro = 0
rojo = 1

#distancias entre las cartas
dis_x_palo = 50
dis_y_palo = 20

#posiciones iniciales pilas
palo_x_ini = 10
palo_y_ini = 80

#posicion inicial mazo
maz_x_ini = 10
maz_y_ini = 10

#posicion inicial pilas_subir
maz_arriba_XINICIAL = maz_x_ini+dis_x_palo*3
maz_arriba_YINICIAL = maz_y_ini

#posicion inicial cartas carta_boca_arriba
mostr_pos_x = maz_x_ini + dis_x_palo
mostr_pos_y = maz_y_ini

#tamano de las cartas
TAMX_CARTA = 79
TAMY_CARTA = 53

#distancia entre las que se muestran
DISTX_MOSTRADA = 10

#cartas a mostrar
CARTAS_MOSTRAR = 3

#pygame
LEFT = 1

#ventana
WIDTH = palo_x_ini*2 + dis_x_palo*7
HEIGHT = 500

def load_image(filename, transparent=False):
		try: image = pygame.image.load(filename)
		except pygame.error:
				raise (SystemExit)
		image = image.convert()
		if transparent:
				color = image.get_at((0,0))
				image.set_colorkey(color)
		return image

class Carta(pygame.sprite.Sprite):
	def _init_(self, numero, pinta, posx=-1, posy=-1):
		self.pila = None
		self.clicked = False
		self.pinta = pinta
		if pinta == trebol or pinta == pica:
			self.color = negro
		else:
			self.color = rojo
		self.numero = numero
		self.estado = abajo
		# pygame
		self.image = load_image("cards\\back.png")
		self.arri_izq(posx, posy)
        
	def arri_izq(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.posfx = self.posx
		self.posfy = self.posy
		self.rect.topleft = (self.posx, self.posy)
        
	def arrastrar(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x-TAMX_CARTA/2
		self.posy = y-TAMY_CARTA/2
		self.rect.topleft = (self.posx, self.posy)
        
	def centr(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x-TAMX_CARTA/2
		self.posy = y-TAMY_CARTA/2
		self.posfx = self.posx
		self.posfy = self.posy
		self.rect.topleft = (self.posx, self.posy)

	def mostrar(self):
		if(self.estado == abajo):
			self.estado = arriba
			self.image = load_image("cards\\"+self.pinta+str(self.numero+1)+".png")
			print ("cards\\"+self.pinta+str(self.numero)+".png")
            
	def ocultar(self):
		if(self.estado == arriba):
			self.estado = abajo
			self.image = load_image("cards\\back.png")
            
	def cambiar(self):
		if(self.estado == arriba):
			self.ocultar()
		else:
			self.mostrar()
            

class maz_arriba(pygame.sprite.Sprite):
	def _init_(self, pinta, posx=-1, posy=-1):
		self.pinta = pinta
		self.image = load_image("cards\\"+pinta+".png")
		self.arri_izq(posx, posy)
		self.cartas = []
        
	def arri_izq(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)


class mazo(pygame.sprite.Sprite):
	def _init_(self):
		self.image = load_image("cards\\back.png")
		self.arri_izq(maz_x_ini, maz_y_ini)
		self.cartas = []
		self.crearmazo()
		self.revolver()
        
	def arri_izq(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)

	def crearmazo(self):
		for pinta in figuras:
			for numero in range(13):
				new_carta = Carta(numero, pinta)
				self.cartas.append(new_carta)

	def revolver(self):
		random.shuffle(self.cartas)
    

class Juego:
	def _init_(self):
		self._running = True
		self.screen = None
		self.size = self.width, self.height = WIDTH, HEIGHT
        
	#reparte las cartas en las 7 pilas
	def on_init(self):
		pyg.init()
		self.screen = pyg.display.set_mode(self.size)
		pyg.display.set_caption("Dissert.")
		self.background = load_image('cards/bg.png')
		self.pilas = []
		self.pilas_subir = []
		self.carta_boca_arriba = []
		self.maz = mazo()
		self.posibi()
        
	def on_loop(self):
		if self.dragging:
			desp = 0
			for card in self.dragging:
				card.arrastrar(pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1]+desp)
				desp += dis_y_palo
		#Verificar si gano
		f = True
		for pilasub in self.pilas_subir:
			if len(pilasub.cartas) != 13:
				f = False
		if f:
			self.ganar()
            
	def ejecucion(self):
		self.dragging = []
		self.clicked_sprites = []
		if self.on_init() == False:
			self._running = False
		while self._running:
			for event in pyg.event.get():
				self.evento(event)
			self.on_loop()
			self.on_render()
		self.limpiar()

	def on_render(self):
		self.screen.blit(self.background, (0, 0))
		#dibujar mazo
		self.screen.blit(self.maz.image, self.maz.rect)
		#dibujar subidas
		for pinta in self.pilas_subir:
			self.screen.blit(pinta.image, pinta.rect)
			for carta_p in pinta.cartas:
				self.screen.blit(carta_p.image, pinta.rect)
		#dibujar pilas
		for pila in self.pilas:
			for card in pila:
				if not card in self.dragging:
					self.screen.blit(card.image, card.rect)
		#dibujar carta_boca_arriba
		for ncart, card in enumerate(self.carta_boca_arriba[-CARTAS_MOSTRAR:]):
			if not card in self.dragging:
				card.arri_izq(mostr_pos_x+DISTX_MOSTRADA*ncart, mostr_pos_y)
				self.screen.blit(card.image, card.rect)
		#dibujar arrastrando, al final para que no se tapen
		for card in self.dragging:
			self.screen.blit(card.image, card.rect)
		pyg.display.flip()
	def limpiar(self):
		pyg.quit()

	def evento(self, evento):
		if evento.type == pygame.QUIT:
			self._running = False
		elif evento.type == pyg.KEYDOWN:
			if evento.key == pyg.K_ESCAPE:
				self.on_init()
		elif evento.type == pyg.MOUSEBUTTONDOWN:
			pos = pyg.mouse.get_pos()
			#juntar todos los sprites y guardar los clickeados.
			tipo = None
			for i in self.pilas:
				for x in i:
					if x.rect.collidepoint(pos):
						tipo = palo
						self.clicked_sprites.append(x)

			for i in self.carta_boca_arriba:
				if i.rect.collidepoint(pos):
					tipo = carta_boca_arriba
					self.clicked_sprites.append(i)

			if self.clicked_sprites:
				clickeada = self.clicked_sprites[-1]
				if tipo == carta_boca_arriba:
					if clickeada == self.carta_boca_arriba[-1]:
						self.dragging.append(clickeada)
				elif tipo == palo :
					if clickeada.estado == arriba:
						clickea_index_pila = clickeada.pila.index(clickeada) #obtener el indice de la ultima carta clickeada
						for cartasacar in clickeada.pila[clickea_index_pila:]: #arrastrar desde la ultima hacia abajo
							self.dragging.append(cartasacar)
					else: #si esta hacia abajo y se clickea voltearla
						if clickeada == clickeada.pila[-1]:
							clickeada.mostrar()
		elif evento.type == pyg.MOUSEBUTTONUP:
			pos = pyg.mouse.get_pos()
			tipo_drop, piladrop_index = self.area_palo(pos[0], pos[1])
			if(tipo_drop == palo):
				if self.dragging:
					piladrop = self.pilas[piladrop_index]
					if(piladrop):
						if(piladrop_index != -1 and self.parejas(self.dragging[0], piladrop[-1])):
							for card in self.dragging:
								if card.pila:
									card.pila.remove(card)
								else:
									self.carta_boca_arriba.remove(card)
								card.arri_izq(piladrop[-1].posx, piladrop[-1].posy+dis_y_palo)
								piladrop.append(card)
								card.pila = piladrop
					else: #Si esta vacia, revisar que sea K 
						if piladrop_index!=-1 and self.dragging[0].numero == 12:
							for card in self.dragging:
								if card.pila:
									card.pila.remove(card)
								else:
									self.carta_boca_arriba.remove(card)
								if(card == self.dragging[0]):
									self.dragging[0].arri_izq(palo_x_ini+(piladrop_index*dis_x_palo), palo_y_ini)
								else:
									card.arri_izq(piladrop[-1].posx, piladrop[-1].posy+dis_y_palo)
								piladrop.append(card)
								card.pila = piladrop
			elif(tipo_drop == maz_arriba and len(self.dragging)==1):
				if self.dragging:
					card = self.dragging[0]
					if(card.pinta == piladrop_index.pinta):
						if card.numero == 0:
							self.subir(card, piladrop_index)
						if piladrop_index.cartas:
							if card.numero == piladrop_index.cartas[-1].numero+1:
								self.subir(card, piladrop_index)
			elif(tipo_drop == mazo):
				if self.maz.cartas:
					for card in self.maz.cartas[:CARTAS_MOSTRAR]:
						self.maz.cartas.remove(card)
						card.mostrar()
						self.carta_boca_arriba.append(card)
				else:
					while self.carta_boca_arriba:
						card = self.carta_boca_arriba[0]
						self.maz.cartas.append(card)
						self.carta_boca_arriba.remove(card)
			for card in self.dragging:
				card.arri_izq(card.posfx, card.posfy)
			self.dragging = []
			self.clicked_sprites = []

#----- FUNCIONES DEL JUEGO -----
	def ganar(self):
		print ("GANASTEEEEEEEEE")
		self._running = False
        
	def subir(self, card, piladrop_index):
		if card.pila:
			card.pila.remove(card)
		else:
			self.carta_boca_arriba.remove(card)
		card.arri_izq(piladrop_index.posx, piladrop_index.posy)
		piladrop_index.cartas.append(card)
		card.pila = piladrop_index

	def posibi(self):
		xact = palo_x_ini
		for pilaact in range(7): 
			yact = palo_y_ini
			pila = []
			for numcarta in range(pilaact+1): 
				carta_ins = self.maz.cartas[0]
				carta_ins.arri_izq(xact, yact)
				carta_ins.pila = pila
				pila.append(carta_ins)
				self.maz.cartas.remove(carta_ins)
				if numcarta==pilaact: # Si es la ultima carta de la pila
					carta_ins.mostrar()
				yact += dis_y_palo
			self.pilas.append(pila)
			xact += dis_x_palo

		#Crear pilas donde se suben las cartas
		deltax = 0
		for pinta in figuras:
			p = maz_arriba(pinta)
			p.arri_izq(maz_arriba_XINICIAL+deltax, maz_arriba_YINICIAL)
			self.pilas_subir.append(p)
			deltax+= dis_x_palo

	#Retorna en que pila esta la posicion pos
	def area_palo(self, posx, posy):
		#revisar si el click es en el mazo
		p_xi = self.maz.posx
		p_xf = p_xi + TAMX_CARTA
		p_yi = self.maz.posy
		p_yf = p_yi + TAMY_CARTA
		if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
			return mazo, self.maz
		#revisar si el click es en las cartas carta_boca_arriba
		p_xi = mostr_pos_x
		p_xf = p_xi + TAMX_CARTA
		p_yi = mostr_pos_y
		p_yf = p_yi + TAMY_CARTA
		if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
			return carta_boca_arriba, None
		for pilaact in range(7):
			p_xi = palo_x_ini + (pilaact*dis_x_palo)
			p_xf = p_xi + TAMX_CARTA
			p_yi = palo_y_ini
			p_yf = p_yi + TAMY_CARTA + (dis_y_palo*pilaact)
			if(posx > p_xi and posx < p_xf and posy > p_yi):
				return palo, pilaact
		for pila_subir in self.pilas_subir:
			p_xi = pila_subir.posx
			p_xf = p_xi + TAMX_CARTA
			p_yi = pila_subir.posy
			p_yf = p_yi + TAMY_CARTA
			if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
				return maz_arriba, pila_subir
		return -1, -1
    
	#Recibe 2 cartas y retorna si c2 se puede poner sobre c1
	def parejas(self, c1, c2):
		if(c1.color != c2.color and c1.numero+1 == c2.numero):
			return True
		else:
			return False
if __name__ == "__main__":
    juego = Juego()
    juego.ejecucion()
