import { Component, OnInit } from '@angular/core';

import { DataService } from '../../core/data.service';

import { iDeviceConfig } from '../../shared/interfaces'


@Component({
  selector: 'app-device-config-list',
  templateUrl: './device-config-list.component.html',
  styleUrls: ['./device-config-list.component.css']
})
export class DeviceConfigListComponent implements OnInit {
  device_config_list: iDeviceConfig[]
  api_wait: boolean = true;
  
  
  constructor(private dataService: DataService) {}

  ngOnInit() {
	  this.load()
  }


  load() {
    this.api_wait = true
    this.dataService.getDeviceConfigList()
    .subscribe((jsondata: iDeviceConfig[]) => {
      this.device_config_list = jsondata;
      this.api_wait = false;
    });

  }

}
