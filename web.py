from flask import Flask, json, request, render_template
from pony import orm
from flask import Flask
import flask.ext.restful as rest

from core.models import Device, Transmission
from core.settings import DATABASE as db, FLASK_DEBUG

app = Flask(__name__, template_folder='core/templates')
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
                Device(id=data['id'], name=data['name'])
                return {}, 200
        return {}, 400

class APITransmission(rest.Resource):

    def get(self):
        with orm.db_session:
            return {
                tr.id: {
                    'device_id': tr.device.id,
                    'time': tr.time,
                    'raw_data': tr.packet.payload,
                    'txPower': tr.txPower,
                    'rssi': tr.rssi
                } for tr in Transmission.select()
            }

@app.route('/')
def index():
    with orm.db_session:
        result = list(Device.select())
        return render_template('index.html' , result=result)


@app.route('/transmission')
def transmission():
    with orm.db_session:
        result = list(Transmission.select())
        return render_template('transmission.html', result=result)

api.add_resource(APIWhitelist, '/api/whitelist', endpoint='Whitelist')
api.add_resource(APITransmission, '/api/transmission', endpoint='Transmissions')


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)