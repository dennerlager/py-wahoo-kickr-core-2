"""credits go to
https://github.com/elfrances/wahoo-fitness-tnp
https://github.com/kilianyp/hacs-wahoo-wftnp
"""
import atexit
import struct
from command import Command
from interface import Interface
from ftms import services, characteristics

class Wkc2:
    hostname = 'KICKR-CORE-3CFD.local'
    ipAddress = '192.168.1.120'
    port = 36866

    def __init__(self):
        self.interface = Interface(self.ipAddress, self.port)
        atexit.register(self.interface.shutdown)

    def discoverServices(self):
        return self.interface.transceive(
            Command.create('discoverServices'))

    def discoverCharacteristics(self, service):
        return self.interface.transceive(
            Command.create('discoverCharacteristics',
                           service))

    def readCharacteristic(self, name):
        return self.interface.transceive(
            Command.create('readCharacteristic',
                           characteristics[name]))

    def enableCharacteristicNotification(self, name):
        self.interface.transceive(
            Command.create('enableCharacteristicNotification',
                           characteristics[name],
                           1))

    def disableCharacteristicNotification(self, name):
        self.interface.transceive(
            Command.create('enableCharacteristicNotification',
                           characteristics[name],
                           0))

    def getSerialNumber(self):
        return self.readCharacteristic('serialNumber').data.decode('ascii')

    def getFirmwareRevision(self):
        return self.readCharacteristic('firmwareRevision').data.decode('ascii')

    def getHardwareRevision(self):
        return self.readCharacteristic('hardwareRevision').data.decode('ascii')

    def getManufacturerName(self):
        return self.readCharacteristic('manufacturerName').data.decode('ascii')

    def getSensorLocation(self):
        return self.readCharacteristic('sensorLocation')

    def getCyclingPowerFeature(self):
        return f"{struct.unpack('<H', self.readCharacteristic('cyclingPowerFeature').data)[0]:#_b}"

    def getFitnessMachineFeature(self):
        """
        Bit Number Definition
        0  Average Speed Supported
        1  Cadence Supported
        2  Total Distance Supported
        3  Inclination Supported
        4  Elevation Gain Supported
        5  Pace Supported
        6  Step Count Supported
        7  Resistance Level Supported
        8  Stride Count Supported
        9  Expended Energy Supported
        10  Heart Rate Measurement Supported
        11  Metabolic Equivalent Supported
        12  Elapsed Time Supported
        13  Remaining Time Supported
        14  Power Measurement Supported
        15  Force on Belt and Power Output Supported
        16  User Data Retention Supported
        17-31  Reserved for Future Use
        32-63 ?
        """
        return f"{struct.unpack('<Q', self.readCharacteristic('fitnessMachineFeature').data)[0]:#_b}"

    def getTrainingStatus(self):
        return self.readCharacteristic('trainingStatus')

    def getSupportedResistanceLevelRange(self):
        """returns:
        minimum resistance level,
        maximum resistance level,
        minimum increment
        """
        return struct.unpack('<HHH', self.readCharacteristic('supportedResistanceLevelRange').data)

    def getSupportedPowerRange(self):
        """returns:
        minimum power,
        maximum power,
        minimum increment
        """
        return struct.unpack('<HHH', self.readCharacteristic('supportedPowerRange').data)

    def getWeight(self):
        return struct.unpack('<H', self.readCharacteristic('weight').data)[0] / 200

    def getNotification(self):
        return self.interface.getNotification()

    def requestControl(self):
        self.interface.transceive(
            Command.create('writeCharacteristic',
                           characteristics['fitnessMachineControlPoint'],
                           struct.pack('<B', 0)))

    def setResistance(self, resistance):
        self.interface.transceive(
            Command.create('writeCharacteristic',
                           characteristics['fitnessMachineControlPoint'],
                           struct.pack('<BB', 4, resistance)))

    def setPower(self, power):
        self.interface.transceive(
            Command.create('writeCharacteristic',
                           characteristics['fitnessMachineControlPoint'],
                           struct.pack('<Bh', 5, power)))

if __name__ == '__main__':
    w = Wkc2()
    # import pprint
    # pprint.pprint(w.discoverServices())
    # for serviceName, uid in services.items():
    #     print(serviceName)
    #     pprint.pprint(w.discoverCharacteristics(uid))
    # print(w.getSerialNumber())
    # print(w.getFirmwareRevision())
    # print(w.getHardwareRevision())
    # print(w.getManufacturerName())
    # print(w.getSensorLocation())
    # print(w.getCyclingPowerFeature())
    # print(w.getFitnessMachineFeature())
    # print(w.getTrainingStatus())
    # print(w.getSupportedResistanceLevelRange())
    # print(w.getSupportedPowerRange())
    # print(w.getWeight())

    w.requestControl()

    w.enableCharacteristicNotification('indoorBikeData')
    for r in [10, 20, 30, 40]:
        w.setResistance(r)
        for i in range(10):
            nt = w.getNotification()
            print(nt.characteristic)
            print(nt.data)
    w.setResistance(10)

    # w.enableCharacteristicNotification('indoorBikeData')
    # for p in [100, 200, 300]:
    #     w.setPower(p)
    #     for i in range(10):
    #         nt = w.getNotification()
    #         print(nt.characteristic)
    #         print(nt.data)
    # w.setResistance(10)

    w.interface.shutdown()
