import { Component, Input, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    TranslateModule
  ],
  template: `
    <mat-form-field appearance="outline" class="custom-input-field" floatLabel="always">
      <mat-label>{{ label }}</mat-label>
      <ng-container *ngIf="!isTextarea; else textarea">
        <input #nativeInput matInput [type]="type" [formControl]="control" [placeholder]="placeholder">
      </ng-container>
      <ng-template #textarea>
        <textarea matInput [formControl]="control" [placeholder]="placeholder" rows="3"></textarea>
      </ng-template>
      <mat-error *ngIf="control.hasError('required')">{{ 'FORMS.ERRORS.REQUIRED' | translate }}</mat-error>
      <ng-content select="[matSuffix]"></ng-content>
    </mat-form-field>
  `,
  styles: [`.custom-input-field { width: 100%; }`]
})
export class InputComponent {
  @Input() label: string = '';
  @Input() placeholder: string = '';
  @Input() type: string = 'text';
  @Input() control: FormControl = new FormControl();
  @Input() isTextarea: boolean = false;

  @ViewChild('nativeInput', { static: false }) nativeInput!: ElementRef<HTMLInputElement>;

  showPicker(): void {
    if (this.nativeInput && this.nativeInput.nativeElement.type === 'date' && this.nativeInput.nativeElement.showPicker) {
      this.nativeInput.nativeElement.showPicker();
    } else if (this.nativeInput) {
      this.nativeInput.nativeElement.focus();
    }
  }
} 