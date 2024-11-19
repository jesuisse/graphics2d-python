from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 800
HEIGHT = 800

# Die Grösse des Grafikfensters soll angepasst werden können
RESIZABLE = True

peach_image = None

def on_draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Grösse des Grafikfensters ausfindig machen
    breite, höhe = get_window_size()
       
    # Zeichnet ein weisses Rechteck in den Dimensionen des Grafikfensters
    draw_filled_rect((0, 0), (breite, höhe), WHITE)
    
    # Zeichnet ein kleineres Rechteck
    draw_filled_rect((40, 20), (100, 60), BLUE)
    
    # Zeichnet einen rechteckigen Rahmen mit dickem Rand
    draw_rect((160, 20), (100, 60), CYAN, 5)
    
    # Zeichnet einige Linien
    draw_line((300, 20), (400, 80), MAGENTA, 1)
    draw_line((420, 20), (520, 80), MAGENTA, 2)
    draw_line((540, 20), (640, 80), MAGENTA, 3)

    # Zeichnet 2 Kreise, abhänging von der Grösse des Grafikfensters
    radius = (breite/8)    
    draw_filled_circle((breite/3, höhe/2), radius, RED)
    draw_circle((2*breite/3, höhe/2), radius, RED, 1)
    
    # Zeichnet Polygone, abhänging von der Grösse des Grafikfensters
    points = [(0.2, 0.7), (0.3, 0.9), (0.1, 0.8)]
    points = [ (x*breite, y*höhe) for x,y in points ]   # Rechnet Punkte auf Fenstergrösse um
    draw_polyline(points, GREEN, True, 2)
    
    points = [(0.6, 0.7), (0.8, 0.9), (0.5, 0.8)]
    points = [ (x*breite, y*höhe) for x,y in points ]   # Rechnet Punkte auf Fenstergrösse um
    draw_filled_polygon(points, GREEN)

    # Rendert Text
    fontname = get_default_fontname()
    fontsize = 30
    draw_text(fontname, fontsize, "Dare to do peachy things!", (40, 200), Color("orange"))

    # Render an image
    if peach_image:
        draw_surface(peach_image, (450, 170))


def on_ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    

    # Lade ein Bild
    global peach_image
    try:
        peach_image = load_image("graphics2d/assets/peach-icon1.png")
    except FileNotFoundError:
        print("Bilddatei nicht gefunden...")

    # Setze Fenstertitel
    set_window_title("Demo 0 - Drawing")
    

# Konfiguriert und startet das Grafikprogramm.
go()
