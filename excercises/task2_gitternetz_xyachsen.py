import sys
sys.path.append("..")

from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 700

# Wenn ALWAYS_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird.
ALWAYS_REDRAW = False

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
RESIZABLE = True


def draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = WHITE
    w, h = get_window_size()
    draw_filled_rect((0, 0), (w, h), background_color)
    draw_grid(50, Color(200, 200, 200))

def draw_grid(step, gridcolor):
    w, h = get_window_size()
    # Zeichnet Achsen
    draw_line((0, h/2), (w, h/2), RED, 1)
    draw_line((w/2, 0), (w/2, h), GREEN, 1)
    
    # Zeichnet ein Gitternetz
    xcount = int(w/2/step)+1
    ycount = int(h/2/step)+1

    for x in range(1, xcount):
        draw_line((w/2+x*step, 0), (w/2+x*step, h), gridcolor, 1)
        draw_line((w/2-x*step, 0), (w/2-x*step, h), gridcolor, 1)
    for y in range(1, ycount):
        draw_line((0, h/2+y*step), (w, h/2+y*step), gridcolor, 1)
        draw_line((0, h/2-y*step), (w, h/2-y*step), gridcolor, 1)
    

def ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    

    # Setze Fenstertitel
    set_window_title("Aufgabe: Gitternetz mit Achsen")


# Startet das Grafikprogramm.
go()
