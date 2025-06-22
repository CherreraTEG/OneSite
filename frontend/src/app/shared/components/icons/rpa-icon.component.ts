import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-rpa-icon',
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
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
      <line x1="8" y1="21" x2="16" y2="21"/>
      <line x1="12" y1="17" x2="12" y2="21"/>
      <circle cx="12" cy="9" r="2"/>
      <path d="M12 11v4"/>
    </svg>
  `,
  styles: [`
    svg {
      display: block;
    }
  `]
})
export class RpaIconComponent {
  @Input() size: string = '24';
  @Input() stroke: string = '#000';
} 