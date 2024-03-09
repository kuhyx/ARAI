import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCheckboxModule } from '@angular/material/checkbox'


@Component({
  selector: 'app-case-input',
  standalone: true,
  imports: [
    // other modules
    MatInputModule,
    MatCheckboxModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
  ],
  templateUrl: './case-input.component.html',
  styleUrl: './case-input.component.scss'
})
export class CaseInputComponent {

}
