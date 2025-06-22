import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-product-icon',
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
      <path d="M3 3h18v18H3z"/>
      <path d="M3 9h18"/>
      <path d="M9 21V9"/>
    </svg>
  `,
  styles: [`
    svg {
      display: block;
    }
  `]
})
export class ProductIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = '#000';
} 