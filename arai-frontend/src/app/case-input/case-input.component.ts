import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button'
import { BackendService } from '../backend.service';
import { UserInputRequest, userInput } from '../requests-responses';


@Component({
  selector: 'app-case-input',
  standalone: true,
  imports: [
    // other modules
    CommonModule,
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

  onSubmit(): void {
    if(this.userInput !== null) {
      this.backendService.sendMessage(new UserInputRequest(this.userInput));
    } else {
      console.error(`caseInputComponent, onSubmit, userInput is null!`)
    }
  }

}
