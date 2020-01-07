import { Component, OnInit } from '@angular/core';

import { DataService } from '../../core/data.service';

import { iDeviceHardware } from '../../shared/interfaces'

@Component({
  selector: 'app-device-hardware-list',
  templateUrl: './device-hardware-list.component.html',
  styleUrls: ['./device-hardware-list.component.css']
})
export class DeviceHardwareListComponent implements OnInit {
  device_hardware_list: iDeviceHardware[]
  api_wait: boolean = true;
  
  constructor(private dataService: DataService) {}
 
  ngOnInit() {
    this.load()
    // this.dataService.getDeviceHardwareList()
    // .subscribe((jsondata: iDeviceHardware[]) => this.device_hardware_list = jsondata);

    // let id = 'SDV-98A'
    // this.device_hardware_list = [
    //   { ID_FS_UUID: id, sys_is_mounted: false, sys_is_connected: true, sys_dev_path: '/dev/disk-by-uuid/' + id, sys_mountpoint: '/media/gpshub-' + id }
    // ]

    // id = 'HS8-21Q'
    // this.device_hardware_list.push({ ID_FS_UUID: id, sys_is_mounted: true, sys_is_connected: true, sys_dev_path: '/dev/disk-by-uuid/' + id, sys_mountpoint: '/media/gpshub-' + id })

    // id = 'AH8-AB1'
    // this.device_hardware_list.push({ ID_FS_UUID: id, sys_is_mounted: false, sys_is_connected: true, sys_dev_path: '/dev/disk-by-uuid/' + id, sys_mountpoint: '/media/gpshub-' + id })
  }

  load() {
    this.api_wait = true
    this.dataService.getDeviceHardwareList()
    .subscribe((jsondata: iDeviceHardware[]) => {
      this.device_hardware_list = jsondata;
      this.api_wait = false;
    });

  }

  refresh() {
    this.api_wait = true
    this.dataService.getDeviceHardwareList(true)
    .subscribe((jsondata: iDeviceHardware[]) => {
      this.device_hardware_list = jsondata;
      this.api_wait = false;
    });
  }
}
