import struct

from graphics2d.imserver.gserver import GraphicsServer


class ServerCommand:
    def __init__(self, id):
        self._id = id

    def get_cmd_id(self) -> int:
        return self._id

    def serialize(self) -> bytes:
        return b''

    def deserialize(self, data: bytes): 
        pass
    
    def execute(self, server: GraphicsServer):
        # Logic to execute the server command
        pass
