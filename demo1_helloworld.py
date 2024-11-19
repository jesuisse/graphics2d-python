from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 750

# Wenn ALWAYS_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird. Da der Zustand der Grafik hier
# nicht wegen Benutzerinput oder verstreichender Zeit von Frame zu Frame ändert, setzen wir ALWAYS_REDRAW auf
# False, um CPU-Ressourcen zu sparen.
ALWAYS_REDRAW = False

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann - in diesem Fall ja.
RESIZABLE = True


image = None

def on_draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
   
    # Füllt das ganze Fenster mit einer Hintergrundfarbe
    background_color = Color(30, 30, 50)
    w, h = get_window_size()
    draw_filled_rect((0, 0), (w, h), background_color)
    
    # Zeichnet zentrierten Text in die Mitte des Fensters
    text = "Hello World!"    
    font = get_default_fontname()
    fontsize = 50
    tw, th = get_text_size(font, fontsize, text)
    pos = (w/2-tw/2, h/4-th/2)
    draw_text(font, fontsize, text, pos, Color(200, 200, 200))
    
    # Zeichnet das geladene Baum-Bild auf den Bildschirm
    if image:
        iw, ih = image.get_size()
        draw_surface(image, (w/2-iw/3,h-ih))


def on_ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    
    
    global image

    # Setze Fenstertitel
    set_window_title("Demo 1")
    # Versuche eine Grafik zu laden, aber nicht verzweifeln, wenn sie nicht da ist...
    try:
        image = load_image("resources/tree.png")
    except FileNotFoundError:
        print("Could not find image, going on without it...")




# Startet das Grafikprogramm.
go()
