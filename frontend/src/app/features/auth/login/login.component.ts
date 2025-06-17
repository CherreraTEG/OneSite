import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SharedModule } from '../../../shared/shared.module';
import { TranslateService, TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [SharedModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm: FormGroup;
  currentLang: string = 'es';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });

    // Establecer el idioma inicial
    this.currentLang = localStorage.getItem('preferredLanguage') || 'es';
    this.translate.use(this.currentLang);
  }

  onLanguageChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    const language = select.value;
    this.currentLang = language;
    this.translate.use(language);
    localStorage.setItem('preferredLanguage', language);
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      // TODO: Implementar lógica de autenticación
      console.log('Form submitted:', this.loginForm.value);
      this.snackBar.open('Inicio de sesión exitoso', 'Cerrar', {
        duration: 3000
      });
    }
  }
} 