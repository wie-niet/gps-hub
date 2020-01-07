import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { CoreModule } from './core/core.module';
import { DeviceHardwareModule } from './device-hardware/device-hardware.module';
import { DeviceConfigModule } from './device-config/device-config.module';
import { GpxFileModule } from './gpx-file/gpx-file.module';
import { GpsModule } from './gps/gps.module';


import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    AppComponent,
    
  ],
  imports: [
    BrowserModule,
	FormsModule,
    AppRoutingModule,
    CoreModule,
    DeviceHardwareModule, 
	DeviceConfigModule, 
    GpxFileModule, 
	GpsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
