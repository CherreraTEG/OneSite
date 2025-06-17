import { Component, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MatButtonModule],
  template: `
    <button mat-raised-button
            [color]="color"
            [disabled]="disabled"
            [type]="type"
            class="custom-button">
      <ng-content></ng-content>
    </button>
  `,
  styles: [`
    .custom-button {
      font-family: 'Montserrat', sans-serif;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 0 24px;
      height: 40px;
      border-radius: 4px;
    }
  `]
})
export class ButtonComponent {
  @Input() color: 'primary' | 'accent' | 'warn' = 'primary';
  @Input() disabled = false;
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
} 