Small teaching-oriented pygame framework
========================================

This is a framework somewhat similar to pgzero. The goal is to make it easier to teach pygame graphics
programming in high school environments without getting in the way of doing more advanced pygame stuff.

The shortest graphics program looks like this:

    from graphics2d import *

    def on_draw():
        draw_circle((250, 250), 100, RED, 2)

    go()

And here's one which animates the circle's color:

    from graphics2d import *
    
    def on_draw():
        color = pick_one_of(BLUE, RED, YELLOW, GREEN, WHITE)
        draw_circle((250, 250), 100, color, 2)

    go()




