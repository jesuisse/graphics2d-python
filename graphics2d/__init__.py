from graphics2d.framework import *
from pygame import Rect, Color
from pygame.math import Vector2, clamp, lerp
import pygame.locals as const
from graphics2d.simplified import *

# pygame constants that are handy to have in the global namespace
__imported_consts = (
    'QUIT', 'ACTIVEEVENT', 'KEYDOWN', 'KEYUP', 'MOUSEMOTION', 'MOUSEBUTTONUP', 'MOUSEBUTTONDOWN',
    'JOYAXISMOTION', 'JOYBALLMOTION', 'JOYHATMOTION', 'JOYBUTTONUP', 'JOYBUTTONDOWN', 
    'VIDEORESIZE', 'VIDEOEXPOSE', 'USEREVENT'
    )

# Import some constants into the local namespace
for _name in __imported_consts:
    globals()[_name] = getattr(const, _name)


# Provide a few default colors
BLACK = Color("black")
WHITE = Color("white")
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
MAGENTA = Color(255, 0, 255)
CYAN = Color(0, 255, 255)