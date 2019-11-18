from flask.views import MethodView
from flask import make_response, jsonify, request, abort
import json

# from orator.exceptions.query import QueryException

#
# from https://flask.palletsprojects.com/en/1.1.x/views/#method-views-for-apis
#

#
# HTTP status codes: https://restfulapi.net/http-status-codes/
#

class ApiItem(object):
	def to_dict(self):
		'''Likely you need to replace this method.'''
		return(self.__dict__)

	def to_json(self, *args, **kwargs):
		'''json dumps this object.

		it calls self.to_dict() to get all attributes.
		replace the to_dict(self) method in your own class.
		'''
		return(json.dumps(self.get(), *args, **kwargs))


class ApiList(object):
	def to_list(self):
		# empty list
		result = []
		
		# itterate over our items items 
		for item in self.get():
			# get item as dict.
			result.append(item.get())
			
		return(result)

	def to_json(self,  *args, **kwargs):
		'''json dumps this object.

		it calls self.to_list() to get all attributes.
		replace the to_dict(self) method in your own class.
		'''
		return(json.dumps(self.to_list(),  *args, **kwargs))


class RestApi(MethodView):
	read_only_attributes = []
	write_only_attributes = []
	
	need_auth = bool(False)
	need_validation = bool(False)
	need_defaults = bool(False)
	
		

	def get_http_auth(self):
		# if need_auth: read token or fail 401
		
		# check if we need it.
		if not self.need_auth:
			return None
		
		# we need auth, get auth or fail 401:.
		if 'Authorization' in request.headers:
			auth = request.headers.get('Authorization')
			
			# TODO: is auth valid (authenticate auth or validate jwt)
			print("FOUND: Auth (not implemented)", auth)
			# return(auth)
			return(None)
		else:
			error = {'error': 'authorization headers are missing'}
			self.response(error, 401)
			# return make_response(self.make_json(error), 401)

			
			
	
	def has_access(self, auth, method, model=None):
		# auth : { userid: ?? }
		# method :  GET/PUT/POST/DELETE/PATCH
		# model : this item 
		# TODO: implement permision checks && aborts
		pass
	
	def is_valid(self, model):
		# match with self.json_schema
		if self.need_validation:
			self.validator(model)
		
	def validator(self, model):
		'''implement an validation checks && aborts, don't forget to set need_validation''' 
		pass
		
		
	def _call_set_defaults(self, model):
		# call set defaults
		if self.need_defaults:
			self.set_defaults(model)
		
	def set_defaults(self, model):
		'''implement an set_defaults to add defaults to the model, don't forget to set need_defaults'''
		pass
		
	def enforce_write_only(self, data):
		'''remove write-only attributes from data, and return new object'''
		result = {}
		
		for key in data:
			if key not in self.write_only_attributes:
				result[key] = data[key]
		
		return(result)
			
	def enforce_read_only(self, old, new):
		'''raise error if any of the read-only attributes are changed in new compared with old.'''		
		for key in self.read_only_attributes:
			if (old[key] != new[key]):
				# read-only attribute is changed	
				error = {'error': 'cannot change read-only attribute.', 'path': key}
				self.response(error, 409)
		return(result)
			

	#
	# Datalayer methods 
	#
		
	def db_create(self, item):
		# create in data layer
		raise NotImplementedError('implement db_create in your own class')

	def db_update(self,id,item):
		# save/update in data layer
		raise NotImplementedError('implement db_update in your own class')

	def db_find_one(self, id):
		# find 1 in data layer
		raise NotImplementedError('implement db_find_one in your own class')

	def db_list(self):
		# get list from data layer
		raise NotImplementedError('implement db_list in your own class')

	def db_delete(self, id):
		# delete from data layer
		raise NotImplementedError('implement db_delete in your own class')
	   
	#
	# helper functions
	# 
	def make_json(self, object):
		'''
		Orator models and collections are not serializable
		but do have .to_json methods we can use.
		
		use .to_json() method  if exists.
		othwerwise we use jsonify()
		'''
		# use .to_json if exists:
		if hasattr(object, 'to_json'):
			return(object.to_json(indent=4))
	
		else:
			# use jsonify 
			return(jsonify(object))
			
			
	def response(self, object, code=200):
		# short cut for :
		abort(make_response(self.make_json(object), code))
		
	
	#
	# HTTP methods:
	#
	
	def get_list(self):
		'''GET  : Read collection'''
		
		# get auth header (if needed)
		auth = self.get_http_auth()
		
		# check permision (if needed)
		self.has_access(auth, 'GET')
		
		# get item from data layer
		data = self.db_list()

		# serialize json, http 200
		self.response(data, 200)

	def get_item(self, id):
		'''GET  : Read single item'''
		
		# get auth header (if needed)
		auth = self.get_http_auth()
		
		# check permision (if needed)
		self.has_access(auth, 'GET')
		
		# get item from data layer
		data = self.db_find_one(id)

		# 404 not found 
		if data is None:
			error = {'error': 'not found'}
			self.response(error, 404)

		# check permision for this item (if needed)
		self.has_access(auth, 'GET', data)
		
		# enforce write-only permisions
		result = self.enforce_write_only(data)
		
		# serialize json, http 200
		self.response(result, 200)

	def get(self, id):
		if id is None:
			return self.get_list()
		else:
			return self.get_item(id)
			
		
	def post(self):
		'''POST : Create single item'''
		# get auth header (if needed)
		auth = self.get_http_auth()
		
		# check permision (if needed)
		self.has_access(auth, 'GET')
		
		# get POST data from HTTP request
		new_item = request.get_json()
				
		# add defaults if needed
		self._call_set_defaults(new_item)

		# check validation (if needed)
		self.is_valid(new_item)
			
		# do we have permision to create THIS item here
		self.has_access(auth, 'POST', new_item)
		
		# create item in db layer 
		try:
			item = self.db_create(new_item)

		except Exception as e:
			error = {'error': 'db error'}
			print(error,  str(e))
			self.response(error, 500)


		# enforce write-only permisions for response
		result = self.enforce_write_only(item)
				
		# serialize json, http 200
		self.response(result, 200)
		

	def put(self, id):
		'''PUT  : Update single item'''
		# get auth header (if needed)
		auth = self.get_http_auth()
		
		# check permision (if needed)
		# self.has_access(auth, 'PUT')
		
		# get POST data from HTTP request
		new_item = request.get_json()

		# add defaults if needed
		self._call_set_defaults(new_item)

		# check validation (if needed)
		self.is_valid(new_item)
				
		# check permision to update this item (if needed)
		self.has_access(auth, 'PUT', new_item)

		# get item from data layer
		old_item = self.db_find_one(id)

		# 404 not found
		if old_item is None:
			 error = {'error': 'not found'}
			 self.response(error, 404)

		# # check permision to update this item (if needed)
		# self.has_access(auth, 'PUT', old_item)

		# enforce read-only attributes
		self.enforce_read_only(old_item, new_item)

		# update item in db layer 
		try:
			item = self.db_update(id, new_item)
		except Exception as e:
			error = {'error': 'db error'}
			print(error,  str(e))
			self.response(error, 500)

		# enforce write-only permisions for response
		result = self.enforce_write_only(item)
			
		# serialize json, http 200
		self.response(result, 201)


	def delete(self, id):
		'''DELETE : Delete single item'''
		# get auth header (if needed)
		auth = self.get_http_auth()
		
		# check permision (if needed)
		self.has_access(auth, 'DELETE')
		
		try:
			result = self.db_delete(id)

				
		except Exception as e:
			error = {'error': 'db error'}
			print(error,  str(e))
			self.response(error, 500)

		# not found:
		if result is 0:
			error = {'error': 'not found'}
			print (404)
			self.response(error, 404)
			
		# serialize json, http 204
		self.response(None, 204)
		

	def patch(self, id):
		'''PATCH : update single item using jsonpatch'''
		return('Patch not implemented..')

