import inspect
import pygame
import pygame.font
import datetime
import graphics2d.drawing as draw

def empty_func(*args):
    pass

hooks = {
    'draw': empty_func,
    'update': empty_func,
    'ready': empty_func,
    'quit': empty_func,
    'resized': empty_func
}

settings = {
    'WIDTH' : 1280,
    'HEIGHT': 720,
    'AUTO_REDRAW': True,
    'MAX_FPS': 120,
    'FULLSCREEN': False,
    'RESIZABLE': False,
    'DEFAULT_FONT_SIZE': 24
}


screen = None
clock = None
needs_redraw = True
# This leads to draw() callback being called every frame. If you turn this off via disable_auto_redraw(), you'll need to call
# request_redraw() to have the event loop call draw().
auto_redraw = True

is_fullscreen=False
is_resizable=False

def _init():
    global screen, clock
    pygame.init()
    pygame.font.init()
    _honor_display_mode_settings()
    clock = pygame.time.Clock()
    print(pygame.display.get_desktop_sizes())
    print(pygame.display.list_modes())

def _get_display_flags():
    flags = 0
    if settings['RESIZABLE']:
        flags += pygame.RESIZABLE
    if settings['FULLSCREEN']:
        flags += pygame.FULLSCREEN        
    return flags    

def _honor_display_mode_settings(): 
    global is_fullscreen, is_resizable, screen
    width = settings['WIDTH']
    height = settings['HEIGHT']
    if settings['FULLSCREEN']:
        width = 0
        height = 0
    screen = pygame.display.set_mode((width, height), _get_display_flags())
    request_redraw()
    is_fullscreen = settings['FULLSCREEN']
    is_resizable = settings['RESIZABLE']


def _event_loop():
    global needs_redraw
    running = True
    last = datetime.datetime.now()    
    while running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:                
                hooks['resized'](event.w, event.h)
                
        now = datetime.datetime.now()
        dt = now-last
        last = now
        hooks['update'](dt.seconds * 1000 + (dt.microseconds / 1000))
        if needs_redraw or settings['AUTO_REDRAW']:
            hooks['draw']()
            pygame.display.flip()
            needs_redraw = False
        clock.tick(settings['MAX_FPS'])


def request_redraw():
    global needs_redraw
    needs_redraw = True

def draw_filled_rect(x, y, width, height, color):
    draw.draw_filled_rect(screen, pygame.Rect(x, y, width, height), color)

def draw_text(fontname, fontsize, text, x, y, color, antialiased=True, background=None):
    font = draw.get_font(fontname, fontsize)
    surface = draw.draw_text(font, text, color, antialiased, background)
    screen.blit(surface, pygame.Rect(x, y, 100, 10))


def get_size():
    return screen.get_size()

def get_default_fontname():
    return draw.get_default_fontname()
    

def go():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    g = dir(mod)
    for name in hooks.keys():
        if name in g:
            hooks[name] = getattr(mod, name)
    for name in settings.keys():
        if name in g:
            settings[name] = getattr(mod, name)

    _init()    
    _honor_display_mode_settings()    
    hooks['ready']()
    _event_loop()
    hooks['quit']()
    pygame.font.quit()
    pygame.quit()
    
        
