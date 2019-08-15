
"""Python module to interact with handheld GPS Devices connected as USB MassStorage device.
Initialy this module is created for the Garmin eTrex 30x."""

import os
import stat
import xml.etree.ElementTree as ET
import sh

class MassStorage:
	mount_point = None
	dev_path = None

	def __init__(self, mount_point="/media/USBDisk", dev_path="/dev/disk/by-label/USBDisk"):
		"""init GarminGpsMassStorage object based on the mount_point"""
		self.mount_point = mount_point
		self.dev_path = dev_path

	def isMounted(self):
		"""is the device mounted"""
		return(os.path.ismount(self.mount_point))

	def isDevExists(self):
		"""is the device connected, does the dev point exist"""
		try:
			return stat.S_ISBLK(os.stat(os.path.realpath(self.dev_path)).st_mode)
		except:
			return False


	def mount(self, dev_path=None, mount_point=None):
		"""mount the device"""
		if dev_path is not None:
			self.dev_path = dev_path

		if mount_point is not None:
			self.mount_point = mount_point 


		sh.mount(self.dev_path, self.mount_point)

	def umount(self):
		"""umount the device"""
		sh.umount(self.mount_point)

class GarminGpsMassStorage(MassStorage): 
	device = None

	def __init__(self, mount_point='/media/GARMIN',dev_path="/dev/disk/by-label/GARMIN"):
		"""init GarminGpsMassStorage object based on the mount_point"""
		MassStorage.mount_point = mount_point
		MassStorage.dev_path = dev_path 

		#if self.isMounted():
			#self.readGarminDeviceXml()

	def mount(self):
		super().mount()
		self.readGarminDeviceXml()
		
	def umount(self):
		super().umount()
		# simple way to clear device info
		self.device = None

	def getFolderPathByName(self, Name):
		# read gps config  from Device xml
		try:
			return os.path.join(self.mount_point, self.device['folderByName'][Name]['Path'])
		except:
			return False

	def getFolderExtensionByName(self, Name):
		# read gps config  from Device xml
		try:
			return self.device['folderByName'][Name]['FileExtension']
		except:
			return False

	
	def listdir(self, Name="UserDataSync"):
		""" List directory, default Name=UserDataSync"""
		dir_path = self.getFolderPathByName(Name)
		
		dir_entries = os.listdir(dir_path)

		# filter extension
		dir_entries = [ fi for fi in dir_entries if fi.lower().endswith('.' + self.getFolderExtensionByName(Name).lower()) ]

		return(dir_entries)

	def getTrackNameFromGPX(self, gpx_file, folderName=None):
		""" read GPX track name by gpx file name , optionaly relative to the "folderName"  """

		if folderName is not None:
			gpx_file = os.path.join(self.getFolderPathByName(folderName), gpx_file)


		try:
			tree = ET.parse(gpx_file)
			xml = tree.getroot()
			ns = {'gpx': '{http://www.topografix.com/GPX/1/1}'}
		
			#trackName = xml.find('gpx:trk/gpx:name', ns).text
			trackName = xml.find('{http://www.topografix.com/GPX/1/1}trk/{http://www.topografix.com/GPX/1/1}name', ns).text
		except:
			trackName = None
			


		return trackName


	def readGarminDeviceXml(self, device_xml="Garmin/GarminDevice.xml"):
		""" read Garmin/GarminDevice.xml """
		tree = ET.parse(os.path.join(self.mount_point,device_xml))
		xml = tree.getroot()
		ns = {'Garmin': 'http://www.garmin.com/xmlschemas/GarminDevice/v2'}

		self.device = {}
		d = self.device
		d['description'] = xml.find('Garmin:Model/Garmin:Description', ns).text
		d['softwareversion'] = xml.find('Garmin:Model/Garmin:SoftwareVersion', ns).text
		d['partnumber'] = xml.find('Garmin:Model/Garmin:PartNumber', ns).text


		#d['folders'] = []
		d['folderByName'] = {}
		for el in xml.find('Garmin:MassStorageMode', ns):
			folder = {}

			#folder['tag'] = el.tag 

			tag = el.find('Garmin:Name', ns)
			if tag is not None:
				folder['Name'] = tag.text
			
			tag = el.find('Garmin:File/Garmin:TransferDirection', ns)
			if tag is not None:
				folder['TransferDirection'] = tag.text

			tag = el.find('Garmin:File/Garmin:Location/Garmin:Path', ns)
			if tag is not None:
				folder['Path'] = tag.text

			tag = el.find('Garmin:File/Garmin:Location/Garmin:FileExtension', ns)
			if tag is not None:
				folder['FileExtension'] = tag.text

			tag = el.find('Garmin:File/Garmin:Location/Garmin:BaseName', ns)
			if tag is not None:
				folder['BaseName'] = tag.text

			if el.tag == '{http://www.garmin.com/xmlschemas/GarminDevice/v2}DataType':
				#d['folders'].append(folder)
				name = folder['Name']
				d['folderByName'][name] = folder

			#print el.tag, el.attrib, el.text

		return tree

		

		
