from os import listdir
from os.path import isfile, isdir,  join
import os

from rest_api_flask import RestApi, ApiItem, ApiList, request
from rest_api_jsonschema import JsonSchemaForRestApi

# global data store
from data_store import data_store
import pendulum


class GpxFile(ApiItem):
	id = None
	path = None
	dir_tag = None
	gps_id = None
	
	def __init__(self, filename, path=None, dir_tag=None, gps_id=None):
		self.id = filename
		self.path = path 
		self.__dict__['dir_tag'] = dir_tag
		self.gps_id = gps_id

		# init all values.
		self.stat()

	def to_dict(self):
		return(self.__dict__)
		# data = {}
		# data['id'] = self.id
		#
		# return(data)

	def get_path(self):
		return(join(self.path, self.id))
	
	def stat(self):
		st = os.stat(self.get_path())
		# self.raw_stat = os.stat(self.get_path())
		
		self.size_bytes = st.st_size
		self.time_created = pendulum.from_timestamp(st.st_ctime).to_iso8601_string() 
		self.time_changed = pendulum.from_timestamp(st.st_mtime).to_iso8601_string()
		self.time_accesed = pendulum.from_timestamp(st.st_atime).to_iso8601_string() 

	@property
	def dir_tag(self):
		return(self.__dict__['dir_tag'])
	
	@dir_tag.setter
	def dir_tag(self,dir_tag):	
		print ("DEBUG: update dir_tag {} -> {}".format(self.dir_tag, dir_tag))
		
		dest_path = self.get_path_by_dir_tag(dir_tag)
		
		os.rename(join(self.path, self.id), join(dest_path, self.id))
		
		self.__dict__['dir_tag'] = dir_tag
		self.__dict__['path'] = dest_path
		#THOUGHTS: 
		# 1. maybe redirct to new URL (niet zo ..)| or 
		# 2. redisign API -> folder/?dir_tag=gpx_archive|gpx (beter idee voor client integratie.)
		# 3. spectial response for "DELETED succesful "  | "MOVED succesful" etc. events.
		

	def get_path_by_dir_tag(self, dir_tag):
		# get our container with objects
		ds = data_store()

		# get GPS config dict
		gps_conf = ds.conf_list.first(self.gps_id)

		# get gpshublib.DeviceHardware object (for is_mounted) 
		gps_hw = ds.dev_hw_list.find(self.gps_id)
				
		# return file path dir_tag: gpx_dir / gpx_dir_archive 
		if not gps_conf['has_' + dir_tag + '_dir' ]:
			# has_ + dir_tag == False 
			raise NotImplementedError('dir_tag Directory not set or set to false in config')
			
		return(join(gps_hw.sys_mountpoint, gps_conf[dir_tag + '_dir']))

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

		self.need_validation = True
		self.need_defaults = True
		self.need_enforce_read_only = True
		self.need_enforce_write_only = True
	
		# self.json_schema = json_schema['gps_conf']
		self._read_json_schema('schema.gpx_file.json')
		
		

	def magic_parse_route(self, **kwargs):
		## ROUTE : /gps/<string:gps_id>/files/<string:dir_tag><string:id> 
		self.gps_id = kwargs.get('gps_id')
		self.dir_tag = kwargs.get('dir_tag')
				

	def get_gpx_path(self):
		gps_id = self.gps_id
		dir_tag = self.dir_tag
		
		# get GPS config dict
		gps_conf = self.ds.conf_list.first(gps_id)

		# get gpshublib.DeviceHardware object (for is_mounted) 
		gps_hw = self.ds.dev_hw_list.find(gps_id)
		
		# check if gps device is mounted
		if not gps_hw.sys_is_mounted:
			error = {'error': 'GPS Device not mounted'}
			self.response(error, 404)
		
		# return file path dir_tag: gpx_dir / gpx_dir_archive 
		if not gps_conf['has_' + dir_tag + '_dir' ]:
			# has_ + dir_tag == False 
			error = {'error': 'Directory not set or set to false in config.'}
			self.response(error, 400)
			
		return(join(gps_hw.sys_mountpoint, gps_conf[dir_tag + '_dir']))
		

	def db_find_one(self, filename):
		# find 1 in data layer
		gpx_path = self.get_gpx_path()

		# test if it's a file
		if not isfile(join(gpx_path, filename)):
			error = {'error': 'GPX file not found.'}
			self.response(error, 404)
		
		# get all GPX File ApiItem 
		gpx_file = GpxFile(filename, gpx_path, self.dir_tag, self.gps_id)
		
		# return item
		return(gpx_file)
		

	def db_list(self):
		print ("DEBUG ds:", self.ds)
		
		# get list from data layer
		gpx_path = self.get_gpx_path()
		if not isdir(gpx_path):
			error = {'error': 'gpx_path Directory not found.'}
			self.response(error, 404)
		
		# list of filenames
		onlyfiles = [f for f in listdir(gpx_path) if isfile(join(gpx_path, f))]
		
		data = []
		for filename in onlyfiles:
			data.append(GpxFile(filename, gpx_path, self.dir_tag, self.gps_id))
		
		
		return(data)
	
	def db_update(self, id, new_item, old_item=None):
		
		if old_item is None:
			old_item = self.db_find_one(id)
		
		url_changed = False
		update_keys = []
		for x in new_item.keys():
			if getattr(old_item,x) != new_item[x]:
				# update varuable x 
				update_keys.append(x)
		
		for x in update_keys:
			print ("db_update: object.{} [ {} -> {} ]".format(x, getattr(old_item,x), new_item[x]))
			print ("db_update: object.{} [ {} -> {} ]".format(x, type(getattr(old_item,x)), type(new_item[x])))
			setattr(old_item,x, new_item[x])
			# with all changes the url path will change too:
			url_changed = True

		if url_changed:
			# gps/0aed834e-8c8f-412d-a276-a265dc676112/files/gpx_archive/iets.gpx
			 url_changed = '/gps/'+old_item.gps_id+'/files/'+old_item.dir_tag+'/'+old_item.id
	
		# return a fresh copy :
		# return self.db_find_one(id)

		self.response(old_item, 204)
		self.response(old_item, 201,  location=url_changed)
	
		
	def db_delete(self, id):
		# delete from data layer
		raise NotImplementedError('implement db_delete in your own class')

