import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DeviceConfigListComponent } from './device-config-list/device-config-list.component';
import { DeviceConfigComponent } from './device-config.component';

const routes: Routes = [
    { path: 'device-config', component: DeviceConfigListComponent },
    { path: 'device-config/:id', component: DeviceConfigComponent }

];


@NgModule({
    imports: [ RouterModule.forChild(routes) ],
    exports: [ RouterModule ]
})
export class DeviceConfigRoutingModule {}
