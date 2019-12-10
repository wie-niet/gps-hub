from flask import Flask, jsonify, make_response

import gpshublib
import toml_config_table
import gpx_files

# global data stores
ds = {}
ds['conf_list'] = toml_config_table.GpsConfigCollection()
ds['dev_hw_list'] = gpshublib.DeviceHardwareList()



# Creating Flask application
app = Flask(__name__)
app.debug = True

# set Cross Origin Resource Sharing 
from flask_cors import CORS
CORS(app)


#
# API /gps_dev_view
#
gps_dev_view = gpshublib.DeviceHardwareRestApi(dev_hw_list=ds['dev_hw_list']).as_view('gps_dev_api')
app.add_url_rule('/gps_dev/', defaults={'id': None}, view_func=gps_dev_view, methods=['GET',])
app.add_url_rule('/gps_dev/', view_func=gps_dev_view, methods=['POST',])
app.add_url_rule('/gps_dev/<id>', view_func=gps_dev_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])



#
# API /gps_hw
#
gps_conf_view = toml_config_table.DeviceConfigRestApi(conf_list=ds['conf_list']).as_view('gps_conf_api')
app.add_url_rule('/gps_conf/', defaults={'id': None}, view_func=gps_conf_view, methods=['GET',])
app.add_url_rule('/gps_conf/', view_func=gps_conf_view, methods=['POST',])
app.add_url_rule('/gps_conf/<id>', view_func=gps_conf_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])

#
# GPX files meta data /gps/<id>/files/
#
gpx_files_view = gpx_files.GpxFilesRestApi(ds=ds).as_view('gpx_files_api')
app.add_url_rule('/gps/<gps_id>/files/', defaults={'id': None}, view_func=gpx_files_view, methods=['GET',])
# app.add_url_rule('/gps/<gps_id>/files/', view_func=gpx_files_view, methods=['POST',])
app.add_url_rule('/gps/<gps_id>/files/<id>', view_func=gpx_files_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])

#
# GPX files meta data /gps/<id>/files_data/
#



if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    
