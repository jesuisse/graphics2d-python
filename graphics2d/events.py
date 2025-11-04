import pygame
import pygame.locals as _const

_MOUSE_EVENTS = ['MOUSEMOTION', 'MOUSEBUTTONDOWN', 'MOUSEBUTTONUP']
_TOUCH_EVENTS = ['FINGERMOTION', 'FINGERDOWN', 'FINGERUP', 'MULTIGESTURE']
_FOCUS_EVENTS = ['KEYUP', 'KEYDOWN']

_pointer_events = []
_mouse_events = []
_touch_events = []
_touch_available = False

# Determine which pointer events are available
for _name in _MOUSE_EVENTS:
    if hasattr(_const, _name):
        _mouse_events.append(getattr(_const, _name))
        _pointer_events.append(getattr(_const, _name))
for _name in _TOUCH_EVENTS:
    if hasattr(_const, _name):
        _touch_available = True
        _pointer_events.append(getattr(_const, _name))
        _touch_events.append(getattr(_const, _name))

def is_pointer_event(event : pygame.event.Event):
    """
    Returns True if the given event is a pointer event
    (e.g. it has a position - this includes mouse and touch events)
    """
    return event.type in _pointer_events

def is_touch_event(event : pygame.event.Event):
    """
    Returns True if the given event is a touch event
    """
    return _touch_available and event in _touch_events

def is_focus_event(event : pygame.event.Event):
    """
    Returns True if the given event is an event that should
    be sent to the focused item in the scene tree.
    """
    return event in _FOCUS_EVENTS



def is_touch_supported() -> bool:
    """
    Returns True if touch events are supported
    (this doesn't mean that they can be produced on the current
    device, just that the framework is capable of handling them
    if a device generates them)
    """
    return _touch_available

def get_event_location(event: pygame.event.Event):
    """
    Returns the location of an event (or None if the event has no
    location information attached to it)
    """
    if is_touch_event(event):
        return (event.x, event.y)
    elif event.type in _mouse_events and event.type != _const.MOUSEWHEEL:
        return event.pos
    else:
        return None



