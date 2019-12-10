from os import listdir
from os.path import isfile, join

from rest_api_flask import RestApi, ApiItem, ApiList, request
from rest_api_jsonschema import JsonSchemaForRestApi


class GpxFile(ApiItem):
	def __init__(self, filename):
		self.id = filename

		


#
# RestApi 
#
class GpxFilesRestApi( JsonSchemaForRestApi, RestApi):
	__ds = {}
	
	def __init__(self, dev_hw_list=None,conf_list=None ):
		
		# set DeviceHardwareList
		# if dev_hw_list is None:
		# 	self.__ds['dev_hw_list'] = DeviceHardwareList()
		self.__ds['dev_hw_list'] = dev_hw_list
			
		# set DeviceConfigList
		# if conf_list is None:
		# 	self.__ds['conf_list'] = GpsConfigCollection()
		self.__ds['conf_list'] = conf_list

		
		

	def magic_parse_route(self, **kwargs):
		## ROUTE : /gps/<string:gps_id>/files/<string:id> 
		self.gps_id = kwargs.get('gps_id')
		


	def get_gpx_path(self):
		gps_id = self.gps_id
		
		# get GPS config dict
		gps_conf = self.__ds['conf_list'].first(gps_id)

		# get gpshublib.DeviceHardware object (for is_mounted) 
		gps_hw = self.__ds['dev_hw_list'].find(gps_id)
		
		# check if gps device is mounted
		if not gps_hw.sys_is_mounted:
			error = {'error': 'GPS Device not mounted'}
			self.response(error, 404)
		
		# return gpx_path
		return(join(gps_hw.sys_is_mountpoint, gps_conf['gpx_dir']))
		

	def db_find_one(self, filename):
		# find 1 in data layer
		gpx_path = self.get_gpx_path()

		# test if it's a file
		if not isfile(join(gpx_path, filename)):
			error = {'error': 'GPX file not found.'}
			self.response(error, 404)
		
		# get all GPX File ApiItem 
		gpx_file = GpxFile(filename)
		
		# return item
		return(gpx_file)
		

	def db_list(self):
		# get list from data layer
		gpx_path = self.get_gpx_path()
		
		# list of filenames
		onlyfiles = [f for f in listdir(gpx_path) if isfile(join(gpx_path, f))]
		
		data = []
		for filename in onlyfiles:
			data.append(self.GpxFile(filename))
		
		
		return(data)
		
		
	def db_delete(self, id):
		# delete from data layer
		raise NotImplementedError('implement db_delete in your own class')

