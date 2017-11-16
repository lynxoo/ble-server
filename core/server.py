from core.settings import DATABASE as db
from core.ble_scan import AuthScanner, ScanDelegate

class Server:

    def __init__(self):
        db.generate_mapping(create_tables=True)

    def run(self):

        scanner = AuthScanner().withDelegate(ScanDelegate())
        devices = scanner.scan(300.0)

        for dev in devices:
            print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print("  {} = {}".format(desc, value))