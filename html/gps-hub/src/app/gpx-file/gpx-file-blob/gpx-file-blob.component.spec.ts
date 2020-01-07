import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GpxFileBlobComponent } from './gpx-file-blob.component';

describe('GpxFileBlobComponent', () => {
  let component: GpxFileBlobComponent;
  let fixture: ComponentFixture<GpxFileBlobComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GpxFileBlobComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GpxFileBlobComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
