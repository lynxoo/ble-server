from flask import Flask
from pony import orm

from core.models import Device, Packet, Transmission
from core.settings import DATABASE as db

app = Flask(__name__)
db.generate_mapping(create_tables=True)

@app.route('/')
def index():
    return 'Ble-WEB-Server'

@app.route('/whitelist')
def whitelist():
    with orm.db_session:
        return '<br>'.join([str(dev) for dev in Device.select()])

@app.route('/transmission')
def transmission():
    with orm.db_session:
        return '<br>'.join([str(dat) for dat in Transmission.select()])

