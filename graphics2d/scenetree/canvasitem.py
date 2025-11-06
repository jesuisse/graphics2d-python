from graphics2d.scenetree.sceneitem import SceneItem
from pygame.math import Vector2
from pygame import Color, Rect
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
       
        if 'position' in kwargs:
            self.position = kwargs['position']
        else:
            self.position = Vector2(0, 0)

        # This will be set by the framework from the outside when calling the on_draw callback!!!
        self._draw_surface = None

    def request_redraw(self):
        """
        Call this to notify the SceneTree that this CanvasItem needs to redraw itself.
        
        If this item has a CanvasItem parent, the redraw request is forwarded to the parent.
        Otherwise, the tree is notified directly.
        """
        parent = self.get_parent()
        if isinstance(parent, CanvasItem):
            parent.child_requests_redraw(self)
        else:
            tree = self.get_tree()
            if tree:
                tree.request_redraw(self)


    def child_requests_redraw(self, child):
        """
        Called by a child CanvasItem to notify this item that the child needs to redraw itself.
        By default, the request is forwarded up the tree (without adding ourselves to the 
        redraw list).
        """
        parent = self.get_parent()
        if isinstance(parent, CanvasItem):
            parent.child_requests_redraw(child)
        else:
            tree = self.get_tree()
            if tree:
                tree.request_redraw(child)
        

    def get_viewport_position(self):
        """
        Returns the position of this item relative to the top left corner of the viewport.
        """
        return self._get_viewport_position(self)

    def _get_viewport_position(self, node):
        parent = node.parent() if node.parent else None
        if isinstance(node, CanvasItem):
            pos = node.position
        else:
            pos = Vector2(0, 0)
        if parent:
            return pos + self._get_viewport_position(parent)
        else:
            return pos
    
 

    def on_ready(self):
        pass

    def on_draw(self, draw_surface):
        """
        Callback to draw itself

        draw_surface: The surface do draw this object on.
        """
        pass
    
    def on_input(self, event):
        """
        Callback to handle events.
        """
        pass

    def on_unhandled_input(self, event):
        """
        Callback to handle events that haven't been marked as handled.
        This runs *after* all items in the scene tree capable of handling
        the event have had their on_input called.
        """
        pass

    def on_resized(self, new_width, new_height):
        """
        Callback when the item is resized. You shoul react to this if
        the visual representation of this item depends on its size.
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

    ALIGN_START = 1
    ALIGN_CENTERED = 2
    ALIGN_END = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Vector2(0, 0)
        self.min_size = (0, 0)
        self.max_size = (None, None)
        self.flags = 0
        self.weight_ratio = 1.0
        if 'size' in kwargs:
            size = kwargs['size']
            if isinstance(size, Vector2):
                self.size = size
            else:
                self.size = Vector2(size)
        if 'min_size' in kwargs:
            size = kwargs['min_size']
            if isinstance(size, Vector2):
                self.min_size = (size.x, size.y)
            else:
                self.min_size = (size[0], size[1])
        if 'max_size' in kwargs:
            size = kwargs['max_size']
            if isinstance(size, Vector2):
                self.max_size = (size.x, size.y)
            else:
                self.max_size = (size[0], size[1])
        if 'weight_ratio' in kwargs:
            self.weight_ratio = kwargs['weight_ratio']
        if 'flags' in kwargs:
            self.flags = kwargs['flags']

    def get_weight_ratio(self):
        return self.weight_ratio

    def get_min_size(self):
        return self.min_size

    def get_max_size(self):
        return self.max_size

    def get_bbox(self):
        return Rect(self.position, self.size)

    def on_resized(self, new_width, new_height):
        self.size[0] = new_width
        self.size[1] = new_height

    def on_gui_input(self, event):
        """
        CanvasRectAreas have a GUI input callback, which is only triggered when the 
        event has originated in this item's space (for pointer events), or if this
        item is focused (for key events)
        """
        pass


class CanvasColorRect(CanvasRectAreaItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'color' in kwargs:
            self.color = kwargs['color']
        else:
            self.color = Color(255, 0, 255)

    def on_draw(self, draw_surface):
        draw_surface.fill(self.color)
