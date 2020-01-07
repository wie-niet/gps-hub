import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { DeviceHardwareListComponent } from './device-hardware-list/device-hardware-list.component';
import { DeviceHardwareComponent } from './device-hardware.component';
import { DeviceHardwareRoutingModule } from './device-hardware-routing.module'
import { SharedModule } from '../shared/shared.module'

@NgModule({
  declarations: [DeviceHardwareListComponent, DeviceHardwareComponent],
  imports: [
    CommonModule, DeviceHardwareRoutingModule, SharedModule
  ],
  exports: [DeviceHardwareListComponent, DeviceHardwareComponent]
})
export class DeviceHardwareModule { }
