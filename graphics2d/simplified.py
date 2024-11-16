"""
Simplified 2D Graphics interface for teaching  (c) 2024 by Pascal Schuppli

This provides drawing functions that wrap the drawing module and simplify it slightly by not requiring a
surface to draw onto; the framework's screen is used. Also, it contains code to check the validity of
the arguments provided and tries to give meaningful error messages if something is wrong.
"""

import pygame as _pygame
from pygame.math import Vector2
import graphics2d.drawing as _draw
import graphics2d.framework as _framework


_VALID_IMAGE_EXTENSIONS = ['.bmp', '.jpg', '.jpeg', '.gif', '.lbm', '.pbm', '.pgm', '.ppm', '.pcx', '.png', '.pnm', '.tga', '.tiff', '.webp', '.xpm']


def draw_line(start, end, color, width=1):
    """
    Draws a line from start (x1, y1) to end (x2, y2)
    """
    _draw.draw_line(_framework.screen, start, end, color, width)    

def draw_polyline(points, color, is_closed=False, width=1):
    """
    Draws a sequence of connected lines defined by an arbitrary number of points.
    If is_closed is True, a line will be drawn from the last to the first point to make a polygon shape.
    """
    _draw.draw_polyline(_framework.screen, points, color, is_closed, width)

def draw_filled_polygon(points, color):
    """
    Draws a polygon from a sequence of points.    
    """
    _draw.draw_filled_polygon(_framework.screen, points, color)

def draw_rect(topleft, size, color, width=1):
    """
    Draws a rectangle 
    """
    _draw.draw_rect(_framework.screen, _pygame.Rect(topleft, size), color, width)

def draw_filled_rect(topleft, size, color):
    """
    Draws a filled rectangle 
    """
    _draw.draw_filled_rect(_framework.screen, _pygame.Rect(topleft, size), color)

def draw_circle(center, radius, color, width=1):
    """
    Draws a circle at center position (x, y) with the given radius.
    """
    _draw.draw_circle(_framework.screen, center, radius, color, width)

def draw_filled_circle(center, radius, color):
    """
    Draws a filled circle at position (x, y) with the given radius.
    """
    _draw.draw_filled_circle(_framework.screen, center, radius, color)


def draw_text(fontname : str, fontsize : float, text : str, position, color, antialiased=True, background=None):
    """
    Draws text with a given font, size and color at a given coordinate
    """
    font = _draw.get_font(fontname, fontsize)
    surface = _draw.draw_text(font, text, color, antialiased, background)
    _framework.screen.blit(surface, position)

def draw_surface(source_surface, destination_position, source_area=None):
    _framework.screen.blit(source_surface, destination_position, source_area)


def get_text_size(fontname : str, fontsize : float, text : str) -> Vector2:
    font = _draw.get_font(fontname, fontsize)
    return _draw.get_text_size(font, text)

def get_default_fontname():
    """
    Returns the default font name as a string
    """
    return _draw.get_default_fontname()

def get_all_fontnames():
    """
    Returns the names of all available fonts
    """
    return _draw.get_fontnames() 

def load_image(filename):
    """
    Loads the image stored in the file with the given filename.

    Supports most image formats, such as jpg, png, webp, gif, bmp and so on. Simple svg files are supported as well.
    """
    try:
        if len(filename) < 4:
            raise ValueError("The filename you provided has no extension. Please provide a filename with an extension.")
        ext = filename[-4:].lower()
        if ext not in _VALID_IMAGE_EXTENSIONS:
            raise ValueError("The filename you provided doesn't look like an image I can load. (Valid image extensions are {})".format(", ".join(VALID_IMAGE_EXTENSIONS)))
    except TypeError:
        raise ValueError("You must provide a valid string as a filename for load_image.")
    return _pygame.image.load(filename)

def save_screen(filename):
    _pygame.image.save(framework.screen, filename)
