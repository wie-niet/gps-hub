import { NgModule } from '@angular/core';
// import { CommonModule } from '@angular/common';

import { HttpClientModule } from '@angular/common/http';

import { DataService } from './data.service';


@NgModule({
  declarations: [],
  imports:   [ HttpClientModule ],
  providers: [ DataService ]
})
export class CoreModule { }
