class Server:
    ip = 1

    def __init__(self):
        self.ip = Server.ip
        Server.ip += 1
        self.buffer = []
        self.router = None

    def send_data(self, data):
        if self.router is not None:
            self.router.buffer.append(data)

    def get_data(self):
        returned_buffer = self.buffer.copy()
        self.buffer.clear()
        return returned_buffer


    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.connect_pool = []
        self.buffer = []

    def link(self, server: Server):
        if server not in self.connect_pool:
            self.connect_pool.append(server)
            server.router = self

    def unlink(self, server: Server):
        if server in self.connect_pool:
            self.connect_pool.remove(server)
            server.router = None

    def send_data(self):
        for elem in self.buffer:
            for server in self.connect_pool:
                if elem.ip == server.ip:
                    server.buffer.append(elem)
        self.buffer.clear()


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


