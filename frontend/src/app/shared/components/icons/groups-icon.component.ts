import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-groups-icon',
  standalone: true,
  imports: [CommonModule],
  template: `
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      [attr.width]="size" 
      [attr.height]="size"
      fill="none" 
      viewBox="0 0 24 24" 
      stroke-width="1.5" 
      [attr.stroke]="stroke">
      <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-4.663M5.022 13.978a6.375 6.375 0 014.288-1.168l-7.007-4.256a4.125 4.125 0 01-1.353-6.425M16.5 5.625a2.625 2.625 0 10-5.25 0 2.625 2.625 0 005.25 0z" />
    </svg>
  `,
})
export class GroupsIconComponent {
  @Input() size: string = '24';
  @Input() color: string = 'currentColor'; // For consistency, not used for fill
  @Input() stroke: string = 'currentColor';
} 