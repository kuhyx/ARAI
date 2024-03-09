import { TestBed } from '@angular/core/testing';

import { kosztService } from './koszt.service';

describe('kosztService', () => {
  let service: kosztService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(kosztService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
