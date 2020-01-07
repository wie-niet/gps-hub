import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { iDeviceHardware, iDeviceConfig } from '../shared/interfaces';

import { DataService } from '../core/data.service';


@Component({
  selector: 'app-device-hardware',
  templateUrl: './device-hardware.component.html',
  styleUrls: ['./device-hardware.component.css']
})
export class DeviceHardwareComponent implements OnInit {
  id :string;
  device_hardware: iDeviceHardware|null;
  device_config: iDeviceConfig|null;
  api_wait: boolean = false;
  error: any;

  private DeviceHardwareObserver = {
    next: jsondata => this.device_hardware = jsondata,
    error: (err) => {
      this.error = err ;
      console.log(err);
      this.api_wait = false;
	},
    complete:  () => {
      this.api_wait = false;
      this.error = null;

    }
  };
  
  constructor(private route: ActivatedRoute , private dataService: DataService) { }


  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
	this.load()
    // this.api_wait = true
    // this.dataService.getDeviceHardware(this.id)
    // .subscribe(this.DeviceHardwareObserver);


    // this.dataService.getDeviceHardware(id)
    // .subscribe((jsondata: iDeviceHardware) => this.device_hardware = jsondata);
    // .subscribe((jsondata: iDeviceHardware) => this.device_hardware = new DeviceHardwareData(jsondata));

    // // use service to get data, for now just written something down here
    // this.device_hardware = { ID_FS_UUID: id, sys_is_mounted: null, sys_is_connected: true, sys_dev_path: '/dev/disk-by-uuid/' + id, sys_mountpoint: '/media/gpshub-' + id };
  
  }

  load() {
      this.api_wait = true
      this.dataService.getDeviceHardware(this.id)
      .subscribe(this.DeviceHardwareObserver);
  }
  
  // set_device_hardware(jsondata, lock:boolean=false) {
  // 	  this.device_hardware = jsondata
  // 	  this.api_wait = lock
  // }

  mount(dev_hw: iDeviceHardware) {
    this.api_wait = true
    // patch aproach:
    // this.dataService.mountDeviceHardware(dev_hw, true)
    // .subscribe(this.DeviceHardwareObserver);
 
    // update aproach:
    dev_hw.sys_is_mounted = true
    this.dataService.updateDeviceHardware(dev_hw)
    .subscribe(this.DeviceHardwareObserver);
  }

  umount(dev_hw: iDeviceHardware) {
    this.api_wait = true
    // patch aproach:
    // 	    // this.dataService.mountDeviceHardware(dev_hw, false)
    // 	    // .subscribe((jsondata: iDeviceHardware) => {
    // 	    //   this.device_hardware = jsondata;
    // 	    //   this.api_wait = false;
    // 	    // });
    // this.dataService.mountDeviceHardware(dev_hw, false)
    // .subscribe(this.DeviceHardwareObserver);

    // update aproach:
    dev_hw.sys_is_mounted = false
    this.dataService.updateDeviceHardware(dev_hw)
    .subscribe(this.DeviceHardwareObserver);
  }

  save(dev_hw: iDeviceHardware) {
    this.api_wait = true
    this.dataService.updateDeviceHardware(dev_hw)
    .subscribe(this.DeviceHardwareObserver);
    // console.log('device_hardware save() : not implemented ..')
    // alert('save() not implemented.')
    // this.api_wait = false;
  }

}
