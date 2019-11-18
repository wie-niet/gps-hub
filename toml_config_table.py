# import simplejson as json
import json
import toml
import os
import jsonpatch
from flask_rest_api import RestApi, ApiItem, ApiList, request

# from jsonschema import validate, ValidationError
from schemaconf import json_schema
# import json
# import jsonschema



class GpsConfigCollection(object):
	toml_file = 'gpsconfig.toml'
	toml_data = []
	model_name = 'gps-device-configs'
	primary_key = 'id'
	
	def __init__(self):
		self.file_read()
	
	def file_read(self):
		tdata = toml.load(self.toml_file)
		self.toml_data = tdata[self.model_name]
		
	def file_write(self):
		f = open(self.toml_file + '.tmp', "w")
		tdata = { self.model_name : self.toml_data }
		toml.dump(tdata, f)
		f.close()
		
		os.rename(self.toml_file + '.tmp', self.toml_file )
		# print("DEBUG: file_write")
		
	def all(self):
		return(self.toml_data)
		
	def first(self, value):
		key = self.primary_key
		
		for i in self.toml_data:
			if key in i:
				if i[key] == value:
					return i
	
	def append(self, item):
		self.toml_data.append(item)
		return(item)
	
	def destroy(self, value):
		'''remove item by id'''
		key = self.primary_key

		for i in self.toml_data:
			if key in i:
				if i[key] == value:
					self.toml_data.remove(i)
					# return 1 deleted
					return(1)
		# return 0 deleted
		return(0)

#
# RestApi 
#
class DeviceConfigRestApi(RestApi):
	# our Toml Config List
	__conf_list = None
	
		
	def __init__(self, conf_list=None):
		# set DeviceHardwareList
		if conf_list is None:
			conf_list = GpsConfigCollection()

		self.__conf_list = conf_list
		
		self.need_validation = True
		self.need_defaults = True
		self.json_schema = json_schema['gps_conf']
	
	# #
	# # validation methods
	# #
	# def validator(self, model):
	# 	print("debug: running validator...")
	# 	try:
	# 		validate(instance=model, schema=json_schema['gps_conf'])
	# 	except ValidationError as e:
	# 		# catches only first error.
	# 		error = {}
	# 		error['type'] = 'validation'
	# 		# pointer '.' or path '/'
	# 		error['path'] = '.'.join(e.path)
	# 		error['message'] = e.message
	#
	# 		print( '------validation-error:---------------' )
	# 		print( 'error: ', json.dumps(error, indent=3))
	# 		print( '--------------------------------------' )
	#
	# 		# HTTP response
	# 		self.response(error, 400)
	#
	# #
	# # set defaults
	# #
	# def set_defaults(self, model):
	# 	print("debug: running set_defaults...")
	# 	# itterate over default values and check if attribute exist in model:
	# 	for key, propertie in json_schema['gps_conf']['properties'].items():
	# 		if 'default' in propertie:
	# 			if key not in model:
	# 				# we have a missing attribute:
	# 				print("debug: set missing key:", key, propertie['default'])
	# 				model[key] = propertie['default']
	#


	#
	# Datalayer methods 
	#
		
	def db_create(self, item):
		# create in data layer
		if 'id' not in item.keys():
			raise Exception('id missing')
		
		# add and save
		item = self.__conf_list.append(item)
		self.__conf_list.file_write()
		
		# return new created item
		return(item)
		
		
	def db_update(self,id,n_data):
		# save/update in data layer
		data = self.__conf_list.first(id)

		# print()
		# print("DEBUG:", type(request.get_json()), request.get_json())
		for k in n_data.keys():
			data[k] = n_data[k]

		for k in [x for x in data.keys() if x not in n_data.keys()]:
			del(data[k])

		# make sure id isn't changed:
		id_name = self.__conf_list.primary_key
		data[id_name] = id
		
		#save changes
		self.__conf_list.file_write()
		
		# return new item
		return (data)
		

	def db_find_one(self, id):
		# find 1 in data layer
		return(self.__conf_list.first(id))

	def db_list(self):
		# get list from data layer
		
		# implement our special "refresh=true" url argument
		refresh = request.args.get('refresh', default=False)
		if refresh:
			self.__conf_list.file_read()

		# return list
		return(self.__conf_list.all())

	def db_delete(self, id):
		# delete from data layer
		count = self.__conf_list.destroy(id)
		# save changes to file
		self.__conf_list.file_write()
		return(count)
		


	#
	# HTTP Patch
	#
	def patch(id):
		# get current data from db
		data = self.__conf_list.first(id)
		if not data:
			error = {'error': 'not found'}
			self.response(error, 404)
	
		try:		
			# patch to apply 
			patch = jsonpatch.JsonPatch(request.get_json())
			# apply patch , inplace=True  
			patch.apply(data, True)
		
		except Exception as e:
			data = {'error': str(e)}
			self.response(data, 400)
	

		# print("DEBUG:", type(request.get_json()), request.get_json())
		# new_data = patch.appply(data)
		# for k in new_data.keys():
		#	 data[k] = new_data[k]
		#
		# for k in [x for x in data.keys() if x not in new_data.keys()]:
		#	 del(data[k])

		# make sure id isn't changed:
		data['id'] = id
	
		# write changes
		self.__conf_list.file_write()
	
		# HTTP response
		self.response(data, 200)
	

