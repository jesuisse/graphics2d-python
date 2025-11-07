from graphics2d import *
from graphics2d.scenetree.canvasitem import CanvasRectAreaItem
import graphics2d.drawing as _draw


class Label(CanvasRectAreaItem):
    """ 
    Displays text
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'text' in kwargs:
            self.text = kwargs['text']
        else:
            self.text = "placeholder"
    
        if "font" in kwargs:
            self.font = kwargs['font']
        else:
            self.font = get_font(get_default_fontname())

        self.size = _draw.get_text_size(self.font, self.text)

        if "color" in kwargs:
            self.color = kwargs['color']
        else:
            self.color =  Color(120, 120, 120)

        self.size = _draw.get_text_size(self.font, self.text)
        
        if not "min_size" in kwargs:
            self.min_size = Vector2(self.size)
        if not "max_size" in kwargs:
            self.max_size = Vector2(self.size)


    def on_draw(self, surface):
        pos = Vector2(0, 0)
        rendered_text = _draw.draw_text(self.font, self.text, self.color, antialias=True)
        surface.blit(rendered_text, pos)
    
    def set_text(self, text):
        self.text = text        
        self.size = _draw.get_text_size(self.font, self.text)
        self.min_size = (self.size[0], self.size[1])

        self.request_redraw()
