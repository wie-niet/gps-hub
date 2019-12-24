from flask import Flask, jsonify, make_response, request

from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
from os.path import isfile, join

import gpshublib
import toml_config_table
import gpx_files

from data_store import data_store as ds

# global data store
ds = ds()
ds.conf_list = toml_config_table.GpsConfigCollection()
ds.dev_hw_list = gpshublib.DeviceHardwareList()



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
gps_conf_view = toml_config_table.DeviceConfigRestApi.as_view('gps_conf_api')
app.add_url_rule('/gps_conf/', defaults={'id': None}, view_func=gps_conf_view, methods=['GET',])
app.add_url_rule('/gps_conf/', view_func=gps_conf_view, methods=['POST',])
app.add_url_rule('/gps_conf/<id>', view_func=gps_conf_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])

#
# GPX files meta data /gps/<id>/files/
#
gpx_files_view = gpx_files.GpxFilesRestApi.as_view('gpx_files_api')
app.add_url_rule('/gps/<gps_id>/files/', defaults={'id': None}, view_func=gpx_files_view, methods=['GET',])
app.add_url_rule('/gps/<gps_id>/files/<id>', view_func=gpx_files_view, methods=['GET', 'PUT', 'DELETE', 'PATCH'])

#
# GPX files upload/download data /gps/<gps_id>/files_data/
#
@app.route('/gps/<gps_id>/files_data/', methods=['POST'])
def upload_file(gps_id):
	print( "upload file ")
	
	# print(request.files)
	# check if the post request has the file part
	if 'file' not in request.files:
		error = '{ "error": "no file in request" }'
		return(make_response(error, 400, {'Content-Type': 'application/json'}))

	file = request.files['file']
	if file.filename == '':
		error = '{ "error": "no selected [file]" }'
		return(make_response(error, 400, {'Content-Type': 'application/json'}))

	filename = secure_filename(file.filename)

	# get location to store file:
	# get GPS config dict
	gps_conf = ds.conf_list.first(gps_id)

	# get gpshublib.DeviceHardware object (for is_mounted) 
	gps_hw = ds.dev_hw_list.find(gps_id)
	
	# check if gps device is mounted
	if not gps_hw.sys_is_mounted:
		error = '{ "error": "GPS Device not mounted" }'
		return(make_response(error, 400, {'Content-Type': 'application/json'}))
	
	# get gpx_path
	gpx_path = join(gps_hw.sys_mountpoint, gps_conf['gpx_dir'])
	
	
	# gps_dev.gpx_dir
	# TODO , check if already exist , create unique new name
	file.save(os.path.join(gpx_path, filename))

	data = '{ "status": "Succes" }'
	return(make_response(data, 200, {'Content-Type': 'application/json'}))
	# make_response(self.make_json(obj), code, {'Content-Type': 'application/json'}))

#
# GPX files download data /gps/<gps_id>/files_data/
#
@app.route('/gps/<gps_id>/files_data/<filename>', methods=['GET'])
def download_file(gps_id, filename):
	print( "download file ")
	# get GPS config dict
	gps_conf = ds.conf_list.first(gps_id)

	# get gpshublib.DeviceHardware object (for is_mounted) 
	gps_hw = ds.dev_hw_list.find(gps_id)
	
	# check if gps device is mounted
	if not gps_hw.sys_is_mounted:
		error = '{ "error": "GPS Device not mounted" }'
		return(make_response(error, 400, {'Content-Type': 'application/json'}))
	
	# get gpx_path
	gpx_path = join(gps_hw.sys_mountpoint, gps_conf['gpx_dir'])
	
	# is the download=1 argument set
	# if request.args.get('download').lower() in ("yes", "true", "1", "on"):
	# 	is_download = True
	# else:
	# 	is_download = False
	#
	# is the download=1 argument set
	is_download = True if request.args.get('download', '').lower() in ('yes', 'true', '1', 'on') else False
	
	return send_from_directory(directory=gpx_path, filename=filename, as_attachment=is_download, mimetype='application/gpx+xml')



@app.route('/api/ping', methods=['GET'])
def api_ping():
		return(make_response('{ "status": true }', 200, {'Content-Type': 'application/json'}))


if __name__ == '__main__':
	app.run(host= '0.0.0.0')
	
