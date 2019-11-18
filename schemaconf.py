# from jsonschema import validate, ValidationError
import json
# import jsonschema

# let's put all our schemas in a dict
raw_json = {}

raw_json['gps_conf'] = '''{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://wie-niet.nl/gpshub/schema.gps_conf.json",
  "title": "GPS-HUB Device Configuration",
  "description": "Object for GPS Device Configuration.",
  "type": "object",
  "properties": {
      "id": {
          "description": "Primary Key to Device Hardware (created from ID_FS_UUID)",
          "type": "string"
      },
      "label": {
          "description": "client choosen name for the device.",
		  "default" : "...",
          "type": "string"
      },
      "gpx_dir": {
          "description": "path to GPX dir (relative to mount_point)",
		  "default" : "Garmin/GPX",
          "type": "string"
      },
      "gpx_dir_has_archive": {
          "description": "True if gpx_dir has an sub-directory what is used as archive folder.",
		  "default" : false,
          "type": "boolean"
      },
      "gpx_dir_archive": {
          "description": "path to archive dir , relative to mount_point",
		  "default" : "Garmin/GPX/Archive",
          "type": "string"
      },
      "gpx_dir_hidden_list": {
          "description": "List of hidden file names",
		  "default" : [],
	      "type": "array",
	      "contains": {
	        "type": "string"
	      }
      },
      "gpx_dir_readonly_list": {
          "description": "List of read-only file names",
		  "default" : [],
	      "type": "array",
	      "contains": {
	        "type": "string"
	      }
      },
      "auto_mount": {
		  "default" : false,
          "description": "Automaticly mount when detected.",
          "type": "boolean"
      }
  }, 
  "required": [ "id" ],
  "additionalProperties": false
}'''


#
# pyhonize the json schemas
#
json_schema = {}
for schema in raw_json:
	json_schema[schema] = json.loads(raw_json[schema])

#
# if __name__ == '__main__':
#
# 	schema = json.loads(json_schema)
# 	data = json.loads(json_data)
#
# 	try:
# 	    validate(instance=data, schema=schema)
# 	except ValidationError as e:
# 	    # catches only first error.
# 	    error = {}
# 	    error['type'] = 'validation'
# 	    # pointer '.' or path '/'
# 	    error['path'] = '.'.join(e.path)
# 	    error['message'] = e.message
#
# 	    print( '--------------------------------------' )
# 	    print( 'error: ', json.dumps(error, indent=3))
# 	    print( '--------------------------------------' )
#
# 	    #
# 	    # print('ValidationError:', e)
# 	    #
# 	    # print( '--------------------------------------' )
# 	    # print('==== validator:' , e.validator)
# 	    # print( '--------------------------------------' )
# 	    # print('==== relative_path:' , e.relative_path)
# 	    # print( '--------------------------------------' )
#
def set_defaults(model):
	# itterate over default values and check if attribute exist in model:
	for key, propertie in json_schema['gps_conf']['properties'].items():
		if 'default' in propertie:
			if key not in model: 
				# we have a missing attribute:
				print("debug: set missing key:", key, propertie['default'])
				model[key] = propertie['default']
