import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CaseInputComponent } from './case-input.component';

describe('CaseInputComponent', () => {
  let component: CaseInputComponent;
  let fixture: ComponentFixture<CaseInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CaseInputComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CaseInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
