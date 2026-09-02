import time
import pygame.constants

from graphics2d.imserver.gcommand import ServerCommand, ServerAnswer

# Lets client code wait for events from the server in an async manner. We primarily use this
# to handle cases where the server needs to send back a response to a command sent by the client.
# Client code can then be written without the need to resort to callbacks which would complicate
# the code structure.
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


class GraphicsClient:
    def __init__(self, connection):
        self.connection = connection
        self.eventbus = EventBus()

    def send_command(self, command):
        self.connection.send(command.serialize())

    async def wait_for_response(self, request_id):
        return await self.eventbus.wait_for(request_id)

    def event_loop(self):
        print("Running client event loop...")
        running = True
        while running:
            # limit rate at which we check for messages from the child process
            time.sleep(0.01)
    
            # These are events happening in the child process/pygame we get informed about
            while self.connection.has_received_data():                
                msg = self.connection.receive()

                if isinstance(msg, ServerAnswer):
                    # If the message is a ServerAnswer, we publish it to the event bus so that 
                    # any waiting client code can receive it
                    self.eventbus.publish(msg.get_request_id(), msg)
                    continue

                if msg == "QUIT":
                    running = False
                    break
                if msg[0] == pygame.constants.MOUSEBUTTONDOWN:
                    print(f"[CLIENT] Received: MOUSEBUTTONDOWN | {msg[1]}")
                if msg[0] == pygame.constants.MOUSEBUTTONUP:
                    print(f"[CLIENT] Received: MOUSEBUTTONUP | {msg[1]}")
                if msg[0] == pygame.constants.KEYDOWN:
                    print(f"[CLIENT] Received: KEYDOWN | {msg[1]}")
                if msg[0] == pygame.constants.KEYUP:
                    print(f"[CLIENT] Received: KEYUP | {msg[1]}")
                if msg[0] == pygame.constants.VIDEORESIZE:
                    print(f"[CLIENT] Received: VIDEORESIZE | {msg[1]}")
                if msg[0] == pygame.constants.DROPFILE:
                    print(f"[CLIENT] Received: DROPFILE | {msg[1]}")
                if msg[0] == pygame.constants.DROPTEXT:
                    print(f"[CLIENT] Received: DROPTEXT | {msg[1]}")

      