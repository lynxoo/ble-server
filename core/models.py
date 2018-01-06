"""
    Module contains basic PonyORM models needed for collecting data from bluetooth devices. 
    
    module_author: Artur Malarz
    date: 14.11.2017
"""

from pony.orm import *

from core.settings import DATABASE as db

class Wallpoint(db.Entity):
    """
        Model Wallpoint represents sink-server collecting data.
        
        Attributes:
            id - (int) auto generated primary key.
    """
    transmissions = Set('Transmission')

class Device(db.Entity):
    """
        Model Device represents bluetooth node on the whitelist.

        Attributes:
            id - (str) bluetooth node's mac address. 
    """
    id = PrimaryKey(str, max_len=191)
    name = Optional(str, unique=True, nullable=True, max_len=191)
    transmissions = Set('Transmission')

    def __str__(self):
        return self.id

class Packet(db.Entity):
    """
        Model Packet represents message send by the bluetooth node.

        Attributes:
           id - (int) auto generated primary key.
           type - (int) type of received packet/
           seqNo - (int) ???
           payload - (bytes) data received from the bluetooth node.
    """
    type = Required(int)
    seqNo = Optional(int)
    payload = Required(str)
    transmission = Optional('Transmission')


class Transmission(db.Entity):
    """
        Model Transmission contains information about data transmission send from the bluetooth device.

        Attributes:
           id - (int) auto generated primary key.
           wallpoint - (int) id of wallpoint receiving data
           time - (float) time when transmission has been received. Time is represented by epoch. 
           packet - (int) id of packet received during transmission or send by the wallpoint.
           txPower - (int) 
           rsii - (int)
           direction - (int) direction of transmission in (0) or out (1) 
    """
    wallpoint = Required('Wallpoint')
    device = Required(Device)
    time = Required(float)
    packet = Required(Packet)
    txPower = Optional(int)
    rssi = Required(int)
    direction = Required(int)

    def __str__(self):
        return "{}  {}  {}  {}  {}  {}".format(self.id, self.time, self.device,
                                          self.packet.payload, self.rssi, self.txPower)
