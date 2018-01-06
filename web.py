from flask import request, render_template
from pony import orm
from flask import Flask
import flask.ext.restful as rest

from core.models import Device, Transmission
from core.settings import DATABASE as db, FLASK_DEBUG

app = Flask(__name__, template_folder='core/templates')
app.static_folder = 'core/static'
api = rest.Api(app)
db.generate_mapping(create_tables=True)

class APIWhitelist(rest.Resource):

    def get(self):
        with orm.db_session:
            return {
                dev.id: {
                    'name': dev.name
                } for dev in Device.select()
            }

    def post(self):
        with orm.db_session:
            data = request.get_json(force=True)
            if data['id'] and data['name']:
                Device(id=data['id'].upper(), name=data['name'])
                return {}, 200
        return {}, 400

    def delete(self, id):
        with orm.db_session:
            dev = Device.select(lambda d: d.id.upper() == id).first()
            if dev:
                dev.delete()
                return {}, 200
            return {}, 404


class APITransmission(rest.Resource):

    def get(self):
        with orm.db_session:
            return {
                tr.id: {
                    'device_id': tr.device.id if tr.device else None,
                    'time': tr.time,
                    'raw_data': tr.packet.payload,
                    'txPower': tr.txPower,
                    'rssi': tr.rssi
                } for tr in Transmission.select()
            }

@app.route('/', methods=["POST", "GET"])
def index():
    errors = None
    msg = None
    with orm.db_session:
        result = list(Device.select())
        if request.method == 'POST':
            mac = request.form['mac']
            if mac is None or len(mac) == 0:
                errors = "Invalid MAC address!"
                return render_template('index.html', result=result, errors=errors, msg=msg)
            name = request.form['name']
            if name is None or len(mac) == 0:
                dev = Device.select(lambda d: d.id == mac).first()
            else:
                dev = Device.select(lambda d: d.id == mac or d.name == name).first()
            if dev is not None:
                errors = "Device with this parameters already exists!"
                return render_template('index.html', result=result, errors=errors, msg=msg)
            else:
                dev = Device(name=name, id=mac.upper())
                result.append(dev)
                msg = "Device has been added!"
                return render_template('index.html', result=result, errors=errors, msg=msg)
        return render_template('index.html' , result=result, errors=errors, msg=msg)


@app.route('/transmission')
def transmission():
    with orm.db_session:
        result = list(Transmission.select())
        return render_template('transmission.html', result=result)

api.add_resource(APIWhitelist, '/api/whitelist', '/api/whitelist/<id>', endpoint='Whitelist')
api.add_resource(APITransmission, '/api/transmission', endpoint='Transmissions')


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)