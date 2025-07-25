import { Component, Input, Output, EventEmitter, ViewChild, ElementRef } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [MatButtonModule, CommonModule],
  template: `
    <button #nativeButton
      [type]="type"
      [ngClass]="variant"
      (click)="onClick.emit($event)">
      <ng-content></ng-content>
    </button>
  `,
  styles: [`
    .primary {
      background: #C2DFEA !important;
      color: #545386 !important;
      font-weight: 700;
      border: none;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(84, 83, 134, 0.15);
      padding: 0 32px;
      height: 28px;
      min-height: 24px;
      line-height: 1.1;
      font-size: 13px;
      letter-spacing: 0.5px;
      transition: background 0.2s, box-shadow 0.2s, transform 0.1s, color 0.2s;
      text-transform: uppercase;
      outline: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      vertical-align: middle;
    }
    .primary:hover, .primary:focus {
      background: #545386 !important;
      color: #fff !important;
      box-shadow: 0 4px 16px rgba(84, 83, 134, 0.22);
      transform: translateY(-2px) scale(1.03);
    }
    .primary [icon] {
      align-self: center;
      vertical-align: middle;
      margin-bottom: 0 !important;
      margin-top: 0 !important;
      display: inline-block;
    }
    .secondary {
      background: #fff;
      color: #545386 !important;
      font-weight: 600;
      border: 2px solid #545386;
      border-radius: 8px;
      box-shadow: 0 1px 4px rgba(84, 83, 134, 0.08);
      padding: 0 24px;
      height: 36px;
      font-size: 13px;
      letter-spacing: 0.5px;
      transition: background 0.2s, color 0.2s, border 0.2s, box-shadow 0.2s;
      text-transform: uppercase;
      outline: none;
      display: flex;
      align-items: center;
    }
    .secondary:hover, .secondary:focus {
      background: #f5f7fa;
      color: #3d3c6e !important;
      border-color: #3d3c6e;
      box-shadow: 0 2px 8px rgba(84, 83, 134, 0.15);
      transform: translateY(-1px) scale(1.02);
    }
    .custom-button {
      font-family: 'Montserrat', sans-serif;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-radius: 4px;
    }
  `]
})
export class ButtonComponent {
  @ViewChild('nativeButton', { static: true }) nativeButton!: ElementRef<HTMLButtonElement>;
  @Input() type: string = 'button';
  @Input() variant: string = 'primary';
  @Output() onClick = new EventEmitter<Event>();

  blur() {
    this.nativeButton.nativeElement.blur();
  }
} 