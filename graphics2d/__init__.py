from graphics2d.framework import go, VarContainer, request_redraw, set_window_title, get_window_size, get_runtime_in_msecs
from pygame import Rect, Color
from pygame.math import Vector2, clamp, lerp
import pygame.locals as const
import graphics2d.simplified

# This is the simplified drawping API
__imported_functions = (
    'draw_line', 'draw_polyline', 'draw_filled_polygon', 'draw_rect',
    'draw_filled_rect', 'draw_circle', 'draw_filled_circle', 'draw_surface',
    'draw_text', 'get_text_size', 
    'get_default_fontname', 'get_all_fontnames', 'load_image', 'save_screen'
    )

# Constants that are handy to have in the global namespace
__imported_consts = (
    'QUIT', 'ACTIVEEVENT', 'KEYDOWN', 'KEYUP', 'MOUSEMOTION', 'MOUSEBUTTONUP', 'MOUSEBUTTONDOWN',
    'JOYAXISMOTION', 'JOYBALLMOTION', 'JOYHATMOTION', 'JOYBUTTONUP', 'JOYBUTTONDOWN', 
    'VIDEORESIZE', 'VIDEOEXPOSE', 'USEREVENT'
    )

# Import simplified functions into the local namespace
for name in __imported_functions:
    globals()[name] = getattr(graphics2d.simplified, name)

# Import some constants into the local namespace
for name in __imported_consts:
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