import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GpxFileListComponent } from './gpx-file-list.component';

describe('GpxFileListComponent', () => {
  let component: GpxFileListComponent;
  let fixture: ComponentFixture<GpxFileListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GpxFileListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GpxFileListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
