import random


class Cartas:
    figuras = ["trebol", "picas","diamante", "corazon"]
    numeros = ["A","2","3","4","5","6","7","8","9","10",
               "J","Q","K"]
    colores=["negro","rojo"]
    
    def __init__(self, figura=0, numero=0, face="",color=""):
        self.figura = figura
        self.numero = numero
        self.face=face
        if self.figura ==0 or self.figura ==1:
            self.color= "negro"
        elif self.figura==2 or self.figura==3:
            self.color="rojo"

    def __str__(self):
       return (f'{self.numeros[self.numero]} de {self.figuras[self.figura]}, color: {self.color}, está {self.face}')


class Baraja:
    def __init__(self):
        self.baraja =[]
        self.baraja_arriba=[]
        for figura in range(4):
            for numero in range(13):   
                lado=random.choice(["boca_abajo", "boca_arriba"])
                if lado=="boca_arriba":
                    if len(self.baraja_arriba)<7:
                        carta = Cartas(figura, numero, lado)
                        self.baraja_arriba.append(carta)
                    else:
                        lado= "boca_abajo"
                        carta = Cartas(figura, numero, lado)
                        self.baraja.append(carta)
                else:
                    carta=Cartas(figura,numero,lado)
                    self.baraja.append(carta)

    def __str__(self):
        msn = ''
        for carta in self.baraja:
            msn += str(carta)
            msn += '\n'
        for arriba in self.baraja_arriba:
            msn += str(arriba)
            msn += '\n'
        return msn

baraja = Baraja()
print(baraja)
# class Pilares:

# class Face_down:
#------------------------------------------- restricciones------------------------------------------------












