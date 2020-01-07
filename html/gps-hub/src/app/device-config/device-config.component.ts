import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { iDeviceConfig } from '../shared/interfaces';

import { DataService } from '../core/data.service';


@Component({
  selector: 'app-device-config',
  templateUrl: './device-config.component.html',
  styleUrls: ['./device-config.component.css']
})
export class DeviceConfigComponent implements OnInit {
    id :string;
    device_config: iDeviceConfig|null;
    api_wait: boolean = false;
    error: any;
	form_edit_mode: boolean = false;
	

    private DeviceConfigObserver = {
      next: jsondata => this.device_config = jsondata,
      error: (err) => {
        this.error = err ;
        console.log(err);
        this.api_wait = false;
  	  },
      complete:  () => {
        this.api_wait = false;
        this.set_edit_mode(false);
        this.error = null;
      }
    };

	constructor(private route: ActivatedRoute , private dataService: DataService) { }

	ngOnInit() {
	    this.id = this.route.snapshot.paramMap.get('id');
		this.load()
	}

	load() {
        this.api_wait = true
        this.dataService.getDeviceConfig(this.id)
        .subscribe(this.DeviceConfigObserver);
	}
	
	set_edit_mode(mode:boolean = true) {
		this.form_edit_mode = mode
	}
	
  save(data: iDeviceConfig) {
    this.api_wait = true
    this.dataService.updateDeviceConfig(data)
    .subscribe(this.DeviceConfigObserver);
  }

  delete(id) {
    if(confirm("Are you sure to delete this config.\nid:"+ id)) {

      this.api_wait = true
      this.dataService.deleteDeviceConfig(id)
      .subscribe(this.DeviceConfigObserver);
    }
  }
}
