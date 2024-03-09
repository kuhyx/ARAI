import { Component, Input } from '@angular/core';
import { StatisticsOutputInterface } from '../requests-responses';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-cost-view',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './cost-view.component.html',
  styleUrl: './cost-view.component.scss'
})
export class CostViewComponent {
@Input() costData: StatisticsOutputInterface | null = {
  cost_of_trial: 2137,
  time_of_trial: Date.UTC(0, 6, 0, 0, 0, 0, 0)
};

public calculateTimeDifference(utcDateNumber: number): string {
  const currentDate = new Date();
  const targetDate = new Date(utcDateNumber);
  const differenceInMilliseconds = targetDate.getTime() - currentDate.getTime();

  // Convert milliseconds to days
  const differenceInDays = differenceInMilliseconds / (1000 * 60 * 60 * 24);

  // Check if the difference is greater than or equal to 30 to approximate months
  if (differenceInDays >= 30) {
    const months = Math.floor(differenceInDays / 30);
    const years = Math.floor(differenceInDays/365);
    if(years > 0) {
      return `Twoja sprawa zajmie około ${years} lat`
    }
    if(months === 1) {
      return `Twoja sprawa zajmie około 1 miesiąc`;
    } else {
      return `Twoja sprawa zajmie około ${months} miesięcy`;
    }
  } else {
    return `Twoja sprawa zajmie około ${Math.ceil(differenceInDays)} dni`;
  }
}

}
