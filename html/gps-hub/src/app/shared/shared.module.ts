import { NgModule } from '@angular/core';

import { BooleanPipe } from './boolean.pipe';

@NgModule({
    declarations: [ BooleanPipe ],
    exports: [ BooleanPipe ]
})
export class SharedModule { }