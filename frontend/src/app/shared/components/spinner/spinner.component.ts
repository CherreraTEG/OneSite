import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule],
  template: `
    <div class="spinner-container" *ngIf="loading">
      <mat-spinner
        [diameter]="diameter"
        [color]="color"
        class="custom-spinner">
      </mat-spinner>
      <span class="spinner-text" *ngIf="text">{{ text }}</span>
    </div>
  `,
  styles: [`
    .spinner-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .custom-spinner {
      margin-bottom: 16px;
    }

    .spinner-text {
      font-family: 'Montserrat', sans-serif;
      color: var(--color-primary);
      font-size: 14px;
      font-weight: 500;
    }
  `]
})
export class SpinnerComponent {
  @Input() loading = false;
  @Input() diameter = 50;
  @Input() color: 'primary' | 'accent' | 'warn' = 'primary';
  @Input() text = '';
} 