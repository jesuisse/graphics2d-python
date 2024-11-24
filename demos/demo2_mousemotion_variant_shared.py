import sys, os.path
sys.path.append(os.path.join(sys.path[0], ".."))

from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 750

# Du musst request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird
ALWAYS_REDRAW = False

# Fenstergrösse kann vom Benutzer verändert werden
RESIZABLE = True

# Ein Aufbewahrungsort für Variablen, die wir in mehreren Funktionen benötigen,
# als Alternative zu globalen Variablen.
g = VarContainer()
g.mouse_coords = None
g.clicked = False
g.clicked_at_time = 0
g.xpos = 0

def calc_centered_position(text, fontname, fontsize):
    w, h = get_window_size()
    tw, th = get_text_size(fontname, fontsize, text)
    return (w/2-tw/2, h/2-th/2)


def on_draw():
    w, h = get_window_size()

    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = Color(30, 30, 50)
    draw_filled_rect((0, 0), (w, h), background_color)

    # Zeichnet zentrierten Text in die Mitte des Fensters
    if g.mouse_coords:
       text = "Mauszeiger bei ({},{})".format(g.mouse_coords[0], g.mouse_coords[1])
    else:
        text = "Noch keine Mausbewegung"

    font = get_default_fontname()
    fontsize = 25
    x, y = calc_centered_position(text, font, fontsize)
    if abs(x-g.xpos) > 10:
        g.xpos = x

    draw_text(font, fontsize, text, (g.xpos, y), Color(200, 200, 200))

    if g.clicked_at_time and get_runtime_in_msecs()-g.clicked_at_time < 1000:
        x, y = calc_centered_position("Du hast geklickt!", font, fontsize)
        y = 40
        draw_text(font, fontsize, "Du hast geklickt!", (x, y), Color(220, 220, 0))


def on_input(event):

    if event.type == MOUSEMOTION:
        g.mouse_coords = event.pos
        # Wir müssen das framework informieren, dass der Fensterinhalt neu gezeichnet
        # werden soll, ansonsten sehen wir die neuen Koordinaten nicht!
        request_redraw()

    if event.type == MOUSEBUTTONDOWN:
        g.clicked = True
        g.clicked_at_time = get_runtime_in_msecs()
        request_redraw()


def on_ready():
    set_window_title("Demo 2 - Mouse Motion")


# Startet das Grafikprogramm.
go()
