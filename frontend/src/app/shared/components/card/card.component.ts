import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-card',
  template: `
    <div class="card">
      <div class="card-header" *ngIf="title">
        <h3 class="card-title">{{ title }}</h3>
      </div>
      <div class="card-body">
        <ng-content></ng-content>
      </div>
    </div>
  `,
  styles: [`
    .card {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin-bottom: 1rem;
    }
    .card-header {
      padding: 1rem;
      border-bottom: 1px solid #eee;
    }
    .card-title {
      margin: 0;
      font-size: 1.25rem;
      color: #333;
    }
    .card-body {
      padding: 1rem;
    }
  `]
})
export class CardComponent {
  @Input() title?: string;
} 