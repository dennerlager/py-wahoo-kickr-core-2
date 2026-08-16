import uuid

services = {
    'deviceInformationService': uuid.UUID('0000180a-0000-1000-8000-00805f9b34fb'),
    'cyclingPowerService': uuid.UUID('00001818-0000-1000-8000-00805f9b34fb'),
    'fitnessMachineService': uuid.UUID('00001826-0000-1000-8000-00805f9b34fb'),
    'userDataService': uuid.UUID('0000181c-0000-1000-8000-00805f9b34fb'),
    'heartRateService': uuid.UUID('0000180d-0000-1000-8000-00805f9b34fb')}

characteristics = {
    'serialNumber': uuid.UUID('00002a25-0000-1000-8000-00805f9b34fb'),
    'firmwareRevision': uuid.UUID('00002a26-0000-1000-8000-00805f9b34fb'),
    'hardwareRevision': uuid.UUID('00002a27-0000-1000-8000-00805f9b34fb'),
    'manufacturerName':  uuid.UUID('00002a29-0000-1000-8000-00805f9b34fb'),
    'sensorLocation': uuid.UUID('00002a5d-0000-1000-8000-00805f9b34fb'),
    'cyclingPowerMeasurement': uuid.UUID('00002a63-0000-1000-8000-00805f9b34fb'),
    'cyclingPowerFeature': uuid.UUID('00002a65-0000-1000-8000-00805f9b34fb'),
    'cyclingPowerControlPoint': uuid.UUID('00002a66-0000-1000-8000-00805f9b34fb'),
    'fitnessMachineFeature': uuid.UUID('00002acc-0000-1000-8000-00805f9b34fb'),
    'indoorBikeData': uuid.UUID('00002ad2-0000-1000-8000-00805f9b34fb'),
    'trainingStatus': uuid.UUID('00002ad3-0000-1000-8000-00805f9b34fb'),
    'supportedResistanceLevelRange': uuid.UUID('00002ad6-0000-1000-8000-00805f9b34fb'),
    'supportedPowerRange': uuid.UUID('00002ad8-0000-1000-8000-00805f9b34fb'),
    'fitnessMachineControlPoint': uuid.UUID('00002ad9-0000-1000-8000-00805f9b34fb'),
    'fitnessMachineStatus': uuid.UUID('00002ada-0000-1000-8000-00805f9b34fb'),
    'weight': uuid.UUID('00002a98-0000-1000-8000-00805f9b34fb'),
    'heartRateMeasurement': uuid.UUID('00002a37-0000-1000-8000-00805f9b34fb'),
    'bodySensorLocation': uuid.UUID('00002a38-0000-1000-8000-00805f9b34fb')}
