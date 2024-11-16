"""
Simplified 2D Graphics interface for teaching  (c) 2024 by Pascal Schuppli

This is comparable to pygame zero, but provides access to more of pygame (especially surfaces) and
a scene tree which can be used to work with graphical objects, some of which are provided to facilitate
layouting and GUI coding.

This enables students to write minimal valid graphical programs like this:

from graphics2d import *

WIDTH = HEIGHT = 500

def draw():
    draw_circle((250, 250), 100, RED)

go()
"""

__all__ = [
    'go', 'request_redraw', 'get_runtime_in_msecs', 'get_window_size', 'get_window_width', 'get_window_height',
    'set_window_title', 'VarContainer'
    ]

import inspect
import pygame as _pygame
from pygame.math import Vector2
import datetime
from graphics2d.scenetree import SceneTree, SceneItem, CanvasItem

class VarContainer:
    """
    This serves as a container for quasi-global variables.
    """
    pass

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

_icon_already_set = False

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
# This leads to draw() callback being called every frame. If you turn this off 
# you'll need to call request_redraw() to have the event loop call draw().
auto_redraw = True

is_fullscreen=False
is_resizable=False

_dirty_screen_rects = []


def _init():
    global clock, scene_tree
    _pygame.init()
    icon = _pygame.image.load("resources/icon.png")
    if not _icon_already_set:
        _pygame.display.set_icon(icon)
    _honor_display_mode_settings()
    clock = _pygame.time.Clock()
    scene_tree = SceneTree()
     
def _get_display_flags():
    flags = 0
    if settings['RESIZABLE']:
        flags += _pygame.RESIZABLE
    if settings['FULLSCREEN']:
        flags += _pygame.FULLSCREEN        
    return flags    

def _honor_display_mode_settings(): 
    global is_fullscreen, is_resizable, screen
    width = settings['WIDTH']
    height = settings['HEIGHT']
    if settings['FULLSCREEN']:
        width = 0
        height = 0
    screen = _pygame.display.set_mode((width, height), _get_display_flags())    
    is_fullscreen = settings['FULLSCREEN']
    is_resizable = settings['RESIZABLE']
    request_redraw()


def _event_loop():
    global needs_redraw
    running = True
    last = datetime.datetime.now()    
    while running:        
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                running = False
            elif event.type == _pygame.VIDEORESIZE:
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
            _pygame.display.flip()
            needs_redraw = False
        clock.tick(settings['MAX_FPS'])

def _handle_scenetree_input(event):
    # TODO: Figure out how to mark an event as handled so we stop propagating it
    for item in scene_tree.depthfirst_postorder():
        item.on_input(event)

def _handle_scenetree_updates(dt):
    for item in scene_tree.depthfirst_postorder():
        item.on_update(dt)

def _handle_scenetree_drawing():
    # TODO: Make sure we draw children before parents... ?
    
    size = Vector2(screen.get_size())
    for item in scene_tree.redraw_requests:
        # TODO: For items with a size, we should set that as the clip size so items
        # can't draw outside their reported size.
        clip_size = (size.x - item.position.x, size.y - item.position.y)
        r = Rect(item.position, clip_size)
        item.on_draw(screen.subsurface(r))
    scene_tree.clear_redraw_requests()
    

def request_redraw():
    """
    request a visual update. If AUTO_REDRAW is false, this must be called for changes to 
    become visible.
    """
    global needs_redraw
    needs_redraw = True

def set_window_title(title):
    _pygame.display.set_caption(title)
    
def set_window_icon(icon_surface):
    global _icon_already_set
    _icon_already_set = True
    _pygame.display.set_icon(icon_surface)

def get_window_size() -> Vector2:
    """
    Returns a Vector2 containing the size of the window
    """
    return Vector2(screen.get_size())

def get_window_width():
    """
    Returns the width of the window in pixels
    """
    return screen.get_width()

def get_window_height():
    """
    Returns the height of the window in pixels
    """
    return screen.get_height()

def get_runtime_in_msecs():
    """
    Returns the number of msecs this application has been running
    """
    return _pygame.time.get_ticks()

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
    _pygame.display.set_caption("Graphics 2D Window")
    _honor_display_mode_settings()    
    try:
        hooks['ready']()
        _event_loop()    
        hooks['exit']()
    finally:
        # make sure we quit pygame. If we don't because an exception bypasses this, 
        # some systems may freeze until they notice we're dead.
        _pygame.quit()

        
