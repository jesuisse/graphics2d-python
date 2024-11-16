import pygame.draw as draw
import pygame.font
from pygame.math import Vector2

font_cache = {}

def get_font(fontname, size=16):
    key = "{}-{}".format(fontname, size)
    if key not in font_cache:
        font = pygame.font.Font(fontname, size)
        font_cache[key] = font
    return font_cache[key]

def get_fontnames():
    return pygame.font.get_fonts()

def get_default_fontname():
    return pygame.font.get_default_font()

def draw_line(surface, start_pos, end_pos, color, width=1):
    draw.line(surface, color, start_pos, end_pos, width)

def draw_polyline(surface, points, color, is_closed=False, width=1):
    draw.lines(surface, color, is_closed, points, width)

def draw_rect(surface, rect, color, width=1):
    draw.rect(surface, color, rect, width)

def draw_filled_rect(surface, rect, color):
    draw.rect(surface, color, rect)

def draw_filled_polygon(surface, points, color):
    draw.polygon(surface, color, points)

def draw_circle(surface, center, radius, color, width=1):
    draw.circle(surface, color, center, radius, width)

def draw_filled_circle(surface, center, radius, color):
    draw.circle(surface, color, center, radius)

def draw_text(font, text, color, antialias=True, background=None):
    return font.render(text, antialias, color, background)

def get_text_size(font, text) -> Vector2:
    return Vector2(font.size(text))


