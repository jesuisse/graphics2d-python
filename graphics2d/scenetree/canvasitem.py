from graphics2d.scenetree.sceneitem import SceneItem
from pygame.math import Vector2

class CanvasItem(SceneItem):
    """
    CanvasItem is an abstract base class for all items living in the scene tree that have a visual appearance.
    """

    def __init__(self, **kwargs):
        super().__init__()
        
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "CanvasItem-" + str(id)
        
        if 'position' in kwargs:
            self.position = kwargs['position']
        else:
            self.position = Vector2(0, 0)
            
    def request_redraw():
        """
        Call this to notify the SceneTree that this SceneItem needs to redraw itself.
        """
        self.get_tree().request_redraw(self)
        

    def on_ready():
        pass

    def on_draw(draw_surface):
        """
        Callback to draw itself
        
        draw_surface: The surface do draw this object on.
        """
        pass

    def on_update(dt):
        """
        Callback to update the state of this item. dt gives the number of milliseconds which have passed since
        the last frame (or thereabouts)
        """
        pass

    def on_input(event):
        """
        Callback to handle events. 
        """
        pass


