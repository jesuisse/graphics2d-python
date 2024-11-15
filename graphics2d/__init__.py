from graphics2d.simplified import go, request_redraw, draw_line, draw_polyline, draw_filled_polygon, draw_rect, draw_filled_rect, draw_circle, draw_filled_circle, draw_surface, draw_text, get_text_size, get_window_size, get_runtime_in_msecs, get_default_fontname, get_all_fontnames, load_image, save_screen, set_window_title
from pygame import Rect, Color
from pygame.math import Vector2, clamp, lerp
import pygame.locals as const

__imported = [
    'QUIT', 'ACTIVEEVENT', 'KEYDOWN', 'KEYUP', 'MOUSEMOTION', 'MOUSEBUTTONUP', 'MOUSEBUTTONDOWN',
    'JOYAXISMOTION', 'JOYBALLMOTION', 'JOYHATMOTION', 'JOYBUTTONUP', 'JOYBUTTONDOWN', 
    'VIDEORESIZE', 'VIDEOEXPOSE', 'USEREVENT'
    ]

# Import some constants into the local namespace
for name in __imported:
    globals()[name] = getattr(const, name)

# Provide a few default colors
BLACK = Color("black")
WHITE = Color("white")
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
MAGENTA = Color(255, 0, 255)
CYAN = Color(0, 255, 255)