import abc
from header import Header

protocolVersion = 1
class SequenceNumberGenerator:
    sequenceNumber = 0
    def new(self):
        self.sequenceNumber += 1
        self.sequenceNumber %= 256
        return self.sequenceNumber

class Command(abc.ABC):
    sequencNumberGenerator = SequenceNumberGenerator()

    @staticmethod
    def create(commandName, *argv):
        return commands[commandName](*argv)

    def __init__(self, *argv):
        self.payload = self.argparse(*argv)
        self.header = Header(protocolVersion,
                             self.messageType,
                             self.sequencNumberGenerator.new(),
                             0,
                             len(self.payload))

    @abc.abstractmethod
    def argparse(self, *argv):
        pass

    def toBytes(self):
        return self.header.toBytes() + self.payload

class DiscoverServices(Command):
    messageType = 1
    def argparse(self, *argv):
        return bytes()

class DiscoverCharacteristics(Command):
    messageType = 2
    def argparse(self, *argv):
        service = argv[0]
        return service.bytes

class ReadCharacteristic(Command):
    messageType = 3
    def argparse(self, *argv):
        characteristic = argv[0]
        return characteristic.bytes

class WriteCharacteristic(Command):
    messageType = 4
    def argparse(self, *argv):
        characteristic = argv[0]
        bytestream = argv[1]
        return characteristic.bytes + bytestream

class EnableCharacteristicNotifications(Command):
    """the enable/disable byte seems to be ignored"""
    messageType = 5
    def argparse(self, *argv):
        characteristic = argv[0]
        value = argv[1]
        return characteristic.bytes + bytes([value, ])

commands = {
    'discoverServices': DiscoverServices,
    'discoverCharacteristics':  DiscoverCharacteristics,
    'readCharacteristic': ReadCharacteristic,
    'writeCharacteristic': WriteCharacteristic,
    'enableCharacteristicNotification': EnableCharacteristicNotifications, }
