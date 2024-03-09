import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { MatButtonModule } from '@angular/material/button'
import { BackendService } from '../backend.service';
import { GenericRequest, ReturnResponse, UserInputRequest, userInput } from '../requests-responses';
import { Router } from '@angular/router';
import { KosztaService } from '../koszta.service';


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

  constructor(private fb: FormBuilder, private readonly backendService: BackendService, private readonly router: Router, private readonly kosztaService: KosztaService) {
    this.userInputForm = this.fb.group({
      generic_input: [''],
      trial_value: [],
      location: [''],
      experts_called: [false],
      witnesses_called: [false]
    });
  }

  async onSubmit() {
    this.userInput = this.userInputForm.value;
    if(this.userInput !== null) {
    const result = await this.backendService.sendMessage(new UserInputRequest(this.userInput)) as ReturnResponse;
    this.kosztaService.czas = String(result.response_data.first.time_of_trial);
    this.kosztaService.koszta = String(result.response_data.first.cost_of_trial);
    this.router.navigate(['koszt']);
  } else {
    console.error(`caseInputComponent, onSubmit, userInput is null!`)
  }
}
}
