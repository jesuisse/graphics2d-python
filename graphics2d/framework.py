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
    'set_window_title', 'get_window_surface', 'get_scenetree', 'VarContainer', 'CanvasItem', 'CanvasRectAreaItem'
    ]

import inspect
import pygame as _pygame
from pygame.math import Vector2
import datetime
import os.path
from graphics2d.scenetree import SceneTree, SceneItem, CanvasItem, CanvasRectAreaItem


class VarContainer:
    """
    This serves as a container for quasi-global variables.
    """
    pass

def empty_func(*args):
    pass

# callback functions which will be called if defined in the importing python module
hooks = {
    'on_draw': empty_func,
    'on_update': empty_func,
    'on_input': empty_func,
    'on_ready': empty_func,
    'on_exit': empty_func,
    'on_resized': empty_func
}

_calling_module = None
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
auto_redraw = True
is_fullscreen=False
is_resizable=False

_dirty_screen_rects = []

def _init():
    global clock, scene_tree
    _pygame.init()
    icon = _pygame.image.load(os.path.join(_get_internal_asset_path(), "icon.png"))
    if not _icon_already_set:
        _pygame.display.set_icon(icon)
    _honor_display_mode_settings()
    if not _icon_already_set:
        _pygame.display.set_icon(icon)
    clock = _pygame.time.Clock()
    scene_tree = SceneTree()

def _get_internal_asset_path():
    return os.path.join(os.path.dirname(__file__), "assets")

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
                # set window size 'constants' to behave as students expect
                # (tested; keeping these at the original values confuses people)
                if _calling_module:
                    setattr(_calling_module, 'WIDTH', event.w)
                    setattr(_calling_module, 'HEIGHT', event.h)
                hooks['on_resized'](event.w, event.h)
                _handle_scenetree_resize(event.w, event.h)
                scene_tree.request_redraw_all(scene_tree.root)
                request_redraw()
            elif scene_tree.has_active_modal():
                modal = scene_tree.get_active_modal_node()
                modal.on_input(event)
            else:
                _handle_scenetree_input(event)
                hooks['on_input'](event)

        now = datetime.datetime.now()
        dt = now-last
        last = now
        msecs = dt.seconds * 1000 + (dt.microseconds / 1000)
        hooks['on_update'](msecs)
        _handle_scenetree_updates(msecs)
        drawn = False
        if needs_redraw or settings['ALWAYS_REDRAW']:
            drawn = True
            hooks['on_draw']()
        if scene_tree.has_redraw_requests():
            drawn = True
            _handle_scenetree_drawing()
        if drawn:
            _pygame.display.flip()
            needs_redraw = False
        clock.tick(settings['MAX_FPS'])

def _handle_scenetree_input(event):
    # TODO: Figure out how to mark an event as handled so we stop propagating it
    for item in scene_tree.depthfirst_postorder():
        # should we only do this for CanvasItems?
        item.on_input(event)

def _handle_scenetree_updates(dt):
    for item in scene_tree.depthfirst_postorder():
        # Should we only do this for CanvasItems?
        item.on_update(dt)

def _handle_scenetree_resize(new_width, new_height):
    root = scene_tree.root
    if root:
        # Should we only do this for CanvasItems?
        root.on_resized(new_width, new_height)

def _handle_scenetree_drawing():
    size = Vector2(screen.get_size())

    for item in scene_tree.depthfirst_preorder():
        p = item.get_viewport_position()
        if not isinstance(item, CanvasItem) or (not settings['ALWAYS_REDRAW'] and item not in scene_tree.redraw_requests):
            # either an item with no visual represenatation or no redraw request for this item
            continue
        elif isinstance(item, CanvasRectAreaItem):
            if p[0] > size[0] or p[1] > size[1] or p[0] + item.size[0] < 0 or p[1] + item.size[1] < 0:
                # don't bother drawing as the item is outside the visible area
                continue
            clip_size = (max(0, min(item.size[0], size.x-p.x)), max(0, min(item.size[1], size.y-p.y)))
        else:
            clip_size = (max(0, size.x - p.x), max(0, size.y - p.y))
        r = _pygame.Rect(p, clip_size)

        r = calc_viewport_clip_rect(item)
        if r.w <= 0 or r.h <= 0:
            continue

        # This is ugly, but allows CanvasItems to draw without having their own surface AND makes
        # the CanvasItem drawing API cleaner (no need to pass in a surface)
        print(item.name, r)
        subsurface = screen.subsurface(r)
        item._draw_surface = subsurface
        item.on_draw(subsurface)
        item._draw_surface = None
    scene_tree.clear_redraw_requests()

def calc_viewport_clip_rect(item):
    size = screen.get_size()
    parent = item.get_parent()
    pos = item.get_viewport_position()
    if isinstance(parent, CanvasRectAreaItem):
        clipw = min(parent.size[0]-item.position.x, item.size[0])
        cliph = min(parent.size[1]-item.position.y, item.size[1])
        clipw = max(0, min(clipw, size[0]-pos.x))
        cliph = max(0, min(cliph, size[1]-pos.y))
        return _pygame.Rect(pos.x, pos.y, clipw, cliph)
    elif isinstance(item, CanvasRectAreaItem):
        clipw = max(0, min(size[0]-pos.x, item.size[0]))
        cliph = max(0, min(size[1]-pos.y, item.size[1]))
        return _pygame.Rect(pos.x, pos.y, clipw, cliph)
    else:
        return _pygame.Rect(pos.x, pos.y, size[0]-pos.x, size[1]-pos.y)


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

def get_window_surface():
    """
    Returns the surface this window draws its content onto
    """
    return screen

def get_runtime_in_msecs():
    """
    Returns the number of msecs this application has been running
    """
    return _pygame.time.get_ticks()

def get_scenetree():
    return scene_tree

def go():
    """
    Configures pygame and starts the event loop
    """
    global _calling_module
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    _calling_module = mod
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
        hooks['on_ready']()
        _event_loop()
        hooks['on_exit']()
    finally:
        # make sure we quit pygame. If we don't because an exception bypasses this,
        # some systems may freeze until they notice we're dead.
        _pygame.quit()


