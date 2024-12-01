import os, os.path, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graphics2d import *


# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 700

# Wenn ALWAYS_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird.
ALWAYS_REDRAW = False

# Legt die maximale Framerate fest. Default ist 60.
#MAX_FPS = 120

# Legt fest, ob das Fenster im Fullscreen-Modus geöffnet wird. Default ist False.
#FULLSCREEN = True

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
RESIZABLE = True


STEP = 50

image = None

def on_draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = WHITE
    w, h = get_window_size()
    draw_filled_rect((0, 0), (w, h), background_color)
    
    # Zeichnet ein Gitternetz
    
    count = int(max(w, h) / 20)+1
    
    for x in range(1, count):
        draw_line((x*STEP, 0), (x*STEP, h), BLACK, 1)
    for y in range(1, count):
        draw_line((0, y*STEP), (w, y*STEP), BLACK, 1)
        


def on_ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    

    # Setze Fenstertitel
    set_window_title("Aufgabe: Gitternetz")
   


# Startet das Grafikprogramm.
go()
