import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-logout-icon',
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
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
    </svg>
  `
})
export class LogoutIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = 'currentColor';
  @Input() strokeWidth: string = '1.5';
} 