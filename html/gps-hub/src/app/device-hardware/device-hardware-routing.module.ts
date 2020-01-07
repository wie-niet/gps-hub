import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DeviceHardwareListComponent } from './device-hardware-list/device-hardware-list.component';
import { DeviceHardwareComponent } from './device-hardware.component';

const routes: Routes = [
    { path: 'device-hardware', component: DeviceHardwareListComponent },
    { path: 'device-hardware/:id', component: DeviceHardwareComponent }

];


@NgModule({
    imports: [ RouterModule.forChild(routes) ],
    exports: [ RouterModule ]
})
export class DeviceHardwareRoutingModule {}
