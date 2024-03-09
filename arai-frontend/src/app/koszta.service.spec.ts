import { TestBed } from '@angular/core/testing';

import { KosztaService } from './koszta.service';

describe('KosztaService', () => {
  let service: KosztaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(KosztaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
