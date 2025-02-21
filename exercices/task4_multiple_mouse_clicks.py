import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 750
# Fenstergrösse kann verändert werden
RESIZABLE = True
# Du musst request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird
ALWAYS_REDRAW = False


# Ein Aufbewahrungsort für Variablen, die wir in mehreren Funktionen benötigen,
# als Alternative zu globalen Variablen.
g = VarContainer()
g.mouse_coords = []
g.meine_lieblings_netflix_serie = "...."
g.mein_lieblings_lied = "Alle meine Entlein"


def on_draw():
    w, h = get_window_size()

    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = Color(30, 30, 50)
    draw_filled_rect((0, 0), (w, h), background_color)

    # Zeichnet zentrierten Text in die Mitte des Fensters
    for pos in g.mouse_coords:
        draw_filled_circle(pos, 5, RED)


def on_input(event):
    if event.type == MOUSEBUTTONDOWN:
        g.mouse_coords.append(event.pos)
        request_redraw()


def on_ready():
    set_window_title("Aufgabe 4.2 - Mehrere Mausklicks")


# Startet das Grafikprogramm.
go()
