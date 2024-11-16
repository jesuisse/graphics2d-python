"""
Simplified 2D Graphics interface for teaching  (c) 2024 by Pascal Schuppli

This is comparable to pygame zero, but provides access to more of pygame (especially surfaces) and
a scene tree which can be used to work with graphical objects, some of which are provided to facilitate
layouting and GUI coding.
"""

import pygame
import pygame.font
from pygame.math import Vector2
import graphics2d.drawing as draw
import graphics2d.framework as framework

__all__ = [
    'draw_line', 'draw_polyline', 'draw_filled_polygon', 'draw_rect',
    'draw_filled_rect', 'draw_circle', 'draw_filled_circle', 'draw_surface',
    'draw_text', 'get_text_size', 
    'get_default_fontname', 'get_all_fontnames', 'load_image', 'save_screen'
    ]

VALID_IMAGE_EXTENSIONS = ['.bmp', '.jpg', '.jpeg', '.gif', '.lbm', '.pbm', '.pgm', '.ppm', '.pcx', '.png', '.pnm', '.tga', '.tiff', '.webp', '.xpm']



def draw_line(start, end, color, width=1):
    """
    Draws a line from start (x1, y1) to end (x2, y2)
    """
    draw.draw_line(framework.screen, start, end, color, width)    

def draw_polyline(points, color, is_closed=False, width=1):
    """
    Draws a sequence of connected lines defined by an arbitrary number of points.
    If is_closed is True, a line will be drawn from the last to the first point to make a polygon shape.
    """
    draw.draw_polyline(framework.screen, points, color, is_closed, width)

def draw_filled_polygon(points, color):
    """
    Draws a polygon from a sequence of points.    
    """
    draw.draw_filled_polygon(framework.screen, points, color)

def draw_rect(topleft, size, color, width=1):
    """
    Draws a rectangle 
    """
    draw.draw_rect(framework.screen, pygame.Rect(topleft, size), color, width)

def draw_filled_rect(topleft, size, color):
    """
    Draws a filled rectangle 
    """
    draw.draw_filled_rect(framework.screen, pygame.Rect(topleft, size), color)

def draw_circle(center, radius, color, width=1):
    """
    Draws a circle at center position (x, y) with the given radius.
    """
    draw.draw_circle(framework.screen, center, radius, color, width)

def draw_filled_circle(center, radius, color):
    """
    Draws a filled circle at position (x, y) with the given radius.
    """
    draw.draw_filled_circle(framework.screen, center, radius, color)


def draw_text(fontname : str, fontsize : float, text : str, position, color, antialiased=True, background=None):
    """
    Draws text with a given font, size and color at a given coordinate
    """
    font = draw.get_font(fontname, fontsize)
    surface = draw.draw_text(font, text, color, antialiased, background)
    framework.screen.blit(surface, position)

def draw_surface(source_surface, destination_position, source_area=None):
    framework.screen.blit(source_surface, destination_position, source_area)


def get_text_size(fontname : str, fontsize : float, text : str) -> Vector2:
    font = draw.get_font(fontname, fontsize)
    return draw.get_text_size(font, text)

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
    pygame.image.save(framework.screen, filename)
