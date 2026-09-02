import struct

class ServerCommand:
    def __init__(self, id):
        self._id = id

    def get_cmd_id(self) -> int:
        return self._id

    def serialize(self) -> bytes:
        return b''

    def deserialize(self, data: bytes): 
        pass
    
    def execute(self, command_dispatcher):
        # Logic to execute the server command
        pass


class ServerAnswer(ServerCommand):
    def __init__(self, id, request_id):
        self._id = id
        self.request_id = request_id

    def get_ans_id(self) -> int:
        return self._id

    def serialize(self) -> bytes:
        return b''

    def deserialize(self, data: bytes): 
        pass