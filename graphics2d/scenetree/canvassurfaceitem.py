from graphics2d.scenetree.canvasitem import CanvasItem
from pygame.math import Vector2

class CanvasSurfaceItem(CanvasItem):
    """
    This is a canvas item which is backed by a pygame surface.
    """
       
    def __init__(self, **kwargs):
        super().__init__()
        self.surface = None
        self.size = Vector2(0, 0)
        
        if 'surface' in kwargs:
            self.surface = kwargs['surface']
            self.size = Vector2(self.surface.get_size())
    
    def on_draw(draw_surface):
        draw_surface.blit(self.surface, (0,0))
      
        