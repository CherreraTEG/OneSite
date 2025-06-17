import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule
  ],
  template: `
    <mat-form-field appearance="outline" class="custom-input">
      <mat-label>{{ label }}</mat-label>
      <input matInput
             [type]="type"
             [placeholder]="placeholder"
             [formControl]="control"
             [required]="required"
             (input)="onInput($event)"
             (blur)="onBlur()">
      <mat-error *ngIf="control.invalid && (control.dirty || control.touched)">
        {{ getErrorMessage() }}
      </mat-error>
    </mat-form-field>
  `,
  styles: [`
    .custom-input {
      width: 100%;
      font-family: 'Montserrat', sans-serif;
    }

    ::ng-deep .custom-input {
      .mat-mdc-form-field-subscript-wrapper {
        display: none;
      }

      .mat-mdc-form-field-infix {
        padding-top: 8px;
        padding-bottom: 8px;
      }

      .mat-mdc-text-field-wrapper {
        background-color: white;
      }
    }
  `],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => InputComponent),
      multi: true
    }
  ]
})
export class InputComponent implements ControlValueAccessor {
  @Input() label = '';
  @Input() type = 'text';
  @Input() placeholder = '';
  @Input() required = false;
  @Input() control: any;

  value = '';
  disabled = false;
  onChange: any = () => {};
  onTouched: any = () => {};

  writeValue(value: any): void {
    this.value = value;
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  onInput(event: any): void {
    this.value = event.target.value;
    this.onChange(this.value);
  }

  onBlur(): void {
    this.onTouched();
  }

  getErrorMessage(): string {
    if (this.control.hasError('required')) {
      return 'Este campo es requerido';
    }
    if (this.control.hasError('email')) {
      return 'Email inválido';
    }
    if (this.control.hasError('minlength')) {
      return `Mínimo ${this.control.errors?.['minlength'].requiredLength} caracteres`;
    }
    return '';
  }
} 