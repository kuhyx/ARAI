import { Component, Inject } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import {MAT_DIALOG_DATA, MatDialogModule, MatDialogRef} from '@angular/material/dialog'
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-email-input',
  standalone: true,
  imports: [MatDialogModule, MatInputModule, MatButtonModule],
  templateUrl: './email-input.component.html',
  styleUrl: './email-input.component.scss'
})
export class EmailInputComponent {
  constructor(
    public dialogRef: MatDialogRef<EmailInputComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {}

    emailFormControl = new FormControl('', [Validators.required, Validators.email]);


  onNoClick(): void {
    this.dialogRef.close();
  }
}
