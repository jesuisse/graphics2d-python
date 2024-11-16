from graphics2d import *

WIDTH = 700
HEIGHT = 700

g = VarContainer()

g.dragging = False
g.planet = None

def closer_to_planet_than(coords, maxdist):
    # Liefert True, wenn coords näher am Planetenzentrum sind als maxdist
    size = g.planet.get_size()
    dx = g.planet_position.x + size[0]/2 - coords[0]
    dy = g.planet_position.y + size[1]/2 - coords[1]
    return dx**2 + dy**2 < maxdist**2

def draw():    
    draw_filled_rect((0, 0), get_window_size(), BLACK)
    draw_surface(g.planet, g.planet_position)

def input(event):
    if event.type == MOUSEBUTTONDOWN and event.button == 1 and closer_to_planet_than(event.pos, 125):
        g.dragging= True
    elif event.type == MOUSEBUTTONUP and event.button == 1:
        g.dragging = False
    
    if g.dragging and event.type == MOUSEMOTION:
        g.planet_position += Vector2(event.rel)
        
        # Sorgt dafür, dass wir den Planeten nicht aus dem Fenster schieben können
        w, h = get_window_size()
        pw, ph = g.planet.get_size()
        if g.planet_position.x < -pw/2:
            g.planet_position.x = -pw/2
        elif g.planet_position.x > w-pw/2:
            g.planet_position.x = w-pw/2
        if g.planet_position.y < -ph/2:
            g.planet_position.y = -ph/2
        elif g.planet_position.y > h-ph/2:
            g.planet_position.y = h-ph/2
                   


def ready():
    set_window_title("Demo 4 - Drag and Drop")
    g.planet = load_image("resources/planet-cc0.png")
    size = g.planet.get_size()
    g.planet_position = Vector2(350-size[0]/2, 350-size[1]/2)

go()