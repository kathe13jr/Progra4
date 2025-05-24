import turtle
import random
import time
from abc import ABC, abstractmethod

# Configuración inicial de la ventana
ventana = turtle.Screen()
ventana.title("Snake con Patrón Abstract Factory")
ventana.bgcolor("black")
ventana.setup(width=600, height=600)
ventana.tracer(0)

# Interfaz Abstract Factory
class FabricaComida(ABC):
    @abstractmethod
    def crear_comida(self):
        pass

# Clases concretas de comida
class Comida:
    def __init__(self, color, efecto):
        self.obj = turtle.Turtle()
        self.obj.shape("circle")
        self.obj.penup()
        self.obj.color(color)
        self.obj.speed(0)
        self.obj.goto(random.randint(-280, 280), random.randint(-280, 280))
        self.efecto = efecto

# Fábricas concretas
class FabricaVenenosa(FabricaComida):
    def crear_comida(self):
        return Comida("purple", "venenosa")

class FabricaFit(FabricaComida):
    def crear_comida(self):
        return Comida("green", "fit")

class FabricaGrasa(FabricaComida):
    def crear_comida(self):
        return Comida("yellow", "grasa")

class FabricaReyes(FabricaComida):
    def crear_comida(self):
        return Comida("orange", "reyes")

# Inicialización de la serpiente
cabeza = turtle.Turtle()
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = "stop"
segmentos = []

# Marcador
puntaje = 0
velocidad = 0.1
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 260)
marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))

# Movimiento
def mover():
    if cabeza.direction == "up":
        y = cabeza.ycor()
        cabeza.sety(y + 20)
    if cabeza.direction == "down":
        y = cabeza.ycor()
        cabeza.sety(y - 20)
    if cabeza.direction == "left":
        x = cabeza.xcor()
        cabeza.setx(x - 20)
    if cabeza.direction == "right":
        x = cabeza.xcor()
        cabeza.setx(x + 20)

# Teclas
def ir_arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"
def ir_abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"
def ir_izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"
def ir_derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

ventana.listen()
ventana.onkeypress(ir_arriba, "Up")
ventana.onkeypress(ir_abajo, "Down")
ventana.onkeypress(ir_izquierda, "Left")
ventana.onkeypress(ir_derecha, "Right")

# Crear comida aleatoria
def generar_comida():
    fabrica = random.choice([
        FabricaFit(), FabricaVenenosa(), FabricaGrasa(), FabricaReyes()
    ])
    return fabrica.crear_comida()

comida = generar_comida()

# Bucle principal del juego
while True:
    ventana.update()
    mover()

    # Detectar colisión con comida
    if cabeza.distance(comida.obj) < 20:
        efecto = comida.efecto
        comida.obj.goto(1000, 1000)  # Desaparece
        comida = generar_comida()  # Nueva comida

        if efecto == "fit":
            puntaje += 1
            nuevo_segmento = turtle.Turtle()
            nuevo_segmento.shape("square")
            nuevo_segmento.color("grey")
            nuevo_segmento.penup()
            segmentos.append(nuevo_segmento)
        elif efecto == "venenosa":
            puntaje = max(0, puntaje - 1)
            if segmentos:
                segmento_removido = segmentos.pop()
                segmento_removido.hideturtle()
        elif efecto == "grasa":
            puntaje += 3
            velocidad += 0.05
            nuevo_segmento = turtle.Turtle()
            nuevo_segmento.shape("square")
            nuevo_segmento.color("grey")
            nuevo_segmento.penup()
            segmentos.append(nuevo_segmento)
        elif efecto == "reyes":
            puntaje += 5
            velocidad = max(0.05, velocidad - 0.02)
            nuevo_segmento = turtle.Turtle()
            nuevo_segmento.shape("square")
            nuevo_segmento.color("gold")
            nuevo_segmento.penup()
            segmentos.append(nuevo_segmento)

        marcador.clear()
        marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))

    # Mover segmentos del cuerpo
    for i in range(len(segmentos)-1, 0, -1):
        x = segmentos[i-1].xcor()
        y = segmentos[i-1].ycor()
        segmentos[i].goto(x, y)
    if segmentos:
        segmentos[0].goto(cabeza.xcor(), cabeza.ycor())

    # Colisión con pared
    if abs(cabeza.xcor()) > 290 or abs(cabeza.ycor()) > 290:
        time.sleep(1)
        cabeza.goto(0, 0)
        cabeza.direction = "stop"
        for seg in segmentos:
            seg.hideturtle()
        segmentos.clear()
        puntaje = 0
        velocidad = 0.1
        marcador.clear()
        marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))

    time.sleep(velocidad)
