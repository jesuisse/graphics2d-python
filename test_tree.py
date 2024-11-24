from graphics2d import *
from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.canvasitem import CanvasItem, CanvasColorRect
from graphics2d.scenetree.canvascontainer import BoxContainer

WIDTH = 700
HEIGHT = 700
RESIZABLE = True
ALWAYS_REDRAW = False


class CanvasTest(CanvasItem):

    def on_draw(self, draw_surface):
        size = get_window_size()
        draw_filled_rect((0,0), size, Color(30, 30, 30))
        draw_circle((size.x/2, size.y/2), 200, RED, 2)


def on_ready():
    tree = get_scenetree()
    #root = SceneItem(name="root")
    root = BoxContainer(name="root")
    root.size = Vector2(WIDTH, HEIGHT)
    #background = CanvasTest(name="background")
    red = CanvasColorRect(name="red_rect", color=RED,
        weight_ratio=2,
        min_size=(50, 50), max_size=(300, 200), flags=CanvasColorRect.ALIGN_END)
    blue = CanvasColorRect(name="blue_rect", color=BLUE,
        min_size=(20, 50))
    yellow = CanvasColorRect(name="yellow_rect", color=YELLOW,
        min_size=(20, 50), max_size=(200, 300), flags=CanvasColorRect.ALIGN_CENTERED)
    root.add_child(red)
    root.add_child(blue)
    root.add_child(yellow)
    tree.set_root(root)
    set_window_title("SceneTree Test")

go()