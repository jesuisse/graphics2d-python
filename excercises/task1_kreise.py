import sys
sys.path.append("..")

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



image = None

def on_draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = WHITE
    w, h = get_window_size()
    draw_filled_rect((0, 0), (w, h), background_color)
    
    # Zeichnet konzentrische Kreise
    count = int(min(w, h)/20)
    for i in range(count):
        draw_circle((w/2, h/2), w/2-i*20, BLACK, width=2)
        

def on_input(event):
    if event.type == MOUSEBUTTONDOWN and event.button==1:
        save_screen("screenshot.png")

def on_ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    

    # Setze Fenstertitel
    set_window_title("Aufgabe: Kreise")
   


# Startet das Grafikprogramm.
go()
