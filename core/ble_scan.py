import binascii
import time
from bluepy.btle import Scanner, BTLEException, ScanEntry, DefaultDelegate
from pony.orm import db_session

from core.models import Device, Transmission, Packet


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    @db_session
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)
        packet = Packet(type=0, payload=dev.rawData)
        Transmission(
            device=dev.addr,
            time=time.time(),
            packet=packet,
            wallpoint = 0,
            rssi = dev.rssi,
            direction = 0)
        txPower = [data[-1] for data in dev.getScanData() if 'Tx Power' in data]
        Transmission.txPower = txPower.pop() if txPower else None

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
                # if scan ended, restart it
                if resp['state'][0] == 'disc':
                    self._mgmtCmd("scan")

            elif respType == 'scan':
                # device found
                addr = binascii.b2a_hex(resp['addr'][0]).decode('utf-8')
                addr = ':'.join([addr[i:i + 2] for i in range(0, 12, 2)])
                try:
                    Device[addr]
                except:
                    print(addr)
                    continue
                if addr in self.scanned:
                    dev = self.scanned[addr]
                else:
                    dev = ScanEntry(addr, self.iface)
                    self.scanned[addr] = dev
                isNewData = dev._update(resp)
                if self.delegate is not None:
                    self.delegate.handleDiscovery(dev, (dev.updateCount <= 1), isNewData)

            else:
                raise BTLEException(BTLEException.INTERNAL_ERROR, "Unexpected response: " + respType)