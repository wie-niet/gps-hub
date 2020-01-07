import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { GpsListComponent } from './gps-list/gps-list.component';
import { GpsComponent } from './gps.component';

const routes: Routes = [
    { path: 'gps', component: GpsListComponent },
    { path: 'gps/:id', component: GpsComponent }

];


@NgModule({
    imports: [ RouterModule.forChild(routes) ],
    exports: [ RouterModule ]
})
export class GpsRoutingModule {}
