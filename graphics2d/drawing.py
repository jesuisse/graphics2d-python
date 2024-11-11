import pygame.draw as draw
import pygame.font 

font_cache = {}

def get_font(fontname, size=16):
    key = "{}-{}".format(fontname, size)
    if key not in font_cache:
        font = pygame.font.Font(fontname, size)
        font_cache[key] = font
    return font_cache[key]

def get_default_fontname():
    return pygame.font.get_default_font()

def draw_filled_rect(surface, rect, color):
    draw.rect(surface, color, rect)

def draw_rect(surface, rect, color, width=1):
    draw.rect(surface, color, rect, width)

def draw_text(font, text, color, antialias=True, background=None):
    return font.render(text, antialias, color, background)

