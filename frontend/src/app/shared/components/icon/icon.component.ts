import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-icon',
  standalone: true,
  imports: [CommonModule],
  template: `
    <svg
      [attr.width]="size"
      [attr.height]="size"
      [attr.fill]="color"
      [attr.stroke]="stroke"
      [attr.stroke-width]="strokeWidth"
      [class]="className"
    >
      <ng-content></ng-content>
    </svg>
  `,
  styles: [`
    :host {
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
  `]
})
export class IconComponent {
  @Input() size: string = '24';
  @Input() color: string = 'currentColor';
  @Input() stroke: string = 'currentColor';
  @Input() strokeWidth: string = '2';
  @Input() className: string = '';
} 