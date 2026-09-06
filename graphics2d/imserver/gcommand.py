import struct
import pickle

class ServerCommand:
    def __init__(self, id):
        self._id = id

    def get_cmd_id(self) -> int:
        return self._id

    def serialize(self) -> bytes:
        return struct.pack('i', self._id)  # Serialize the command ID as an integer

    @staticmethod
    def deserialize(data: bytes):
        return struct.unpack('i', data)[0]  # Deserialize the command ID from bytes

    @staticmethod 
    def resurrect(cmd_id, payload_data : bytes):
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

    @staticmethod
    def deserialize(data: bytes):
        pass


class ZeroOperandsCommand(ServerCommand):
    def __init__(self, id):
        super().__init__(id)

    def resurrect(cmd_id, payload_data: bytes):
        assert len(payload_data) == 0, "ZeroOperandsCommand should have no payload data"        
        return ZeroOperandsCommand(cmd_id)
    
    def execute(self, command_dispatcher):
        # No operation command does nothing
        pass

class PythonPickleCommand(ServerCommand):
    def __init__(self, id, payload):
        super().__init__(id)
        self.payload = payload

    def serialize(self) -> bytes:        
        idbytes = super().serialize()
        payload_bytes = pickle.dumps(self.payload)
        return idbytes + payload_bytes    

    @staticmethod
    def resurrect(cmd_id, payload_data: bytes):
        return PythonPickleCommand(cmd_id, __class__.deserialize(payload_data))

    @staticmethod
    def deserialize(data: bytes):
        return pickle.loads(data)

class CommandFactory:

    def __init__(self):
        self.class_registry = {}

    def register_command(self, cmd_id, command_class):
        self.class_registry[cmd_id] = command_class

    def deserialize(self, data: bytes) -> ServerCommand:
        cmd_id = ServerCommand.deserialize(data[:4])
        command_class = self.class_registry.get(cmd_id)
        if command_class is None:
            raise ValueError(f"Unknown command class for id {cmd_id}")

        new_command = command_class.resurrect(cmd_id, data[4:])
        return new_command
   

    @staticmethod
    def create_command(cmd_id, payload=None):
        if cmd_id == CMD_ID_EXIT_DUE_TO_CLIENT_ERROR:
            return ZeroOperandsCommand(cmd_id)
        elif cmd_id == CMD_ID_EXIT_DUE_TO_SERVER_ERROR:
            return ZeroOperandsCommand(cmd_id)
        elif cmd_id == CMD_ID_GRAPHICS_EVENT:
            return PythonPickleCommand(cmd_id, payload)
        else:
            raise ValueError(f"Unknown command ID: {cmd_id}")

CMD_ID_EXIT_DUE_TO_CLIENT_ERROR = -1
CMD_ID_EXIT_DUE_TO_SERVER_ERROR = -2

CMD_ID_GRAPHICS_EVENT = 1
CMD_ID_CREATE_WINDOW = 2
CMD_ID_CLOSE_WINDOW = 3
CMD_ID_RESIZE_WINDOW = 4
CMD_ID_FLIP_FULLSCREEN_WINDOW = 5
CMD_ID_SET_WINDOW_TITLE = 6



CMD_EXIT_DUE_TO_CLIENT_ERROR = ZeroOperandsCommand(CMD_ID_EXIT_DUE_TO_CLIENT_ERROR)
CMD_EXIT_DUE_TO_SERVER_ERROR = ZeroOperandsCommand(CMD_ID_EXIT_DUE_TO_SERVER_ERROR)




