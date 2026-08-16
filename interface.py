import queue
import select
import socket
import threading
from header import Header
from response import Response

class Interface:
    def __init__(self, ipAddress, port):
        self.closeEvent = threading.Event()
        self.commandQueue = queue.Queue()
        self.responseQueue = queue.Queue()
        self.notificationQueue = queue.Queue()
        self.worker = InterfaceWorker(self.closeEvent,
                                      ipAddress,
                                      port,
                                      self.commandQueue,
                                      self.responseQueue,
                                      self.notificationQueue)
        self.worker.start()

    def shutdown(self):
        self.closeEvent.set()
        self.worker.join()

    def transceive(self, command):
        self.commandQueue.put(command)
        response = self.responseQueue.get()
        if not command.header.sequenceNumber == response.header.sequenceNumber:
            raise RuntimeError('sequence number mismatch:\n' +
                               f'sent: {command.sequenceNumber}, ' +
                               f'received: {response.sequenceNumber}')
        return response

    def getNotification(self):
        return self.notificationQueue.get()

class InterfaceWorker(threading.Thread):
    protocolVersion = 1
    responseCodes = {0: 'Success',
                     1: 'Invalid Message Type',
                     2: 'Generic Error',
                     3: 'Service Not Found',
                     4: 'Characteristic Not Found',
                     5: 'Characteristic Operation Not Supported',
                     6: 'Characteristic Write Failed', }

    def __init__(self, closeEvent, ipAddress, port, commandQueue, responseQueue, notificationQueue):
        threading.Thread.__init__(self)
        self.closeEvent = closeEvent
        self.commandQueue = commandQueue
        self.responseQueue = responseQueue
        self.notificationQueue = notificationQueue
        self.sequenceNumber = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.connect((ipAddress, port))

    def run(self):
        while True:
            if self.closeEvent.is_set():
                self.close()
                return
            try:
                self.transmit(self.commandQueue.get(block=False))
            except queue.Empty:
                pass
            if select.select([self.socket, ], [], [], 0.1)[0]:
                response = self.receive()
                if response.isNotification():
                    self.notificationQueue.put(response)
                else:
                    self.responseQueue.put(response)

    def close(self):
        self.socket.close()

    def transmit(self, command):
        self.socket.sendall(command.toBytes())

    def receive(self):
        header = self._receiveHeader()
        payload = self.receiveBytes(header.payloadLength)
        return Response.fromBytes(header, payload)

    def _receiveHeader(self):
        header = Header.fromBytes(self.receiveBytes(Header.size))
        if header.responseCode:
            raise RuntimeError(self.responseCodes[header.responseCode])
        return header

    def receiveBytes(self, size):
        message = bytearray()
        while len(message) < size:
            if (size - len(message)) > 4096:
                part = self.socket.recv(4096)
            else:
                part = self.socket.recv(size - len(message))
            if not part:
                raise EOFError('Could not receive all expected data')
            message += part
        return message

    def pollResponse(self, timeout_s):
        if select.select([self.socket], [], [], timeout_s)[0]:
            response = self.receive()
            if response.isError():
                raise RuntimeError(f'error response {response}')
            return response
        else:
            raise TimeoutError(f'no response within {timeout_s}s')
