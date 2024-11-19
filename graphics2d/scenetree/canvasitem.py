from graphics2d.scenetree.sceneitem import SceneItem
from pygame.math import Vector2
import pygame.draw as draw

# Note on internal implementation of drawing: The framework will reach into each CanvasItem object and
# set the *private* _draw_surface* member before calling on_draw, and set it to None afterwards. So you
# can ONLY draw in on_draw. 

class CanvasItem(SceneItem):
    """
    CanvasItem is an abstract base class for all items living in the scene tree that have a visual appearance.    
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "CanvasItem-" + str(id)
        
        if 'position' in kwargs:
            self.position = kwargs['position']
        else:
            self.position = Vector2(0, 0)
        
        # This will be set by the framework from the outside when calling the on_draw callback!!!
        self._draw_surface = None
            
    def request_redraw():
        """
        Call this to notify the SceneTree that this SceneItem needs to redraw itself.
        """
        self.get_tree().request_redraw(self)
        

    def on_ready(self):
        pass

    def on_draw(self, draw_surface):
        """
        Callback to draw itself
        
        draw_surface: The surface do draw this object on.
        """
        pass

    def on_update(self, dt):
        """
        Callback to update the state of this item. dt gives the number of milliseconds which have passed since
        the last frame (or thereabouts)
        """
        pass

    def on_input(self, event):
        """
        Callback to handle events. 
        """
        pass


    def get_default_fontname():
        return pygame.font.get_default_font()

    def draw_line(self, start_pos, end_pos, color, width=1):
        draw.line(self._draw_surface, color, start_pos, end_pos, width)

    def draw_polyline(self, points, color, is_closed=False, width=1):
        draw.lines(self._draw_surface, color, is_closed, points, width)

    def draw_rect(self, rect, color, width=1):
        draw.rect(self._draw_surface, color, rect, width)

    def draw_filled_rect(self, rect, color):
        draw.rect(self._draw_surface, color, rect)

    def draw_filled_polygon(self, points, color):
        draw.polygon(self._draw_surface, color, points)

    def draw_circle(self, center, radius, color, width=1):
        draw.circle(self._draw_surface, color, center, radius, width)

    def draw_filled_circle(self, center, radius, color):
        draw.circle(self._draw_surface, color, center, radius)

    def draw_text(self, font, text, color, antialias=True, background=None):
        return font.render(text, antialias, color, background)

    def get_text_size(self, font, text) -> Vector2:
        return Vector2(font.size(text))


class CanvasRectAreaItem(CanvasItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Vector2(0, 0)
        if 'size' in kwargs:
            size = kwargs['size']
            if isinstance(size, Vector2):
                self.size = size
            else:
                self.size = Vector2(size)
