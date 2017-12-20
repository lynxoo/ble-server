"""
    Module contains server class.

    module_author: Artur Malarz
    date: 14.11.2017
"""
import logging
from datetime import datetime

from pony.orm import db_session

import core.settings as settings
from core.ble_scan import AuthScanner, ScanDelegate

class Server:
    """
        Class Server provides application's initialization and methods for bluetooth nodes management.
    """

    def __init__(self, path=None):
        """
            Server's initialization, initialize server attributes and calls required methods. 
        """
        if settings.LOGFILE:
            if not path:
                path = "logs / {}_debug.txt".format(datetime.now().isoformat())
            logging.basicConfig(filename=path, format='%(asctime)s %(levelname)s >> %(message)s', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s %(levelname)s >> %(message)s', level=logging.DEBUG)
        logging.info("Initializing server")
        settings.DATABASE.generate_mapping(create_tables=True)
        self.time = settings.TIMEOUT
        self.attempts = settings.ATTEMPTS

    @db_session
    def run(self):
        logging.info("Preparing scan's delegate class.")
        scanner = AuthScanner().withDelegate(ScanDelegate())
        logging.info("Initializing scan loop for {} times.".format(self.attempts))
        for x in range(self.attempts):
            try:
                logging.info("Starting scan #{}".format(x))
                scanner.scan(timeout=self.time)
                logging.info("Ending scan #{}".format(x))
            except Exception as e:
                logging.error("Scan #{}, some error occured: {}".format(x,e))
        logging.info("Closing server...")