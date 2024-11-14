"""
template.py

Dieses Programm tut nichts ausser ein schwarzes Fenster anzeigen. Du kannst es als Startpunkt für eigene grafische
Programme verwenden.
"""

from graphics2d import *

# Diese Konstanten legen die Grösse des Grafikfensters fest
WIDTH = 500
HEIGHT = 500

# Wenn ALWAYS_REDRAW True ist (Default), dann wird das ganze Fenster in jedem Frame mit draw() neu gezeichnet.
# Ansonsten musst du request_redraw() aufrufen, wenn du in einem Frame Änderungen machst, welche
# ein Neuzeichnen mittels draw() nötig machen.
#ALWAYS_REDRAW = False

# Legt die maximale Framerate fest. Default ist 60.
#MAX_FPS = 120

# Legt fest, ob das Fenster im Fullscreen-Modus geöffnet wird. Default ist False.
#FULLSCREEN = True

# Legt fest, ob die Grösse des Fensters vom Benutzer verändert werden kann. Default ist False.
#RESIZABLE = True



def draw():
    # Wird aufgerufen, um den Inhalt des Grafikfensters neu zu zeichnen
    pass

def update(dt):
    # Wird so oft wie möglich aufgerufen, aber maximal MAX_FPS mal pro Sekunde. dt gibt die Anzahl Millisekunden seit
    # dem letzten Aufruf an.    
    pass

def input(event):    
    # Wird aufgerufen, wenn ein Ereignis (z.B. ein Mausklick oder ein Tastendruck) vorliegt
    pass    

def ready():
    # Wird aufgerufen, wenn das Grafik-Framework bereit ist, unmittelbar vor dem Start der Event Loop.    
    set_window_title("Langweiliges schwarzes Fenster")

def resized(new_width, new_height):
    # Wird aufgerufen, wenn die Grösse des Grafikfensters verändert wird
    pass

def exit():
    # Wird aufgerufen, bevor die Applikation beendet wird.
    pass


# Startet das Grafikprogramm.
go()
