import { Component, Input } from '@angular/core';
import { IconComponent } from '../icon/icon.component';

@Component({
  selector: 'app-add-icon',
  standalone: true,
  imports: [IconComponent],
  template: `
    <app-icon [size]="size" [color]="color" [stroke]="stroke" [strokeWidth]="strokeWidth">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
        <path d="M12 8V16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M8 12H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </app-icon>
  `
})
export class AddIconComponent {
  @Input() size: string = '24';
  @Input() color: string = 'currentColor';
  @Input() stroke: string = 'currentColor';
  @Input() strokeWidth: string = '2';
} 