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

class IPCQueueConnection:
    def __init__(self, send, recv):
        self._send = send
        self._recv = recv

    def send(self, data):
        self._send.put(data)

    def has_received_data(self) -> bool:
        return not self._recv.empty()

    def receive(self):
        return self._recv.get()


class EventBus:
    def __init__(self):
        self.futures = {}

    async def wait_for(self, event_id):
        future = self.futures.get(event_id)
        if future is None:
            future = asyncio.get_running_loop().create_future()
            self.futures[event_id] = future
        return await future

    def publish(self, event_id, data):
        future = self.futures.pop(event_id, None)
        if future is None:
            future = asyncio.get_running_loop().create_future()
            self.futures[event_id] = future
        future.set_result(data)
        


def run_interactive_media_server(connection):
    # Explicitly set X11 environment parameters
    # Only works on linux platform
    #os.environ["SDL_VIDEODRIVER"] = "x11"
    
    # Import Pygame strictly inside the child process
    import pygame
    from pygame._sdl2.video import Window, Renderer, Texture    
    from graphics2d.imserver.gserver import GraphicsServer

    pygame.init()

    eventbus = EventBus()

    gserver = GraphicsServer(pygame, eventbus)
        
    gserver.add_window(Window("Main Window", size=(700, 700), resizable=True))
    gserver.add_window(Window("Log", size=(350, 700), resizable=False), bgcolor=(35, 35, 35, 200))
           
    clock = pygame.time.Clock()
      
    while not gserver.exit_requested():        
        pygame.event.pump()
        
        for event in pygame.event.get():
            #print(f"[EVENT] Type: {pygame.event.event_name(event.type)} | {event.dict}")

            handled = gserver.handle_pygame_event(event)

            if not handled:           
                data = gserver.serialize_event(event)
            
                # send event to parent process for handling
                connection.send([event.type, data])
        
        # Here we receive commands from the client and handle them accordingly
        while connection.has_received_data():
            item = connection.receive()
            print(f"[CHILD] Received item: {item}")
            connection.send(f"Processed item: {item}")
      

        gserver.present_all()
        gserver.run_defered()
        
        clock.tick(60)

    connection.send("QUIT")
    pygame.quit()
    print("interactive media server exiting...")


def start_ipc_server(server_func):
    # Create the queued data exchange connection
    send = mp.Queue()
    receive = mp.Queue()
    conn = IPCQueueConnection(send, receive)
    server_conn = IPCQueueConnection(receive, send)
    process = mp.Process(target=server_func, args=(server_conn,))
    process.start()
    return process, conn    



def client_event_loop(conn : IPCQueueConnection):
    
    running = True
    while running:
        # limit rate at which we check for messages from the child process
        time.sleep(0.01)

        # These are events happening in the child process/pygame we get informed about
        while conn.has_received_data():
            msg = conn.receive()
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
    



if __name__ == "__main__":
    # Force spawn method on Linux
    mp.set_start_method("spawn", force=True)

    import pygame.constants

    process, conn = start_ipc_server(run_interactive_media_server)

    client_event_loop(conn)
                
    print("Client exiting...")
    process.join()