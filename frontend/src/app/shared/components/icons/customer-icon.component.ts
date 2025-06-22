import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-customer-icon',
  standalone: true,
  template: `
    <svg 
      [attr.width]="size" 
      [attr.height]="size" 
      viewBox="0 0 24 24" 
      fill="none" 
      [attr.stroke]="stroke"
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    >
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </svg>
  `,
  styles: [`
    svg {
      display: block;
    }
  `]
})
export class CustomerIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = '#000';
} 