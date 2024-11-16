from graphics2d import *
from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.canvasitem import CanvasItem

WIDTH = 700
HEIGHT = 700
RESIZABLE = True


class CanvasTest(CanvasItem):
    
    def on_draw(self, draw_surface):
        size = get_window_size()
        draw_filled_rect((0,0), size, Color(30, 30, 30))
        draw_circle((size.x/2, size.y/2), 200, RED, 2)


def on_ready():
    tree = get_scenetree()
    root = SceneItem(name="root")
    background = CanvasTest(name="background")
    root.add_child(background)    
    tree.set_root(root)    
    set_window_title("SceneTree Test")

go()