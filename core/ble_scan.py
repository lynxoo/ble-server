import binascii
import time

import logging
from bluepy.btle import Scanner, BTLEException, ScanEntry, DefaultDelegate
from pony.orm import db_session, commit

from core import settings
from core.models import Device, Transmission, Packet


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        logging.info("Preparing data from {}".format(dev.addr))
        data = binascii.b2a_hex(dev.rawData).decode('utf-8').upper()
        packet = Packet(type=0, payload=data)
        txPower = [data[-1] for data in dev.getScanData() if 'Tx Power' in data]
        txPower = int(txPower.pop(), 16) if txPower else None
        tr = Transmission(
            device=dev.addr,
            time=time.time(),
            packet=packet,
            wallpoint=0,
            rssi=dev.rssi,
            direction=0,
            txPower=txPower
        )
        logging.info("Saving data: {}".format(tr))
        commit()

class AuthScanner(Scanner):
    """
        Class provides methods for 
    """

    @db_session
    def process(self, timeout=300.0):
        if self._helper is None:
            raise BTLEException(BTLEException.INTERNAL_ERROR,
                                "Helper not started (did you call start()?)")
        start = time.time()
        while True:
            if timeout:
                remain = start + timeout - time.time()
                if remain <= 0.0:
                    break
            else:
                remain = None
            resp = self._waitResp(['scan', 'stat'], remain)
            if resp is None:
                break
            respType = resp['rsp'][0]
            if respType == 'stat':
                logging.info("STAT message,")
                # if scan ended, restart it
                if resp['state'][0] == 'disc':
                    logging.warning("Executing SCAN cmd!")
                    self._mgmtCmd("scan")
            elif respType == 'scan':
                # device found
                addr = binascii.b2a_hex(resp['addr'][0]).decode('utf-8')
                addr = ':'.join([addr[i:i + 2] for i in range(0, 12, 2)])
                addr = addr.upper()
                if not Device.select(lambda d: d.id == addr).first() or settings.ALLOW_ANY:
                    logging.warning("Unknown device {} send message, skipping...".format(addr))
                    continue
                dev = ScanEntry(addr, self.iface)
                logging.info("SCAN message from {}".format(addr))
                if Device[addr].name != dev.name:
                    logging.error("{} invalid name, received:{}, valid: {}, skipping...".format(
                        dev.addr, dev.name, Device[addr].name))
                    continue
                dev._update(resp)
                if self.delegate is not None:
                    self.delegate.handleDiscovery(dev, (dev.updateCount <= 1), True)
            else:
                raise BTLEException(BTLEException.INTERNAL_ERROR, "Unexpected response: " + respType)
