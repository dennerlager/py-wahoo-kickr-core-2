import struct
from response import messageTypes

class Header:
    format_ = struct.Struct('!BBBBH')
    size = format_.size
    def __init__(self,
                 protocolVersion,
                 messageType,
                 sequenceNumber,
                 responseCode,
                 payloadLength):
        (self.protocolVersion,
         self.messageType,
         self.sequenceNumber,
         self.responseCode,
         self.payloadLength) = (
            protocolVersion,
            messageType,
            sequenceNumber,
            responseCode,
            payloadLength)

    @staticmethod
    def fromBytes(bytestream):
        return Header(*Header.format_.unpack(bytestream))

    def toBytes(self):
        return self.format_.pack(self.protocolVersion,
                                 self.messageType,
                                 self.sequenceNumber,
                                 self.responseCode,
                                 self.payloadLength)

    def __repr__(self):
        return (f'protocol: {self.protocolVersion}\n' +
                f'message type: {messageTypes[self.messageType]}\n' +
                f'sequence number: {self.sequenceNumber}\n' +
                f'response code: {self.responseCode}\n' +
                f'payload length: {self.payloadLength}')
