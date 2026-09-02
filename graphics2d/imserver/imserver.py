"""
imserver.py (c) 2026-present by Pascal Schuppli. 

See LICENSE.md for license information.

This module runs the graphics server in a separate process via 
multiprocessing and handles communication between the server 
and client processes using queues.
"""

from multiprocessing import connection
import os
import multiprocessing as mp
import time
import sys, os.path

sys.path.append(os.path.join(sys.path[0], "../.."))

from graphics2d.imserver.connections import IPCQueueConnection
from gcommand import ServerCommand, ServerAnswer


# DO NOT IMPORT PYGAME HERE AT THE TOP LEVEL


class IMServer:
    def __init__(self, connection: IPCQueueConnection):
        self.connection = connection        
        self.gserver = self._initialize_graphics()
        
    def send_command_answer(self, answer: ServerAnswer):
        self.connection.send(answer.serialize())   

    def _initialize_graphics(self):
        # Initialize the server and start the event loop
        # We import Pygame strictly inside the server process to avoid
        # issues with Pygame's initialization in the client (parent) process
        
        from graphics2d.imserver.gserver import GraphicsServer
        return GraphicsServer()

    def event_loop(self):
        connection = self.connection
        gserver = self.gserver
        clock = gserver.get_clock()
      
        while not gserver.exit_requested():        
            for event in gserver.get_events():
                #print(f"[EVENT] Type: {event.type} | {event.dict}")

                handled = gserver.handle_pygame_event(event)

                if not handled:           
                    data = gserver.serialize_event(event)
                
                    # send event to parent process for handling
                    connection.send([event.type, data])
            
            # Here we receive commands from the client and handle them accordingly
            while connection.has_received_data():
                item = connection.receive()
                print(f"[imserver] Received item: {item}")
                connection.send(f"Processed item: {item}")
        
            gserver.present_all()
            gserver.run_defered()
            
            clock.tick(60)

        connection.send("QUIT")

    def quit(self):
        print("communication layer exiting...")
        self.connection.send("QUIT")
        self.gserver.quit()
                

def run_interactive_media_server(connection):        
    # Create our message-handling server
    imserver = IMServer(connection)
    
    # run the message and event handling loop...
    imserver.event_loop()
    # and exit
    imserver.quit()


def start_ipc_server(server_func):
    # Create the queued data exchange connection
    send = mp.Queue()
    receive = mp.Queue()
    conn = IPCQueueConnection(send, receive)
    server_conn = IPCQueueConnection(receive, send)
    process = mp.Process(target=server_func, args=(server_conn,))
    process.start()
    return process, conn


if __name__ == "__main__":
    # Force spawn method on Linux
    mp.set_start_method("spawn", force=True)
            
    process, conn = start_ipc_server(run_interactive_media_server)

    try:
        from graphics2d.imserver.gclient import GraphicsClient
        client = GraphicsClient(conn)
        client.event_loop()
    except Exception as e:
        # Log the error
        print(f"Exception in client event loop: {e}", file=sys.stderr)
        # Notify the server that it should exit due to an error in the client 
        client.send_command(ServerCommand(999))  # Example command
    finally:
        print("Client exiting...")
        process.join()