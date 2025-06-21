import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ecommerce-icon',
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
      <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c.51 0 .962-.343 1.087-.835l1.823-6.423a.75.75 0 0 0-.11-.634l-1.34-1.341a.75.75 0 0 0-.635-.257H4.5M4.5 14.25 5.625 5.176m14.25 9.074-.21-1.473" />
    </svg>
  `,
})
export class EcommerceIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = 'currentColor';
  @Input() strokeWidth: string = '1.5';
} 