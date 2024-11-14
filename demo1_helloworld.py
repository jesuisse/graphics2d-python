from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 700
HEIGHT = 750

# Wenn ALWAYS_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird.
ALWAYS_REDRAW = False

# Legt die maximale Framerate fest. Default ist 60.
#MAX_FPS = 120

# Legt fest, ob das Fenster im Fullscreen-Modus geöffnet wird. Default ist False.
#FULLSCREEN = True

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
RESIZABLE = True



TREE = load_image("resources/tree5.png")

def draw():
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
    pos = (w/2-tw/2, h/2-th/2)
    draw_text(font, fontsize, text, pos, Color(200, 200, 200))
    
    # Zeichnet das geladene Baum-Bild auf den Bildschirm
    draw_surface(TREE, (w/2-64,400))
        

def update(dt):
    # Wird so oft wie möglich aufgerufen, aber maximal MAX_FPS mal pro Sekunde. dt gibt die Anzahl Millisekunden seit
    # dem letzten Aufruf an.    
    pass

def input(event):
    # Wird aufgerufen, wenn ein Ereignis (z.B. ein Mausklick oder ein Tastendruck) vorliegt
    
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        pass

def ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    
    set_window_title("Demo 1")
        

def resized(new_width, new_height):
    # Wird aufgerufen, wenn die Grösse des Grafikfensters verändert wird
    print("resized window to new dimensions", new_width, new_height)

def exit():
    # Wird aufgerufen, bevor die Applikation beendet wird.
    print("Finishing now...")


# Startet das Grafikprogramm.
go()
