import json
import gpshublib

d = gpshublib.DeviceHardwareList()
print(d.getList())

for a in d.getList():
	print(a)
	print(json.dumps(a.get(), indent=4))




d._automount_uuids.append('2CBA-17F1')
d.udev_listner()
