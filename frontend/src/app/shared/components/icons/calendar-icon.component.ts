import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-calendar-icon',
  standalone: true,
  imports: [CommonModule],
  template: `
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      [attr.width]="size" 
      [attr.height]="size"
      fill="none" 
      viewBox="0 0 24 24" 
      [attr.stroke-width]="strokeWidth"
      [attr.stroke]="stroke">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
    </svg>
  `
})
export class CalendarIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = 'currentColor';
  @Input() strokeWidth: string = '1.5';
} 