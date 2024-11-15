"""
Simplified 2D Graphics interface for teaching  (c) 2024 by Pascal Schuppli

This is comparable to pygame zero, but provides access to more of pygame (especially surfaces) and
a scene tree which can be used to work with graphical objects, some of which are provided to facilitate
layouting and GUI coding.
"""

import inspect
import pygame
import pygame.font
import datetime
import graphics2d.drawing as draw
from graphics2d.scenetree import SceneTree, SceneItem, CanvasItem

VALID_IMAGE_EXTENSIONS = ['.bmp', '.jpg', '.jpeg', '.gif', '.lbm', '.pbm', '.pgm', '.ppm', '.pcx', '.png', '.pnm', '.tga', '.tiff', '.webp', '.xpm']


def empty_func(*args):
    pass

# callback functions which will be called if defined in the importing python module
hooks = {
    'draw': empty_func,
    'update': empty_func,
    'input': empty_func,
    'ready': empty_func,
    'exit': empty_func,
    'resized': empty_func
}

# global constants which will be picked up from the importing python module and used to
# for initial configuration of the graphics.
settings = {
    'WIDTH' : 1280,
    'HEIGHT': 720,
    'ALWAYS_REDRAW': True,
    'MAX_FPS': 60,
    'FULLSCREEN': False,
    'RESIZABLE': False,
    'DEFAULT_FONT_SIZE': 24
}

scene_tree = None

screen = None
clock = None
needs_redraw = True
# This leads to draw() callback being called every frame. If you turn this off via disable_auto_redraw(), you'll need to call
# request_redraw() to have the event loop call draw().
auto_redraw = True

is_fullscreen=False
is_resizable=False

_dirty_screen_rects = []


def _init():
    global clock, scene_tree
    pygame.init()    
    _honor_display_mode_settings()
    clock = pygame.time.Clock()
    scene_tree = SceneTree()
     
def _get_display_flags():
    flags = 0
    if settings['RESIZABLE']:
        flags += pygame.RESIZABLE
    if settings['FULLSCREEN']:
        flags += pygame.FULLSCREEN        
    return flags    

def _honor_display_mode_settings(): 
    global is_fullscreen, is_resizable, screen
    width = settings['WIDTH']
    height = settings['HEIGHT']
    if settings['FULLSCREEN']:
        width = 0
        height = 0
    screen = pygame.display.set_mode((width, height), _get_display_flags())    
    is_fullscreen = settings['FULLSCREEN']
    is_resizable = settings['RESIZABLE']
    request_redraw()


def _event_loop():
    global needs_redraw
    running = True
    last = datetime.datetime.now()    
    while running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                hooks['resized'](event.w, event.h)
                request_redraw()
            else:
                _handle_scenetree_input(event)
                hooks['input'](event)                
                
        now = datetime.datetime.now()
        dt = now-last
        last = now
        msecs = dt.seconds * 1000 + (dt.microseconds / 1000)
        hooks['update'](msecs)
        _handle_scenetree_updates(msecs)
        if needs_redraw or settings['ALWAYS_REDRAW'] or scene_tree.has_redraw_requests():
            hooks['draw']()
            _handle_scenetree_drawing()
            pygame.display.flip()
            needs_redraw = False
        clock.tick(settings['MAX_FPS'])

def _handle_scenetree_input(event):
    # TODO: Figure out how to mark an event as handled so we stop propagating it
    for item in scene_tree.depthfirst_postorder():
        item.input(event)

def _handle_scenetree_updates(dt):
    for item in scene_tree.depthfirst_postorder():
        item.update(dt)

def _handle_scenetree_drawing():
    # TODO: Make sure we draw children before parents... ?
    for item in scene_tree.redraw_requests:
        item.draw()
    scene_tree.clear_redraw_requests()
    

def request_redraw():
    """
    request a visual update. If AUTO_REDRAW is false, this must be called for changes to 
    become visible.
    """
    global needs_redraw
    needs_redraw = True


def draw_line(start, end, color, width=1):
    """
    Draws a line from start (x1, y1) to end (x2, y2)
    """
    draw.draw_line(screen, start, end, color, width)    

def draw_polyline(points, color, is_closed=False, width=1):
    """
    Draws a sequence of connected lines defined by an arbitrary number of points.
    If is_closed is True, a line will be drawn from the last to the first point to make a polygon shape.
    """
    draw.draw_polyline(screen, points, color, is_closed, width)

def draw_filled_polygon(points, color):
    """
    Draws a polygon from a sequence of points.    
    """
    draw.draw_filled_polygon(screen, points, color)

def draw_rect(topleft, size, color, width=1):
    """
    Draws a rectangle 
    """
    draw.draw_rect(screen, pygame.Rect(topleft, size), color, width)

def draw_filled_rect(topleft, size, color):
    """
    Draws a filled rectangle 
    """
    draw.draw_filled_rect(screen, pygame.Rect(topleft, size), color)

def draw_circle(center, radius, color, width=1):
    """
    Draws a circle at center position (x, y) with the given radius.
    """
    draw.draw_circle(screen, center, radius, color, width)

def draw_filled_circle(center, radius, color):
    """
    Draws a filled circle at position (x, y) with the given radius.
    """
    draw.draw_filled_circle(screen, center, radius, color)


def draw_text(fontname : str, fontsize : float, text : str, position, color, antialiased=True, background=None):
    """
    Draws text with a given font, size and color at a given coordinate
    """
    font = draw.get_font(fontname, fontsize)
    surface = draw.draw_text(font, text, color, antialiased, background)
    screen.blit(surface, position)

def draw_surface(source_surface, destination_position, source_area=None):
    screen.blit(source_surface, destination_position, source_area)


def get_text_size(fontname : str, fontsize : float, text : str):
    font = draw.get_font(fontname, fontsize)
    return draw.get_text_size(font, text)


def set_window_title(title):
    pygame.display.set_caption(title)

def get_window_size():
    """
    Returns a tuple (width, height) containing the size of the window
    """
    return screen.get_size()

def get_runtime_in_msecs():
    """
    Returns the number of msecs this application has been running
    """
    return pygame.time.get_ticks()


def get_default_fontname():
    """
    Returns the default font name as a string
    """
    return draw.get_default_fontname()

def get_all_fontnames():
    """
    Returns the names of all available fonts
    """
    return draw.get_fontnames() 

def load_image(filename):
    """
    Loads the image stored in the file with the given filename.

    Supports most image formats, such as jpg, png, webp, gif, bmp and so on. Simple svg files are supported as well.
    """
    try:
        if len(filename) < 4:
            raise ValueError("The filename you provided has no extension. Please provide a filename with an extension.")
        ext = filename[-4:].lower()
        if ext not in VALID_IMAGE_EXTENSIONS:
            raise ValueError("The filename you provided doesn't look like an image I can load. (Valid image extensions are {})".format(", ".join(VALID_IMAGE_EXTENSIONS)))
    except TypeError:
        raise ValueError("You must provide a valid string as a filename for load_image.")
    return pygame.image.load(filename)

def save_screen(filename):
    pygame.image.save(screen, filename)



def go():
    """
    Configures pygame and starts the event loop
    """
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    g = dir(mod)
    for name in hooks.keys():
        if name in g:
            hooks[name] = getattr(mod, name)
    for name in settings.keys():
        if name in g:
            settings[name] = getattr(mod, name)

    _init()
    pygame.display.set_caption("Graphics 2D Window")
    _honor_display_mode_settings()
    hooks['ready']()
    _event_loop()
    hooks['exit']()
    pygame.font.quit()
    pygame.quit()
    
        
