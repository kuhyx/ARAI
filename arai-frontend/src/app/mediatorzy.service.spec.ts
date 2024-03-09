import { TestBed } from '@angular/core/testing';

import { MediatorzyService } from './mediatorzy.service';

describe('MediatorzyService', () => {
  let service: MediatorzyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MediatorzyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
