import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DeviceConfigListComponent } from './device-config-list/device-config-list.component';
import { DeviceConfigComponent } from './device-config.component';
import { DeviceConfigRoutingModule } from './device-config-routing.module'
import { SharedModule } from '../shared/shared.module'

import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [DeviceConfigListComponent, DeviceConfigComponent],
  imports: [
    CommonModule, DeviceConfigRoutingModule, SharedModule, FormsModule
  ],
  exports:[DeviceConfigListComponent, DeviceConfigComponent]
  
})
export class DeviceConfigModule { }
