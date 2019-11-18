GPS-HUB:

# 
# api object overview
#


#### DeviceHardwareList
  - def get()
#### DeviceHardware
  - (str) id ( uniq id constructed of DeviceHardware.ID_FS_UUID)
  - (str) ID_FS_UUID 
  - (str) ID_MODEL
  - (str) ID_VENDOR
  - (str) ID_FS_TYPE
  - (str) ID_FS_USAGE
  - (str) ID_FS_VERSION
  - (str) ID_SERIAL_SHORT
  - (bool) sys_is_mounted = 1 / 0 
  - (str) sys_mountpoint = '/media/gpshub-$self.ID_FS_UUID'
  - (bool) sys_is_connected = 1 / 0
  - def get()
  - def update()  # only sys_is_mounted is writeable: 1 to mount and 0 to umount

#### DeviceConfigList
  - def get()
  - def add()
  
#### DeviceConfig
  - (str) id (foreign key DeviceHardware.id)
  - (str) name = "My readable name"
  - (str) gpx_dir = "/Garmin/GPX"  -   -   -   -   -   -   -  = find($sys_mountpoint, is_dir, iname='gpx')
  - (bool) gpx_dir_has_archive = 0/1  -   -   -   -   -   -    = find($gpx_dir, is_dir, name='Archive) && 1 || 0
  - (str) gpx_dir_archive = "/Garmin/GPX/Archive"  -   -   -  = find($gpx_dir, is_dir, name='Archive)
  - (list) gpx_dir_hidden_list = ['hiddenfile.gpx']  -   -   - = suspected hidden files.
  - (list) gpx_dir_readonly_list = ['current-location.gpx']  - = suspected readonly files.
  - (bool) auto_mount = 1/0 (using pyudev)
  - def get()
  - def delete()  - 
  - def update()  - 
  - 
#### GpxFileList
  - get()
  - add()  # upload file , if file_name exist add + "(1)". 
#### GpxFile
  - id = $file_name
  - file_name   
  - gpx_name
  - read_only = 1 / 0 
  - gpx_data_path
  - get()
  - delete()  - 
  - update()  - 

#### GpxFileBlob
  download or view gpx file over HTTP
  - id = $file_name
  - get() # ?download=1 to serve as attachment.
