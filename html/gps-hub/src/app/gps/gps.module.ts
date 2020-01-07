import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { GpsListComponent } from './gps-list/gps-list.component';
import { GpsComponent } from './gps.component';
import { GpsRoutingModule } from './gps-routing.module'

import { SharedModule } from '../shared/shared.module'

import { DeviceHardwareModule } from '../device-hardware/device-hardware.module';
import { DeviceConfigModule } from '../device-config/device-config.module';
import { GpxFileModule } from '../gpx-file/gpx-file.module';


@NgModule({
  declarations: [GpsComponent, GpsListComponent],
  imports: [
    CommonModule,GpsRoutingModule, SharedModule, DeviceHardwareModule, DeviceConfigModule, GpxFileModule
  ]
})
export class GpsModule { }
