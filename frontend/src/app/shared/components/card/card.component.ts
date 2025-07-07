import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  template: `
    <mat-card class="custom-card">
      <mat-card-content>
        <ng-content></ng-content>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .custom-card {
      font-family: 'Montserrat', sans-serif;
      border-radius: 8px;
      margin: 16px;
      padding: 24px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
      transition: box-shadow 0.3s ease-in-out;
    }

    .custom-card:hover {
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
  `]
})
export class CardComponent {} 