
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
