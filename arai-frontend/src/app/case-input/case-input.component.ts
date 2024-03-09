import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { MatButtonModule } from '@angular/material/button'
import { BackendService } from '../backend.service';
import { GenericRequest, UserInputRequest, userInput } from '../requests-responses';


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

  constructor(private fb: FormBuilder, private readonly backendService: BackendService) {
    this.userInputForm = this.fb.group({
      generic_input: [''],
      trial_value: [0],
      location: [''],
      experts_called: [false],
      witnesses_called: [false]
    });
  }

  ngOnInit() {
    const data: userInput = {
      "generic_input": "Rozwodzę się z żoną i chcę uczciwie podzielić majątek",
      "trial_cost": 1000,
      "location": "Katowice",
      "experts_called": true,
      "witnesses_called": true
  }
    const newRequest = new UserInputRequest(data);
    this.backendService.sendMessage(newRequest);
  }

  onSubmit(): void {
    if(this.userInput !== null) {
      this.backendService.sendMessage(new UserInputRequest(this.userInput));
    } else {
      console.error(`caseInputComponent, onSubmit, userInput is null!`)
    }
  }

}
