from google.protobuf.json_format import MessageToDict
from sabana import requests as sabana_req


class Program:
    """
    Program: Holds a series of operations to be executed on a Sabana Instance.
    """

    def __init__(self):
        self.req = sabana_req.execute_request()

    def __del__(self):
        del self.req

    def clear(self):
        self.__del__()
        self.req = sabana_req.execute_request()

    def to_dict(self):
        return MessageToDict(self.req)

    def buffer_alloc(self, name=None, size=None, mmio=None, offset=None):
        self.req.requests.append(sabana_req.buffer_alloc(name, size, mmio, offset))

    def buffer_write(self, data, name=None, offset=None):
        self.req.requests.append(sabana_req.buffer_write(name, offset, data))

    def buffer_wait(self, data, name=None, offset=None, timeout=None):
        self.req.requests.append(sabana_req.buffer_wait(name, offset, data, timeout))

    def buffer_read(self, name=None, offset=None, ty=None, shape=None):
        self.req.requests.append(sabana_req.buffer_read(name, offset, ty, shape))

    def buffer_dealloc(self, name=None):
        self.req.requests.append(sabana_req.buffer_dealloc(name))

    def mmio_alloc(self, name=None, size=None):
        self.req.requests.append(sabana_req.mmio_alloc(name, size))

    def mmio_write(self, data, name=None, offset=None):
        self.req.requests.append(sabana_req.mmio_write(name, offset, data))

    def mmio_wait(self, data, name=None, offset=None, timeout=None):
        self.req.requests.append(sabana_req.mmio_wait(name, offset, data, timeout))

    def mmio_read(self, name=None, offset=None, ty=None, shape=None):
        self.req.requests.append(sabana_req.mmio_read(name, offset, ty, shape))

    def mmio_dealloc(self, name=None):
        self.req.requests.append(sabana_req.mmio_dealloc(name))
