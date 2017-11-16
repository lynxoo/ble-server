from datetime import time

from pony.orm import *
from core.settings import DATABASE as db

class Wallpoint(db.Entity):
    id = PrimaryKey(int, auto=True)
    transmissions = Set('Transmission')

class Device(db.Entity):
    id = PrimaryKey(str)
    transmissions = Set('Transmission')

class Packet(db.Entity):
    id = PrimaryKey(int, auto=True)
    type = Required(int)
    seqNo = Optional(int)
    payload = Required(bytes)
    transmission = Optional('Transmission')

class Transmission(db.Entity):
    wallpoint = Required('Wallpoint')
    device = Required(Device)
    time = Required(float)
    packet = Required(Packet)
    txPower = Optional(int)
    rssi = Required(int)
    direction = Required(int)
