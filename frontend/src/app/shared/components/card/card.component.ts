import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  template: `
    <mat-card [class.elevated]="elevated" class="custom-card">
      <mat-card-header *ngIf="title">
        <mat-card-title>{{ title }}</mat-card-title>
        <mat-card-subtitle *ngIf="subtitle">{{ subtitle }}</mat-card-subtitle>
      </mat-card-header>
      <mat-card-content>
        <ng-content></ng-content>
      </mat-card-content>
      <mat-card-actions *ngIf="showActions">
        <ng-content select="[cardActions]"></ng-content>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    .custom-card {
      font-family: 'Montserrat', sans-serif;
      border-radius: 8px;
      margin: 16px;
      transition: all 0.3s ease;
    }

    .custom-card.elevated {
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .custom-card:hover {
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    mat-card-header {
      margin-bottom: 16px;
    }

    mat-card-title {
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--color-primary);
    }

    mat-card-subtitle {
      color: var(--color-primary-light);
    }

    mat-card-content {
      padding: 16px 0;
    }

    mat-card-actions {
      padding: 16px;
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }
  `]
})
export class CardComponent {
  @Input() title?: string;
  @Input() subtitle?: string;
  @Input() elevated = true;
  @Input() showActions = false;
} 