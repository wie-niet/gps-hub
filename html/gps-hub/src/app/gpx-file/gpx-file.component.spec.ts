import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GpxFileComponent } from './gpx-file.component';

describe('GpxFileComponent', () => {
  let component: GpxFileComponent;
  let fixture: ComponentFixture<GpxFileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GpxFileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GpxFileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
