import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

// Material Modules
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

// Shared Components
import { ButtonComponent } from './components/button/button.component';
import { CardComponent } from './components/card/card.component';
import { InputComponent } from './components/input/input.component';
import { SpinnerComponent } from './components/spinner/spinner.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    // Material Modules
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatIconModule,
    MatFormFieldModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    // Shared Components
    ButtonComponent,
    CardComponent,
    InputComponent,
    SpinnerComponent
  ],
  exports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    // Material Modules
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatIconModule,
    MatFormFieldModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    // Shared Components
    ButtonComponent,
    CardComponent,
    InputComponent,
    SpinnerComponent
  ]
})
export class SharedModule { } 