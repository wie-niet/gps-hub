import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GpxFileListComponent } from './gpx-file-list/gpx-file-list.component';
import { GpxFileComponent } from './gpx-file.component';
import { GpxFileBlobComponent } from './gpx-file-blob/gpx-file-blob.component';



@NgModule({
  declarations: [GpxFileListComponent, GpxFileComponent, GpxFileBlobComponent],
  imports: [
    CommonModule
  ]
})
export class GpxFileModule { }
