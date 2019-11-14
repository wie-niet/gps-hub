from flask import Flask, jsonify, make_response
import gpshublib

# Creating Flask application
app = Flask(__name__)
app.debug = True


#
# API /user
#

gps_hw_view = gpshublib.DeviceHardwareRestApi.as_view('gps_hw_api')
app.add_url_rule('/gps_hw/', defaults={'id': None}, view_func=gps_hw_view, methods=['GET',])
app.add_url_rule('/gps_hw/', view_func=gps_hw_view, methods=['POST',])
app.add_url_rule('/gps_hw/<id>', view_func=gps_hw_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])



if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    
