import os, os.path, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from graphics2d import *


# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 700

# Wenn ALWAYS_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird.
ALWAYS_REDRAW = False

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
RESIZABLE = True

# Geschwindigkeiten der 3 Kreise
v1 = 0.1
v2 = 0.2
v3 = 0.15

# Mittelpunkt-Koordinaten der 3 Kreise
kreis1 = [0, 0]
kreis2 = [0, 0]
kreis3 = [0, 0]

def on_draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = WHITE
    w, h = get_window_size()
    draw_filled_rect((0, 0), (w, h), background_color)
    
    # Zeichnet 3 Kreise    
    draw_filled_circle(kreis1, 10, GREEN)
    draw_filled_circle(kreis2, 12, BLUE)
    draw_filled_circle(kreis3, 15, RED)
    

def on_update(dt):
    w, h = get_window_size()
    
    # Kreis 1: Horizontale Kreisbewegung
    kreis1[0] = kreis1[0] + dt*v1
    kreis1[1] = h/2
    if kreis1[0] > w:
        kreis1[0] = 0
    
    # Kreis 2: Vertikale Kreisbewegung
    kreis2[0] = w/2
    kreis2[1] = kreis2[1] + dt*v2
    if kreis2[1] > h:
        kreis2[1] = 0
    
    # Kreis 3: Diagonale Kreisbewegung
    kreis3[0] = kreis3[0] + dt*v3
    kreis3[1] = kreis3[1] + dt*v3
    if kreis3[0] > w:
        kreis3[0] = 0
    if kreis3[1] > h:
        kreis3[1] = 0
      
    request_redraw()
 

def on_input(event):
    if event.type == MOUSEBUTTONDOWN and event.button==1:
        save_screen("screenshot.png")

def on_ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    

    # Setze Fenstertitel
    set_window_title("Aufgabe: Bewegte Kreise")


# Startet das Grafikprogramm.
go()
