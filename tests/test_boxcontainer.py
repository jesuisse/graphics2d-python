import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graphics2d import *
from graphics2d.scenetree.sceneitem import SceneItem
from graphics2d.scenetree.canvasitem import CanvasItem, CanvasColorRect
from graphics2d.scenetree.canvascontainer import BoxContainer, PanelContainer
import graphics2d.constants as G2D

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

    root = PanelContainer(name="root", bg_color=MAGENTA)
    root.size = Vector2(WIDTH, HEIGHT)

    panel = PanelContainer(name="panel", bg_color=Color(30, 30, 30), margins=5, borders=0)

    box = BoxContainer(name="box", separation=5)

    red = CanvasColorRect(name="red_rect", color=RED,
        weight_ratio=2,
        min_size=(50, 50), max_size=(300, 200), flags=G2D.V_ALIGN_END)
    blue = CanvasColorRect(name="blue_rect", color=BLUE,
        min_size=(20, 50), flags=G2D.H_EXPAND+G2D.V_ALIGN_CENTERED)
    yellow = CanvasColorRect(name="yellow_rect", color=YELLOW,
        min_size=(20, 50), max_size=(200, 300), flags=G2D.V_ALIGN_CENTERED)

    panel.add_child(box)
    box.add_child(red)
    box.add_child(blue)
    box.add_child(yellow)
    root.add_child(panel)
    tree.set_root(root)
    set_window_title("SceneTree BoxContainer Test")

go()