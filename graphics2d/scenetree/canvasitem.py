from graphics2d.scenetree.sceneitem import SceneItem

class CanvasItem(SceneItem):
    """
    CanvasItem is an abstract base class for all items living in the scene tree that have a visual appearance.
    """

    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = "CanvasItem-" + str(id)

    def request_redraw():
        """
        Call this to notify the SceneTree that this SceneItem needs to redraw itself.
        """
        self.get_tree().request_redraw(self)
        

    def ready():
        pass

    def draw():
        """
        Callback to draw itself
        """
        pass

    def update(dt):
        """
        Callback to update the state of this item. dt gives the number of milliseconds which have passed since
        the last frame (or thereabouts)
        """
        pass

    def input(event):
        """
        Callback to handle events. 
        """
        pass


