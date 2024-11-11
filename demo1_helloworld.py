from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 1200
HEIGHT = 800

# Wenn AUTO_REDRAW True ist, dann wird das ganze Fenster in jedem Frame neu gezeichnet. Ansonsten musst du
# request_redraw() aufrufen, wenn ein ein Update der Grafik benötigt wird.
#AUTO_REDRAW = False

# Legt die maximale Framerate fest. Default ist 120.
#MAX_FPS = 60

# Legt fest, ob das Fenster im Fullscreen-Modus geöffnet wird. Default ist False.
#FULLSCREEN = True

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
RESIZABLE = True


def draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
    w, h = get_size()
    draw_filled_rect(0, 0, w, h, Color(30, 30, 50))
    font = get_default_fontname()    
    draw_text(font, 50, "Hello World!", w/2-150, h/2-20, Color(200, 200, 200))

def update(dt):
    # Wird so oft wie möglich aufgerufen, aber maximal MAX_FPS mal pro Sekunde. dt gibt die Anzahl Millisekunden seit
    # dem letzten Aufruf an.    
    pass
    
def ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    
    print("Starting now...")

def resized(new_width, new_height):
    # Wird aufgerufen, wenn die Grösse des Grafikfensters verändert wird
    print("resized window to new dimensions", new_width, new_height)

def quit():
    # Wird aufgerufen, bevor die Applikation beendet wird.
    print("Finishing now...")

# Startet das Programm.
go()
