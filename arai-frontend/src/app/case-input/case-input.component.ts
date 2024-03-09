import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { MatButtonModule } from '@angular/material/button'
import { BackendService } from '../backend.service';
import { GenericRequest, Mediator, ReturnResponse, UserInputRequest, userInput } from '../requests-responses';
import { Router } from '@angular/router';
import { kosztService } from '../koszta.service';
import { MediatorzyService } from '../mediatorzy.service';


@Component({
  selector: 'app-case-input',
  standalone: true,
  imports: [
    MatInputModule,
    MatCheckboxModule,
    ReactiveFormsModule,
    MatButtonModule
  ],
  templateUrl: './case-input.component.html',
  styleUrl: './case-input.component.scss'
})
export class CaseInputComponent {
  userInputForm: FormGroup;
  userInput: userInput | null = null;
  receivedInfo: boolean = false;

  constructor(private fb: FormBuilder, private readonly backendService: BackendService, private readonly router: Router, private readonly kosztService: kosztService, private readonly mediatorzyService: MediatorzyService) {
    this.userInputForm = this.fb.group({
      generic_input: ['pracodawca nie wyplacil mi wynagrodzenia za ostatnie 2 miesiace i mnie zwolnil'],
      trial_value: [1000],
      location: ['Warszawa'],
      experts_called: [false],
      witnesses_called: [false]
    });
  }

  private static convertToMediators(input: string[]): Mediator[] {
    return input.map(item => JSON.parse(item) as Mediator);
  }

  async onSubmit() {
    this.userInput = this.userInputForm.value;
    if(this.userInput !== null) {
      if(!this.receivedInfo) {
      this.receivedInfo = true;
      const result = await this.backendService.sendMessage(new UserInputRequest(this.userInput)) as ReturnResponse;
      this.mediatorzyService.setMediatorzy(CaseInputComponent.convertToMediators(result.response_data.second as unknown as string[]));
      this.kosztService.czas = String(result.response_data.first.time_of_trial);
      this.kosztService.koszt = String(result.response_data.first.cost_of_trial);
      console.log(`result: `, result);
      this.router.navigate(['koszt']);
      }
  } else {
    console.error(`caseInputComponent, onSubmit, userInput is null!`)
  }
}
}
