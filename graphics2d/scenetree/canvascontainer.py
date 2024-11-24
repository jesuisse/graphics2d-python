from graphics2d.scenetree.canvasitem import CanvasItem, CanvasRectAreaItem
from pygame.math import Vector2
from pygame import Rect


class CanvasContainer(CanvasRectAreaItem):
    """
    CanvasContainers change the way the frameworks deals with drawing and events.

    When you add a CanvasItem to the scene tree, the framework takes care of sending it mouse input,
    keyboard input, resize events and run it's on_draw callback in the right order. The position of
    your CanvasItem is relative to the first CanvasItem ancestor in the tree.

    If you add your CanvasItem to a CanvasContainer, however, the container will take care of
    distributing input, positioning, sizing and drawing your CanvasItem. In effect, a CanvasContainer
    is fully responsible for whatever happens in it's own screen space. The framework will NOT handle
    any of it, EXCEPT to send keyboard input to your CanvasItem directly if it has focus.
    """

    def on_ready(self):
        self.layout()
        self.request_redraw()

    def on_resized(self, new_width, new_height):
        # This will set our size
        super().on_resized(new_width, new_height)
        self.layout()
        self.request_redraw()

    def on_child_entered(self, node):
        print("Child {} entered tree".format(node.name))
        self.layout()
        self.request_redraw()

    def on_draw(self, draw_surface):
        return # TODO: REMOVE THIS!
        for child in self.children:
            if not isinstance(child, CanvasItem):
                continue
            if isinstance(child, CanvasRectAreaItem):
                if child.position[0] > self.size[0] or child.position[1] > self.size[1] or child.position[0] + child.size[0] < 0 or child.position[1] + child.size[1] < 0:
                    # don't bother drawing as the child is outside the visible area
                    continue
                clip_size = (max(0, min(child.size[0], self.size.x-child.position.x)), max(0, min(child.size[1], self.size.y-child.position.y)))
            else:
                clip_size = (max(0, self.size.x - child.position.x), max(0, self.size.y - child.position.y))
            r = Rect(child.position, clip_size)
            # This is ugly, but allows CanvasItems to draw without having their own surface AND makes
            # the CanvasItem drawing API cleaner (no need to pass in a surface)
            subsurface = draw_surface.subsurface(r)
            child._draw_surface = subsurface
            child.on_draw(subsurface)
            child._draw_surface = subsurface


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


class BoxContainer(CanvasContainer):

    HORIZONTAL = 0
    VERTICAL = 1

    START = 1
    CENTERED = 2
    END = 3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = self.HORIZONTAL
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
        for child in self.children:
            csize = child.get_min_size()
            min_primary_total += csize[self.orientation]
            max_secondary = max(max_secondary, csize[1-self.orientation])
        size = [0, 0]
        size[self.orientation] = min_primary_total
        size[1-self.orientation] = max_secondary
        return tuple(size)

    def layout(self):
        """
        Layouting the box container is fairly complicated because children act differently depending on whether
        they are constrained by a maximum size or not.
        """
        min_total = max_total = weights = unconstrained_weights = visible_count = 0
        unconstrained = []
        orientation = self.orientation

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
            if maxsize is None:
                unconstrained.append(i)
                unconstrained_weights += weight
            else:
                max_total += maxsize
            weights += weight

        # now figure out how much leftover space we have if all children are minimized
        leftover = self.size[orientation] #- min_total
        if not unconstrained and self.size[orientation] - max_total > 0:
            # all children are maxed out and we have space availabe. Calc separator
            separation_gap = (self.size[orientation] - max_total) / (visible_count-1)
        else:
            separation_gap = 0

        # pass 2: calculate the sizes of all the children who are maximum-constrained
        i = -1
        for child in self.children:
            if not isinstance(child, CanvasRectAreaItem):
                continue

            i += 1
            cweight = child.get_weight_ratio()
            cmin = min_sizes[i]
            cmax = max_sizes[i]

            max_available = leftover / weights * cweight
            if cmax[orientation] is None:
                # max-unconstrained children are calculated after the constrained ones
                # because we can't know how much space will be left to distribute among
                # themselves until we've handled all the max-constrained children.
                continue

            primary_size = int(max(cmin[orientation], min(max_available, cmax[orientation])))
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
            #child.size[orientation] = calc_sizes[i][orientation]
            child.position[orientation] = pos
            pos += calc_sizes[i][orientation] + separation_gap

            calc_sizes[i][1-orientation] = self._layout_along_secondary_axis(child, min_sizes[i][1-orientation], max_sizes[i][1-orientation])

            # notify child that it has a new size.
            child.on_resized(calc_sizes[i][0], calc_sizes[i][1])
            # might not work because we're not in the tree yet, possibly...
            #child.request_redraw()

            #print(child.name, child.position, child.size)


    def _layout_along_secondary_axis(self, child, minsize, maxsize):
        orientation = self.orientation
        if maxsize is None:
            # child has unconstrained maximum, so we enlarge it to our own
            # size
            secondary_size = self.size[1-orientation]
        else:
            # otherwise, we make it as big as it can get inside our borders
            secondary_size = min(self.size[1-orientation], maxsize)

        if minsize < self.size[1-orientation]:
            # default is ALIGN_START
            child.position[1-orientation] = 0
            if child.flags & child.ALIGN_CENTERED:
                child.position[1-orientation] = (self.size[1-orientation] - secondary_size) / 2.0
            elif child.flags & child.ALIGN_END:
                child.position[1-orientation] = self.size[1-orientation] - secondary_size
        else:
            self.position[1-orientation] = 0
            secondary_size = self.size[1-orientation]
        return secondary_size


class VBoxContainer(BoxContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = self.VERTICAL

class HBoxContainer(BoxContainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = self.HORIZONTAL



