

 
import pygame.locals as pyconst

pygame = None


class GraphicsServer:
    def __init__(self, pygame_module):  
        global pygame      
        pygame = pygame_module        
        self.windows = {}
        self.renderers = []
        self.defered_calls = []
        self._exit_requested = False
        self.main_window_id = None
            
    def add_window(self, window, bgcolor=(255, 0, 255)):
        if self.main_window_id is None:
            self.main_window_id = window.id
        renderer = pygame._sdl2.video.Renderer(window)
        self.renderers.append(renderer)
        self.windows[window.id] = [window, renderer, bgcolor]
        self.clear_window(window.id)

    def get_desktop_sizes(self):
        return self.pygame.display.get_desktop_sizes()
    
    def get_renderer(self, window_id: int):
        if window_id in self.windows:
            return self.windows[window_id][1]
        return None

    def remove_window(self, window_id: int):
        if window_id in self.windows:
            window, renderer, color = self.windows[window_id]
            self.renderers.remove(renderer)
            window.destroy()            
            del self.windows[window_id]

    def set_window_background_color(self, window_id: int, color):
        if window_id in self.windows:
            self.windows[window_id][2] = color

    def clear_window(self, window_id: int):
        if window_id in self.windows:
            window, renderer, bgcolor = self.windows[window_id]
            renderer.draw_color = bgcolor
            renderer.clear()

    def present_all(self):
        for renderer in self.renderers:
            renderer.present()

    def handle_pygame_event(self, event) -> int:
        if event.type == pygame.QUIT:
            self._exit_requested = True
        elif event.type == pygame.WINDOWCLOSE:
            if event.window.id == self.main_window_id:
                self._exit_requested = True
            else:
                self.add_defered(lambda: self.remove_window(event.window))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._exit_requested = True
        elif event.type == pyconst.WINDOWSIZECHANGED:
            print("Window changed: ", event.window.id)
            self.clear_window(event.window.id)
        return False
    

    def handle_command_event(self, command):
        pass


    def exit_requested(self) -> bool:
        return self._exit_requested


    def add_defered(self, function):
        self.defered_calls.append(function)
    
    def run_defered(self):
        for call in self.defered_calls:
            call()
        self.defered_calls.clear()

    def serialize_event(self, event):
        d = event.dict.copy()
        if "window" in d:
            if d["window"] is not None:
                d["window"] = d['window'].id
            else:
                d['window'] = None
        return d
    
