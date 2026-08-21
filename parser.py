"""https://www.bluetooth.com/specifications/gss/"""
import uuid
import struct
from dataclasses import dataclass

@dataclass
class Field:
    name: str
    format_: str
    unit: str=''
    scale: float=1

def parse(characteristic, payload):
    return parser[characteristic]().parse(payload)

class Parser:
    def parse(self, payload):
        flags = self.flagsFormat.unpack_from(payload, 0)[0]
        # some bits are active-low. invert them that all are active-high:
        flags ^= self.inverterMask
        offset = self.flagsFormat.size
        data = {}
        for bit, field in self.bits.items():
            if 2**bit & flags:
                data[field.name] = struct.unpack_from(field.format_, payload, offset)[0] * field.scale
                offset += struct.calcsize(field.format_)
        return data

class IndoorBikeDataParser(Parser):
    flagsFormat = struct.Struct('<H')
    inverterMask = 1
    bits = {
        0: Field(name='instantaneous speed', format_='<H', unit='km/h', scale=0.01),
        1: Field(name='average speed', format_='<H', unit='km/h', scale=0.01),
        2: Field(name='instantaneous cadence', format_='<H', unit='rpm', scale=0.5),
        3: Field(name='average cadence', format_='<H', unit='rpm', scale=0.5),
        4: Field(name='total distance', format_='uint24', unit='m'),
        5: Field(name='resistance level', format_='<B'),
        6: Field(name='instantaneous power', format_='<h', unit='W'),
        7: Field(name='average power', format_='<h', unit='W'),
        8: Field(name='expended energy', format_='<HHB', unit='kcal'),
        9: Field(name='heart rate', format_='<B', unit='bpm'),
        10: Field(name='metabolic equivalent', format_='<B'),
        11: Field(name='elapsed time', format_='<H', unit='s'),
        12: Field(name='remaining time', format_='<H', unit='s'),
    }

parser = {
    uuid.UUID('00002ad2-0000-1000-8000-00805f9b34fb'): IndoorBikeDataParser,
    }
