import os
import stat
import sh
import pyudev

class DeviceHardware:
	''' device hardware '''
	ID_FS_UUID = None

	def __init__(self, ID_FS_UUID):
		self.ID_FS_UUID = ID_FS_UUID

	def get(self):
		list = {}

		#list = self.read_udev_list() # no argument for all udev entries.
		list = self.read_udev_list([
            'ID_FS_LABEL', 'ID_MODEL', 'ID_VENDOR', 'ID_FS_TYPE',
            'ID_FS_USAGE', 'ID_FS_VERSION', 'ID_SERIAL_SHORT'
            ])

		list['ID_FS_UUID'] = self.ID_FS_UUID
		list['sys_is_mounted'] = self.get_sys_is_mounted()
		list['sys_is_connected'] = self.get_sys_is_connected()
		list['sys_mountpoint'] = self.get_sys_mountpoint()
		list['sys_dev_path'] = self.get_sys_dev_path()

		return(list)

	def read_udev_list(self, filter_keys=None):
		context = pyudev.Context()
		for device in context.list_devices(subsystem='block', ID_FS_UUID=self.ID_FS_UUID):
			list = {}

			# either use filter_keys or all keys in device
			if filter_keys is None:
				filter_keys = device.keys()

			for k in filter_keys:
				list[k] = device.get(k)

			return(list)
		## nothing found:
		list = {}
		list['ID_FS_UUID'] = self.ID_FS_UUID
		list['sys_is_mounted'] = 0
		list['sys_is_connected'] = 0
		return(list)
			
	def get_sys_mountpoint(self):
		mnt_base = '/media/gpshub-'
		return(mnt_base + str(self.ID_FS_UUID))

	def get_sys_dev_path(self):
		return('/dev/disk/by-uuid/' + str(self.ID_FS_UUID))

	def get_sys_is_connected(self):
		"""is the device connected, does the dev point exist"""
		try:
			return stat.S_ISBLK(os.stat(os.path.realpath(self.get_sys_dev_path())).st_mode)
		except:
			return False

	def get_sys_is_mounted(self):
		"""is the device mounted"""
		mount_point = self.get_sys_mountpoint()
		return(os.path.ismount(mount_point))

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

	def set_sys_is_mounted(self, sys_is_mounted):
		if(sys_is_mounted == True and self.get_sys_is_mounted() == False):
			self.exec_mount()
		if(sys_is_mounted == False and self.get_sys_is_mounted() == True):
			self.exec_umount()
		# the rest we silently ignore..
		return(self)

	def exec_mount(self):
		"""mount the device and make mountpoint dir /media/gpshub-.... """
		
		mount_point = self.get_sys_mountpoint()
		dev_path = self.get_sys_dev_path()

		if not os.path.isdir(mount_point):
			os.makedirs(mount_point) 
		sh.mount(dev_path, mount_point)

	def exec_umount(self):
		"""umount the device and remove mountpoint"""
		mount_point = self.get_sys_mountpoint()

		sh.umount(mount_point)
		os.rmdir(mount_point)

	
	
class DeviceHardwareList:
	_automount_uuids = []

	def getList(self):
		list = []
		context = pyudev.Context()
		for device in context.list_devices(subsystem='block', ID_BUS="usb" ):
			ID_FS_UUID = device.get('ID_FS_UUID')
			if ID_FS_UUID is not None: list.append(DeviceHardware(ID_FS_UUID))

		return(list)

	def __getitem__(self, ID_FS_UUID):
		return(DeviceHardware(ID_FS_UUID))


	#
	#  add|remove hardware events
	#
	def udev_device_event(self, action, ID_FS_UUID):
		print ("udev " + action + " event " + ID_FS_UUID)
		if action == "add":
			self.udev_device_event_add(ID_FS_UUID)
		if action == "remove":
			self.udev_device_event_remove(ID_FS_UUID)

		print(DeviceHardware(ID_FS_UUID).get())

	def udev_device_event_add(self, ID_FS_UUID):
		if ID_FS_UUID in self._automount_uuids:
			d = DeviceHardware(ID_FS_UUID)
			print ("event automount " + ID_FS_UUID)
			d.set_sys_is_mounted(1)

	def udev_device_event_remove(self, ID_FS_UUID):
		'''Auto umount when still mounted after hardware is detached.'''
		if ID_FS_UUID in self._automount_uuids:
			d = DeviceHardware(ID_FS_UUID)
			if d.get_sys_is_mounted():
				print ("event auto umount " + ID_FS_UUID)
				d.exec_umount()
				
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

