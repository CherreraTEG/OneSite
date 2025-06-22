import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-order-icon',
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
      <path d="M9 12l2 2 4-4"/>
      <path d="M21 12c-1 0-2-1-2-2s1-2 2-2 2 1 2 2-1 2-2 2z"/>
      <path d="M3 12c1 0 2-1 2-2s-1-2-2-2-2 1-2 2 1 2 2 2z"/>
      <path d="M12 3c0 1-1 2-2 2s-2-1-2-2 1-2 2-2 2 1 2 2z"/>
      <path d="M12 21c0-1 1-2 2-2s2 1 2 2-1 2-2 2-2-1-2-2z"/>
    </svg>
  `,
  styles: [`
    svg {
      display: block;
    }
  `]
})
export class OrderIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = '#000';
} 