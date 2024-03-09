import { Component, Input } from '@angular/core';
import { MatTableModule } from '@angular/material/table'
import { RecommendedMediatorsInterface } from '../requests-responses';
import { MatCardModule } from '@angular/material/card'
import { MatButtonModule } from '@angular/material/button';
import { faker } from '@faker-js/faker';
import {MatIconModule } from '@angular/material/icon'
import { MatDialog } from '@angular/material/dialog';
import { EmailInputComponent } from '../email-input/email-input.component';

@Component({
  selector: 'app-mediators-list',
  standalone: true,
  imports: [MatTableModule, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './mediators-list.component.html',
  styleUrl: './mediators-list.component.scss'
})
export class MediatorsListComponent {
  @Input() mediatorzy: RecommendedMediatorsInterface[] = [
    {
        "name": "Mateusz Szpyruk",
        "specialization": "Prawo podatkowe",
        "localization": "Katowice",
        "ai_rating": 99,
        "user_rating": 99,
        "number_of_opinions": 5
    },
    {
        "name": "Jan Kowalski",
        "specialization": "Prawo pracy",
        "localization": "Katowice",
        "ai_rating": 90,
        "user_rating": 99,
        "number_of_opinions": 5
    },
    {
        "name": "Jan Kowalski",
        "specialization": "Prawo pracy",
        "localization": "Katowice",
        "ai_rating": 76,
        "user_rating": 99,
        "number_of_opinions": 5
    }
]

constructor(private readonly dialog: MatDialog) {}

generatePersonInfo() {
  const personInfo = {
    firstName: faker.name.firstName(),
    lastName: faker.name.lastName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar() // Generating person image
  };
  console.log(`faker.image.avatar(): `, faker.image.avatar());
  const avatarUrl = personInfo.avatar;
  return avatarUrl;
}

convertToStars(score: number): string {
  if (score < 0 || score > 100) {
    return 'Score must be between 0 and 100';
  }

  // Calculate the number of full stars
  const fullStars = Math.floor(score / 20);
  // Determine if there should be a half star
  const halfStar = (score % 20) >= 10 ? 1 : 0;
  // Calculate the number of empty stars
  const emptyStars = 5 - fullStars - halfStar;

  return '★'.repeat(fullStars) + '✩'.repeat(halfStar) + '☆'.repeat(emptyStars);
}

generateCity() {
  return faker.location.city();
}

generateAddress() {
  return faker.location.streetAddress();
}

generateCost() {
  return faker.commerce.price();
}

generateOnline() {
  return faker.datatype.boolean();
}

umowSie() {
  const dialogRef = this.dialog.open(EmailInputComponent, {
    width: '250px',
    data: { /* Data passed to the modal */ }
  });

  dialogRef.afterClosed().subscribe(result => {
    console.log('The dialog was closed');
    // Optional: handle data returned from the modal
  });
}
}
