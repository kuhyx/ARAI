import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CaseInputComponent } from './case-input/case-input.component';
import { FlexLayoutModule } from '@angular/flex-layout';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CaseInputComponent, FlexLayoutModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'arai-frontend';
}
