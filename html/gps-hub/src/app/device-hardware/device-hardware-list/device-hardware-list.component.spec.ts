import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceHardwareListComponent } from './device-hardware-list.component';

describe('DeviceHardwareListComponent', () => {
  let component: DeviceHardwareListComponent;
  let fixture: ComponentFixture<DeviceHardwareListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeviceHardwareListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceHardwareListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
