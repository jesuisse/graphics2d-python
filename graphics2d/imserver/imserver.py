"""
imserver.py (c) 2026-present by Pascal Schuppli. 

See LICENSE.md for license information.

This module runs pygame in a separate process and handles communication between the parent
and child processes.
"""

import os
import multiprocessing as mp
import time

import sys, os.path
sys.path.append(os.path.join(sys.path[0], "../.."))


# DO NOT IMPORT PYGAME HERE AT THE TOP LEVEL



def run_interactive_media_server(receive, send):
    # Explicitly set X11 environment parameters
    # Only works on linux platform
    #os.environ["SDL_VIDEODRIVER"] = "x11"
    
    # Import Pygame strictly inside the child process
    import pygame
    from pygame._sdl2.video import Window, Renderer, Texture    
    from graphics2d.imserver.gserver import GraphicsServer

    pygame.init()

    gserver = GraphicsServer(pygame)
        
    gserver.add_window(Window("Main Window", size=(700, 700), resizable=True))
    gserver.add_window(Window("Tools", size=(350, 700), resizable=False), bgcolor=(35, 35, 35, 200))
    
    print("[CHILD] Window created. Move mouse or press keys over the window...")
    
    clock = pygame.time.Clock()
    running = True
    
    while not gserver.exit_requested():        
        pygame.event.pump()
        
        for event in pygame.event.get():
            print(f"[EVENT] Type: {pygame.event.event_name(event.type)} | {event.dict}")

            gserver.handle_pygame_event(event)
                        
            d = event.dict
            if "window" in d:
                if d["window"] is not None:
                    d["window"] = d['window'].id
                else:
                    d['window'] = None
            
            # send event to parent process
            send.put([event.type, d])
        
        # Here we receive commands from the parent process and handle them accordingly
        while not receive.empty():
            item = receive.get()
            print(f"[CHILD] Received item: {item}")
            send.put(f"Processed item: {item}")
      

        gserver.present_all()
        gserver.run_defered()
        
        clock.tick(60)

    send.put("QUIT")
    pygame.quit()
    print("interactive media server exiting...")


if __name__ == "__main__":
    # Force spawn method on Linux
    mp.set_start_method("spawn", force=True)

    import pygame.constants

    send = mp.Queue()
    receive = mp.Queue()
        
    process = mp.Process(target=run_interactive_media_server, args=(send, receive))
    process.start()
    running = True
    while running:
        # limit rate at which we check for messages from the child process
        time.sleep(0.01)

        # These are events happening in the child process/pygame we get informed about
        while not receive.empty():
            msg = receive.get()
            if msg == "QUIT":
                running = False
                break
            if msg[0] == pygame.constants.MOUSEBUTTONDOWN:
                print(f"[PARENT] Received: MOUSEBUTTONDOWN | {msg[1]}")
            if msg[0] == pygame.constants.MOUSEBUTTONUP:
                print(f"[PARENT] Received: MOUSEBUTTONUP | {msg[1]}")
            if msg[0] == pygame.constants.KEYDOWN:
                print(f"[PARENT] Received: KEYDOWN | {msg[1]}")
            if msg[0] == pygame.constants.KEYUP:
                print(f"[PARENT] Received: KEYUP | {msg[1]}")
            if msg[0] == pygame.constants.VIDEORESIZE:
                print(f"[PARENT] Received: VIDEORESIZE | {msg[1]}")
            if msg[0] == pygame.constants.DROPFILE:
                print(f"[PARENT] Received: DROPFILE | {msg[1]}")
            if msg[0] == pygame.constants.DROPTEXT:
                print(f"[PARENT] Received: DROPTEXT | {msg[1]}")

    
            
    print("Parent exiting...")
    process.join()