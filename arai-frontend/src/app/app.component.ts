import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CaseInputComponent } from './case-input/case-input.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { BackendService } from './backend.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CaseInputComponent, FlexLayoutModule, HttpClientModule],
  providers: [BackendService],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'arai-frontend';
}
