from os import listdir
from os.path import isfile, join
import os

from rest_api_flask import RestApi, ApiItem, ApiList, request
from rest_api_jsonschema import JsonSchemaForRestApi

# global data store
from data_store import data_store
import pendulum


class GpxFile(ApiItem):
	id = None
	__dir = None
	
	def __init__(self, filename, parent_dir):
		self.id = filename
		self.__dir = parent_dir

	def to_dict(self):
		self.stat()
		return(self.__dict__)
		data = {}
		data['id'] = self.id
		
		return(data)

	def get_path(self):
		return(join(self.__dir, self.id))
	
	def stat(self):
		st = os.stat(self.get_path())
		# self.raw_stat = os.stat(self.get_path())
		
		self.size_bytes = st.st_size
		self.time_created = pendulum.from_timestamp(st.st_ctime).to_iso8601_string() 
		self.time_changed = pendulum.from_timestamp(st.st_mtime).to_iso8601_string()
		self.time_accesed = pendulum.from_timestamp(st.st_atime).to_iso8601_string() 


#
# RestApi 
#
class GpxFilesRestApi( JsonSchemaForRestApi, RestApi):
	ds = None
	
	def __init__(self):
		self.ds = data_store()

		#  DeviceHardwareList
		# self.ds.dev_hw_list
			
		#  DeviceConfigList
		# self.ds.conf_list

		
		

	def magic_parse_route(self, **kwargs):
		## ROUTE : /gps/<string:gps_id>/files/<string:id> 
		self.gps_id = kwargs.get('gps_id')
				

	def get_gpx_path(self):
		gps_id = self.gps_id
		
		# get GPS config dict
		gps_conf = self.ds.conf_list.first(gps_id)

		# get gpshublib.DeviceHardware object (for is_mounted) 
		gps_hw = self.ds.dev_hw_list.find(gps_id)
		
		# check if gps device is mounted
		if not gps_hw.sys_is_mounted:
			error = {'error': 'GPS Device not mounted'}
			self.response(error, 404)
		
		# return gpx_path
		return(join(gps_hw.sys_mountpoint, gps_conf['gpx_dir']))
		

	def db_find_one(self, filename):
		# find 1 in data layer
		gpx_path = self.get_gpx_path()

		# test if it's a file
		if not isfile(join(gpx_path, filename)):
			error = {'error': 'GPX file not found.'}
			self.response(error, 404)
		
		# get all GPX File ApiItem 
		gpx_file = GpxFile(filename, gpx_path)
		
		# return item
		return(gpx_file)
		

	def db_list(self):
		print ("DEBUG ds:", self.ds)
		
		# get list from data layer
		gpx_path = self.get_gpx_path()
		
		# list of filenames
		onlyfiles = [f for f in listdir(gpx_path) if isfile(join(gpx_path, f))]
		
		data = []
		for filename in onlyfiles:
			data.append(GpxFile(filename, gpx_path))
		
		
		return(data)
		
		
	def db_delete(self, id):
		# delete from data layer
		raise NotImplementedError('implement db_delete in your own class')

