from obswebsocket import obsws


class ObsConnection:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.client = obsws(self.host, self.port, self.password)

    def __enter__(self):
        print("Connecting to OBS...")
        self.client.connect()
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        print("Disconnecting from OBS...")
        self.client.disconnect()
