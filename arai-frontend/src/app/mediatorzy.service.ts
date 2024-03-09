import { Injectable } from '@angular/core';
import { Mediator } from './requests-responses';

@Injectable({
  providedIn: 'root'
})
export class MediatorzyService {
  public mediatorzy: Mediator[] = [];

  setMediatorzy(setMediatorzy: Mediator[]) {
    this.mediatorzy = setMediatorzy.sort((a, b) => b.user_rating - a.user_rating);
    return this.mediatorzy;
  }
}
