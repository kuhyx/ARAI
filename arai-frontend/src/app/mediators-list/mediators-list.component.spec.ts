import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MediatorsListComponent } from './mediators-list.component';

describe('MediatorsListComponent', () => {
  let component: MediatorsListComponent;
  let fixture: ComponentFixture<MediatorsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MediatorsListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MediatorsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
