import os
import stat
import sh
import pyudev
from flask_rest_api import RestApi
import json

class DeviceHardware:
	''' device hardware '''
	ID_FS_UUID = None
	
	def __init__(self, ID_FS_UUID):
		self.ID_FS_UUID = ID_FS_UUID

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def get(self):
		data = {}

		#data = self.read_udev_list() # no argument for all udev entries.
		data = self.read_udev_list([
			'ID_FS_LABEL', 'ID_MODEL', 'ID_VENDOR', 'ID_FS_TYPE',
			'ID_FS_USAGE', 'ID_FS_VERSION', 'ID_SERIAL_SHORT'
			])

		data['ID_FS_UUID'] = self.ID_FS_UUID
		data['sys_is_mounted'] = self.sys_is_mounted
		data['sys_is_connected'] = self.sys_is_connected
		data['sys_mountpoint'] = self.sys_mountpoint
		data['sys_dev_path'] = self.sys_dev_path

		return(data)
		
	def to_json(self, *args, **kwargs):
		return(json.dumps(self.get(), *args, **kwargs))

	def read_udev_list(self, filter_keys=None):
		context = pyudev.Context()
		for device in context.list_devices(subsystem='block', ID_FS_UUID=self.ID_FS_UUID):
			data = {}

			# either use filter_keys or all keys in device
			if filter_keys is None:
				filter_keys = device.keys()

			for k in filter_keys:
				data[k] = device.get(k)

			return(data)

		# nothing found, return empty list:
		return({})

	@property
	def sys_mountpoint(self):
		'''get moutpoint, constructed as '/media/gpshub-' + self.ID_FS_UUID '''
		return('/media/gpshub-' + str(self.ID_FS_UUID))

	@property
	def sys_dev_path(self):
		'''get  /dev/disk/by-uuid/ + self.ID_FS_UUID '''
		return('/dev/disk/by-uuid/' + str(self.ID_FS_UUID))

	@property
	def sys_is_connected(self):
		'''is the device connected, does the dev point exist'''
		try:
			return stat.S_ISBLK(os.stat(os.path.realpath(self.sys_dev_path)).st_mode)
		except:
			return False

	@property
	def sys_is_mounted(self):
		'''is the device mounted'''
		mount_point = self.sys_mountpoint
		return(os.path.ismount(mount_point))

	@sys_is_mounted.setter
	def sys_is_mounted(self, sys_is_mounted):
		'''set the device mounted status
		
		sys_is_mounted = True(mount) / False(umount)
			
		'''
		if(sys_is_mounted == True and self.sys_is_mounted == False):
			self.exec_mount()
		if(sys_is_mounted == False and self.sys_is_mounted == True):
			self.exec_umount()
		# the rest we silently ignore..
		return(self)

	def exec_mount(self):
		'''mount the device and make mountpoint dir /media/gpshub-.... '''

		mount_point = self.sys_mountpoint
		dev_path = self.sys_dev_path

		if not os.path.isdir(mount_point):
			os.makedirs(mount_point)
		sh.mount(dev_path, mount_point)

	def exec_umount(self):
		'''umount the device and remove mountpoint. '''
		mount_point = self.sys_mountpoint

		sh.umount(mount_point)
		os.rmdir(mount_point)



class DeviceHardwareList():
	# tmp solution, should be in config
	_automount_uuids = []

	def get(self):
		data = []
		context = pyudev.Context()
		for device in context.list_devices(subsystem='block', ID_BUS="usb"):
			ID_FS_UUID = device.get('ID_FS_UUID')
			if ID_FS_UUID is not None: data.append(DeviceHardware(ID_FS_UUID))

		return(data)
	
	def to_json(self,  *args, **kwargs):
		# empty list
		result = []
		
		# itterate over DeviceHardware items 
		for item in self.get():
			# get item as dict.
			result.append(item.get())
			
		return(json.dumps(result,  *args, **kwargs))	
		

	def find(self, ID_FS_UUID):
		return(DeviceHardware(ID_FS_UUID))


	#
	#  add|remove hardware events
	#
	def udev_device_event(self, action, ID_FS_UUID):
		print("udev " + action + " event " + ID_FS_UUID)
		if action == "add":
			self.udev_device_event_add(ID_FS_UUID)
		if action == "remove":
			self.udev_device_event_remove(ID_FS_UUID)

		print(DeviceHardware(ID_FS_UUID).get())

	def udev_device_event_add(self, ID_FS_UUID):
		if ID_FS_UUID in self._automount_uuids:
			dev_hw = DeviceHardware(ID_FS_UUID)
			print("event automount " + ID_FS_UUID)
			dev_hw.sys_is_mounted = 1

	def udev_device_event_remove(self, ID_FS_UUID):
		'''Auto umount when still mounted after hardware is detached.'''
		if ID_FS_UUID in self._automount_uuids:
			dev_hw = DeviceHardware(ID_FS_UUID)
			if dev_hw.sys_is_mounted:
				print("event auto umount " + ID_FS_UUID)
				dev_hw.exec_umount()

	def udev_listner(self):
		'''start blocking look while listning to for harwdware changes'''

		print('start monitor:')
		context = pyudev.Context()
		monitor = pyudev.Monitor.from_netlink(context)
		monitor.filter_by(subsystem='block')

		for device in iter(monitor.poll, None):
			ID_FS_UUID = device.get('ID_FS_UUID')
			#ID_BUS  = device.get('ID_BUS')
			#if ID_FS_UUID is not None and ID_BUS is "usb":
			if ID_FS_UUID is not None:
				self.udev_device_event(device.action, ID_FS_UUID)



from flask_rest_api import RestApi	
				
class DeviceHardwareRestApi(RestApi):
	def __init__(self, dev_hw_list=None):
		# set DeviceHardwareList
		if dev_hw_list is None:
			dev_hw_list = DeviceHardwareList()

		self.__dev_hw_list = dev_hw_list
	
	#
	# Datalayer methods for RestApi
	# 
	   
	# def db_create(self, item):
	#	 # create in data layer
	#	 raise NotImplementedError('implement db_create in your own class')

	def db_update(self,id,item):
		# save/update in data layer
		dev = DeviceHardware(ID_FS_UUID)
		# we only have to deal with sys_is_mounted
		dev.sys_is_mounted = item.sys_is_mounted
		# done here, no need to save anything.
		return(dev)

	def db_find_one(self, id):
		# find 1 in data layer
		return(DeviceHardware(id))
		
	def db_list(self):
		# get list from data layer
		return(self.__dev_hw_list)

	# def db_delete(self, id):
	#	 # delete from data layer
	#	 raise NotImplementedError('implement db_delete in your own class')
	   



class DeviceConfig:
	'''Config settings for an GPS device, with functions to read/update/delete'''
	# ID_FS_UUID = None
	#
	# def get(self):
	# 	data = {}
	# 	data.ID_FS_UUID = self.ID_FS_UUID
	# 	return(data)

class DeviceConfigList:
	'''List of all config settings in DeviceConfig objects. with functions to read/update/delete/create '''
	# def get(self):
	# 	''' get list of DeviceConfig objects '''
	# 	#TODO read config.
	# 	return([])
	#
	# def add(self, device_config):
	# 	''' add new DeviceConfig objects '''
	# 	#TODO: addd device_config to list
	# 	return(device_config)
