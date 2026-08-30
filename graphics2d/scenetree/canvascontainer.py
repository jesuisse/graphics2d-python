from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.notification import Notification
from graphics2d.scenetree.canvasitem import CanvasItem, CanvasRectAreaItem
from graphics2d.events import is_pointer_event, get_event_location, is_focus_event
from pygame.math import Vector2
import pygame.locals as const
from pygame import Rect, Surface
import graphics2d.constants as G2D

class CanvasContainer(CanvasRectAreaItem):
    """
    CanvasContainers change the way the frameworks deals with drawing and events.

    When you add a CanvasItem to the scene tree, the framework takes care of sending it mouse input,
    keyboard input, resize events and run it's on_draw callback in the right order. The position of
    your CanvasItem is relative to the first CanvasItem ancestor in the tree.

    If you add your CanvasItem to a CanvasContainer, however, the container will take care of
    distributing pointer input, positioning, sizing and drawing your CanvasItem. In effect, a CanvasContainer
    is fully responsible for whatever happens in it's own screen space. The framework will NOT handle
    any of it, EXCEPT to send GUI keyboard input to your CanvasItem directly if it has focus.
    """

    # signal resized(item: CanvasContainer, new_width, new_height)
    resized = Notification("resized", "new_width", "new_height")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # stores the item that currently contains the mouse
        self.item_containing_mouse = None


    def on_ready(self):
        self.layout()
        self.request_redraw()

    def on_resized(self, new_width, new_height):
        # This will set our size
        super().on_resized(new_width, new_height)
        self.layout()
        self.request_redraw()
        self.emit(CanvasContainer.resized, new_width, new_height)
    
    def on_entered(self):
        self.layout()
        self.request_redraw()

    def on_child_entered(self, node):
        self.layout()
        self.request_redraw()

    def on_draw(self, draw_surface):
        for child in self.children:
            self._draw_child(child, draw_surface, draw_surface.get_size())
            

    def _draw_child(self, child: SceneItem, draw_surface: Surface, size: tuple):
        if not isinstance(child, CanvasItem):
            return        
        if isinstance(child, CanvasRectAreaItem):
            if child.position[0] > self.size[0] or child.position[1] > self.size[1] or child.position[0] + child.size[0] < 0 or child.position[1] + child.size[1] < 0:
                # don't bother drawing as the child is outside the visible area
                return
            # TODO: Figure out why self.size can be larger than draw_surface.size (which leads to an exception if
            # we use the commented out clip_size calculation)
            #clip_size = (max(0, min(child.size[0], self.size.x-child.position.x)), max(0, min(child.size[1], self.size.y-child.position.y)))            
            clip_size = (min(child.size[0],size[0]-child.position.x), min(child.size[1], size[1]-child.position.y))
        else:
            clip_size = (size[0] - child.position.x, size[1] - child.position.y)
        if clip_size[0] <= 0 or clip_size[1] <= 0:
            # do not draw children who's visible area is zero
            return        
        # This is ugly, but allows CanvasItems to draw without having their own surface AND makes
        # the CanvasItem drawing API cleaner (no need to pass in a surface)            
        r = Rect(child.position, clip_size)
        subsurface = draw_surface.subsurface(r)
        child._draw_surface = subsurface
        child.on_draw(subsurface)
        child._draw_surface = None


    def layout(self):
        """
        Lays the children out, e.g. determines their size and position
        in the container.
        """
        pass


    def notify_children_resized(self):
        """
        Notifies children that they have been resized via the on_resized callback.
        Note that their size has already been set when they receive this notificaton,
        but it is not guaranteed that they have been positioned yet.

        If you write your own container, call this once you have sized all the children
        in layout().
        """
        for child in self.children:
            if isinstance(child, CanvasRectAreaItem):
                child.on_resized(child.size[0], child.size[1])

    def get_content_min_size(self):
        """
        Returns the minimum size of the container's content (e.g. it's children)
        """
        return (0, 0)

    def get_min_size(self):
        """
        Calculates the minimum size of the Container
        """
        content_size = self.get_content_min_size()
        return (max(self.min_size[0], content_size[0]), max(self.min_size[1], content_size[1]))


    def on_gui_input(self, event):
        """
        CanvasContainers receive input events via the special callback gui_input *if* the 
        on_input mechanism hasn't consumed the event. The container then treates input
        according to type; mouse and touch events are sent only to CanvasRectAreaItem children
        that contain the pointer. 
        """        
        if is_pointer_event(event):            
            pos = get_event_location(event)            
            if pos:
                has_mouse = None
                for child in self.children:
                    viewport_pos = child.get_viewport_position()
                    r = Rect(viewport_pos, child.get_bbox().size)
                    if isinstance(child, CanvasRectAreaItem) and r.collidepoint(pos):
                        has_mouse = child
                        child.on_gui_input(event)
                        break
                if self.item_containing_mouse != has_mouse:
                    if self.item_containing_mouse:
                        self.item_containing_mouse.on_mouse_leave()
                    self.item_containing_mouse = has_mouse
                    if has_mouse:
                        has_mouse.on_mouse_enter(event)
                        
            else:
                # we get here for MOUSEWHEEL events. What do we do with them?
                pass
        
        elif is_focus_event(event):
            # keyboard events are sent to the focused CanvasItem by the framework. So this
            # code is usually not executed. 
            pass
            #print("DEADEND - focus event at the wrong destination")
        else:
            print(self.name, "received but won't handle", event)

    def child_requests_redraw(self, child):        
        # We do not propagate child redraw requests up the tree, as we are responsible
        # for handling their redrawing. We simply ask to be redrawn ourselves and will 
        # then redraw (currently) all the children.
        self.request_redraw()


class FreeLayoutContainer(CanvasContainer):
    """
    This Container does *not* layout its children. Instead, they keep full
    control over where they position themselves.

    This is used as the scene tree root by default. 
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'bgcolor' in kwargs:
            self.bgcolor = kwargs['bgcolor']
        else:
            self.bgcolor = None
    
    def on_draw(self, surface):        
        if self.bgcolor:
            surface.fill(self.bgcolor)
        super().on_draw(surface)


class BoxContainer(CanvasContainer):

    HORIZONTAL = 0
    VERTICAL = 1

    START = 1
    CENTERED = 2
    END = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = G2D.HORIZONTAL
        self.separation = 0
        if 'orientation' in kwargs:
            self.orientation = kwargs['orientation']
        if 'separation' in kwargs:
            self.separation = kwargs['separation']

    def get_content_min_size(self):
        """
        Calculates the minimum size of the content
        """
        min_primary_total = 0
        max_secondary = 0
        visible = 0
        for child in self.children:
            if not isinstance(child, CanvasRectAreaItem):
                continue
            visible += 1
            csize = child.get_min_size()
            min_primary_total += csize[self.orientation]
            max_secondary = max(max_secondary, csize[1-self.orientation])
        size = [0, 0]
        size[self.orientation] = min_primary_total + self.separation * (visible-1)
        size[1-self.orientation] = max_secondary
        return tuple(size)


    def layout(self):
        """
        Layouting the box container is fairly complicated because children act differently depending on whether
        they are constrained by a maximum size or not.
        """
        if self.size[0] == 0 and self.size[1] == 0:
            return
        min_total = max_total = weights = unconstrained_weights = visible_count = 0
        unconstrained = []
        orientation = self.orientation
        flagshift = (G2D.H_LAYOUT, G2D.V_LAYOUT)[orientation]

        min_sizes = [None] * len(self.children)
        max_sizes = [None] * len(self.children)
        calc_sizes = [None] * len(self.children)

        # pass 1: determine minimum size the children will take up
        for i, child in enumerate(self.children):
            if not isinstance(child, CanvasRectAreaItem):
                continue
            visible_count += 1
            min_sizes[i] = child.get_min_size()
            max_sizes[i] = child.get_max_size()
            calc_sizes[i] = [0, 0]
            min_total += min_sizes[i][orientation]
            maxsize = max_sizes[i][orientation]
            weight = child.get_weight_ratio()
            if child.flags & G2D.EXPAND << flagshift:
                unconstrained.append(i)
                unconstrained_weights += weight
            elif maxsize is not None:
                max_total += maxsize            
            weights += weight

        # now figure out how much leftover space we have
        # TODO: This looks wrong. Shouldn't we subtract the total of the minimum sizes?
        leftover = self.size[orientation]
        if not unconstrained and leftover - max_total - (self.separation)*(visible_count-1) > 0:
            # all children are maxed out and we have space availabe. Calc separator
            if visible_count == 1:
                separation_gap = leftover - max_total
            else:
                separation_gap = (leftover - max_total) / (visible_count-1)
        else:
            separation_gap = self.separation

        # pass 2: calculate the sizes of all the children who are maximum-constrained
        leftover -= separation_gap * (visible_count-1)
        i = -1
        for child in self.children:
            if not isinstance(child, CanvasRectAreaItem):
                continue

            i += 1
            cweight = child.get_weight_ratio()
            cmin = min_sizes[i]
            cmax = max_sizes[i]

            max_available = leftover / weights * cweight
            if child.flags & G2D.EXPAND << flagshift:  # cmax[orientation] is None
                # max-unconstrained children are calculated after the constrained ones
                # because we can't know how much space will be left to distribute among
                # themselves until we've handled all the max-constrained children.
                continue

            if child.flags & G2D.SHRINK << flagshift:
                # children with the SHRINK flag take up their minimum space 
                # TODO: What if there isn't enough space available?
                primary_size = int(cmin[orientation])
            elif cmax[orientation]:
                primary_size = int(max(cmin[orientation], min(max_available, cmax[orientation])))
            else:
                primary_size = int(max(cmin[orientation], max_available))
            weights -= cweight
            leftover -= primary_size

            calc_sizes[i][orientation] = primary_size
            calc_sizes[i][1-orientation] = min_sizes[i][1-orientation]

        # distribute leftover space among the maximum-unconstrained children we skipped in the last loop
        for i in unconstrained:
            cweight = self.children[i].get_weight_ratio()
            primary_size = int(max(min_sizes[i][orientation], leftover / unconstrained_weights * cweight))
            unconstrained_weights -= cweight
            leftover -= primary_size
            calc_sizes[i][orientation] = primary_size
            calc_sizes[i][1-orientation] = min_sizes[i][1-orientation]

        # pass 3 - determine position of each child and notify them of their new size
        pos = 0
        for i, child in enumerate(self.children):
            if not isinstance(child, CanvasRectAreaItem):
                continue
            child.position[orientation] = pos
            pos += calc_sizes[i][orientation] + separation_gap

            calc_sizes[i][1-orientation] = self._layout_along_secondary_axis(child, min_sizes[i][1-orientation], max_sizes[i][1-orientation])
            # notify child that it has a new size.
            child.on_resized(calc_sizes[i][0], calc_sizes[i][1])
            # might not work because we're not in the tree yet, possibly...
            if self.get_tree():
                child.request_redraw()

        

    def _layout_along_secondary_axis(self, child, minsize, maxsize):
        orientation = self.orientation
        flagshift = (G2D.V_LAYOUT, G2D.H_LAYOUT)[orientation]
       
        if child.flags & G2D.EXPAND << flagshift:
            # child has unconstrained maximum, so we enlarge it to our own
            # size
            secondary_size = self.size[1-orientation]
        elif maxsize is not None and not (child.flags & G2D.SHRINK << flagshift):
            # otherwise, if we have a valid maximum we set the size to that
            secondary_size = min(self.size[1-orientation], maxsize)
        else:
            # otherwise, we use the child's minimum size
            secondary_size = minsize

        if minsize < self.size[1-orientation] and not child.flags & G2D.FILL << flagshift:
            # default is ALIGN_START
            child.position[1-orientation] = 0
            if child.flags & G2D.ALIGN_CENTERED << flagshift:
                child.position[1-orientation] = (self.size[1-orientation] - secondary_size) / 2.0
            elif child.flags & G2D.ALIGN_END << flagshift:
                child.position[1-orientation] = self.size[1-orientation] - secondary_size        
        else:
            self.position[1-orientation] = 0
            secondary_size = self.size[1-orientation]
        return secondary_size


class VBoxContainer(BoxContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = G2D.VERTICAL

class HBoxContainer(BoxContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = G2D.HORIZONTAL

class PanelContainer(CanvasContainer):
    """
    PanelContainer contains a single child. It provides the child with a margin, border and background.
    If you add multiple children to the PanelContainer, only the first CanvasRectAreaItem is drawn.

    The margin separates this item from its parent; it is immediately followed by the border, and
    the content CanvasItem is placed *inside* the border, on top of the given background. The background
    does not fill the margins.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # left, right, top, bottom
        self.borders = (0, 0, 0, 0)
        self.margins = (0, 0, 0, 0)
        self.bg_color = None

        if 'margins' in kwargs:
            self.margins = self._interpret_size_parameter(kwargs['margins'])
        if 'borders' in kwargs:
            self.borders = self._interpret_size_parameter(kwargs['borders'])
        if 'bg_color' in kwargs:
            self.bg_color = kwargs['bg_color']

    def _interpret_size_parameter(self, seq):
        if type(seq) is list or type(seq) is tuple:
            if len(seq) == 4:
                return tuple(seq)
            elif len(seq) == 2:
                return tuple([seq[0], seq[0], seq[1], seq[1]])
        elif type(seq) is float or type(seq) is int:
            return tuple([seq, seq, seq, seq])
        else:
            raise ValueError("expected either a single number for all 4 sides, a sequence of (left, right, top, bottom) or (left/right, top/bottom) sizes")

    
    def _find_child(self) -> CanvasRectAreaItem:
        i = 0
        child = None
        # Find first usable child. We don't layout any other children even if there are more.
        while i < len(self.children) and not isinstance(child, CanvasRectAreaItem):
            child = self.children[i]
            i += 1        
        return child
        

    def get_content_min_size(self):        
        child = self._find_child()

        min_width = self.margins[0] + self.margins[1] + self.borders[0] + self.borders[1]
        min_height = self.margins[2] + self.margins[3] + self.borders[2] + self.borders[3]

        if child:
            ms = child.get_min_size()
            return tuple([ms[0]+min_width, ms[1]+min_height])
        else:
            return tuple([min_width, min_height])


    def layout(self):
        child = self._find_child()
        if child is None:
            return

        child.position[0] = self.margins[0] + self.borders[0]
        child.position[1] = self.margins[2] + self.borders[2]

        min_width = self.margins[0] + self.margins[1] + self.borders[0] + self.borders[1]
        min_height = self.margins[2] + self.margins[3] + self.borders[2] + self.borders[3]

        width = self.size[0] - min_width
        height = self.size[1] - min_height

        min_size = self.get_content_min_size()
        max_size = child.get_max_size()

        width = max(min_size[0], min(width, max_size[0]) if max_size[0] is not None else width)
        height = max(min_size[1], min(height, max_size[1]) if max_size[0] is not None else height)

        child.on_resized(width, height)


    def on_draw(self, draw_surface):
        # draw background
        w = self.size[0] - self.margins[0] - self.margins[1]
        h = self.size[1] - self.margins[2] - self.margins[3]
        if self.bg_color:
            self.draw_filled_rect(Rect(self.margins[0], self.margins[2], w, h), self.bg_color)

        child = self._find_child()
        if not child:
            return

        ssize = draw_surface.get_size()
        ssize = [ssize[0] - self.margins[1] - self.borders[1], 
                 ssize[1] - self.margins[3] - self.borders[3]]
        self._draw_child(child, draw_surface, ssize)

        

