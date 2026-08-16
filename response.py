import uuid
from parser import parse

class Response:
    """Use factory method 'fromBytes(header, payload)' to instantiate"""
    data = None
    # characteristicFormats = {}

    @staticmethod
    def fromBytes(header, payload):
        try:
            return messageTypes[header.messageType](header, payload)
        except KeyError:
            raise ValueError(f'invalid message type: {header.messageType}')

    def __init__(self, header, payload):
        self.header = header
        self.parseDataFromPayload(payload)

    def parseDataFromPayload(self, payload):
        """overwrite me to implement different byte arrangement of data"""
        self.data = payload

    def __repr__(self):
        return 'response: {}, data: [{}]'.format(self.__class__.__name__, self.data)

    def isNotification(self):
        return False

class DiscoverServices(Response):
    def parseDataFromPayload(self, payload):
        self.data = []
        while payload:
            self.data.append(uuid.UUID(bytes=bytes(payload[:16])))
            payload = payload[16:]

class DiscoverCharacteristics(Response):
    """properties:
    value description
    0x01  read
    0x02  write
    0x04  notify"""
    def parseDataFromPayload(self, payload):
        self.service = uuid.UUID(bytes=bytes(payload[:16]))
        payload = payload[16:]
        self.data = {}
        while payload:
            characteristic = uuid.UUID(bytes=bytes(payload[:16]))
            payload = payload[16:]
            properties = payload[:1][0]
            payload = payload[1:]
            self.data[characteristic] = properties

class ReadCharacteristic(Response):
    def parseDataFromPayload(self, payload):
        self.characteristic = uuid.UUID(bytes=bytes(payload[:16]))
        self.data = payload[16:]

class WriteCharacteristic(Response):
    def parseDataFromPayload(self, payload):
        self.characteristic = uuid.UUID(bytes=bytes(payload))

class EnableCharacteristicNotifications(WriteCharacteristic):
    pass

class CharacteristicNotification(ReadCharacteristic):
    def parseDataFromPayload(self, payload):
        self.characteristic = uuid.UUID(bytes=bytes(payload[:16]))
        self.data = parse(self.characteristic, payload[16:])

    def isNotification(self):
        return True

messageTypes = {1: DiscoverServices,
                2: DiscoverCharacteristics,
                3: ReadCharacteristic,
                4: WriteCharacteristic,
                5: EnableCharacteristicNotifications,
                6: CharacteristicNotification, }
