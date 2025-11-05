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

class Polygon:
    def __init__(self, fill_color, stroke_color):
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.points = []
        
    def is_valid(self):
        return len(self.points) > 1
    
    def add_point(self, pos):
        self.points.append(pos)

    def is_closing_point(self, pos):
        if not self.is_valid():
            return False
        first = self.points[0]
        distance = 5
        return (first[0]-pos[0])**2 + (first[1]-pos[1])**2 < distance**2


        



# Ein Aufbewahrungsort für Variablen, die wir in mehreren Funktionen benötigen,
# als Alternative zu globalen Variablen.
g = VarContainer()
g.active_polygon = Polygon(BLUE, GREEN)
g.finished_polygons = []


def on_draw():
    w, h = get_window_size()

    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = WHITE #Color(30, 30, 50)
    draw_filled_rect((0, 0), (w, h), background_color)


    polylinecolor = Color(70, 70, 70)

    # Zeichnet fertige Polygone
    greyscale = 80
    for polygon in g.finished_polygons:        
        draw_filled_polygon(polygon.points, polygon.fill_color)

    # Zeichnet ein noch nicht fertiges Polygon
    if g.active_polygon.is_valid():
        draw_polyline(g.active_polygon.points, g.active_polygon.stroke_color, False, 2)
    for pos in g.active_polygon.points:
        draw_filled_circle(pos, 5, RED)


def is_closer_than(a, b, distance):
    # Pythagoras
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 < distance**2

def on_input(event):
    if event.type == MOUSEBUTTONDOWN:
        if len(g.active_polygon_points) > 0 and is_closer_than(g.active_polygon_points[0], event.pos, 5):
            # Wir haben ein fertiges Polygon
            g.finished_polygons.append(g.active_polygon)
            g.active_polygon = Polygon(BLUE, GREEN)
        else:
            g.active_polygon.add_point(event.pos)
        request_redraw()


def on_ready():
    set_window_title("Aufgabe 5 - Polygone zeichnen")


# Startet das Grafikprogramm.
go()
