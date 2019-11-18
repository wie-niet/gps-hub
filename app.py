from flask import Flask, jsonify, make_response

import gpshublib
import toml_config_table



# Creating Flask application
app = Flask(__name__)
app.debug = True

# set Cross Origin Resource Sharing 
from flask_cors import CORS
CORS(app)


#
# API /gps_dev_view
#
gps_dev_view = gpshublib.DeviceHardwareRestApi.as_view('gps_dev_api')
app.add_url_rule('/gps_dev/', defaults={'id': None}, view_func=gps_dev_view, methods=['GET',])
app.add_url_rule('/gps_dev/', view_func=gps_dev_view, methods=['POST',])
app.add_url_rule('/gps_dev/<id>', view_func=gps_dev_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])



#
# API /gps_hw
#
gps_conf_view = toml_config_table.DeviceHardwareRestApi.as_view('gps_conf_api')
app.add_url_rule('/gps_conf/', defaults={'id': None}, view_func=gps_conf_view, methods=['GET',])
app.add_url_rule('/gps_conf/', view_func=gps_conf_view, methods=['POST',])
app.add_url_rule('/gps_conf/<id>', view_func=gps_conf_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    
