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

        if "color" in kwargs:
            self.color = kwargs['color']
        else:
            self.color =  Color(120, 120, 120)

        if "bgcolor" in kwargs:
            self.bgcolor = kwargs['bgcolor']
        else:
            self.bgcolor = Color(255, 0, 255)

        if "size" not in kwargs:
            self.size = list(self.get_content_min_size())
                
        if "min_size" not in kwargs:
            self.min_size = (None, None)
        if "max_size" not in kwargs:
            self.max_size = (None, None)

    @property 
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, new_text):
        self.__text = new_text        
        self.size = self.get_content_min_size()        
        self.request_redraw()
    
    def get_content_min_size(self):
        if hasattr(self, "font"):
            s = _draw.get_text_size(self.font, self.__text)
            return (s[0], s[1])

    def on_draw(self, surface):        
        pos = Vector2(0, 0)        
        rendered_text = _draw.draw_text(self.font, self.__text, self.color, antialias=True)
        h = rendered_text.get_height()        
        pos = Vector2(0, (self.size[1]-h)/2.0)
        surface.fill(self.bgcolor)
        surface.blit(rendered_text, pos)
    
