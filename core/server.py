"""
    Module contains server class.

    module_author: Artur Malarz
    date: 14.11.2017
"""
from pony.orm import db_session

from core.models import Packet
from core.settings import DATABASE as db
from core.ble_scan import AuthScanner, ScanDelegate

class Server:
    """
        Class Server provides application's initialization and methods for bluetooth nodes management.
    """

    def __init__(self):
        """
            Server's initialization, initialize server attributes and calls required methods. 
        """
        db.generate_mapping(create_tables=True)
        self.time = 300

    @db_session
    def run(self):
        scanner = AuthScanner().withDelegate(ScanDelegate())
        devices = scanner.scan(timeout=self.time)