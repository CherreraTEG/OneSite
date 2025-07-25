import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SharedModule } from '../../../shared/shared.module';
import { TranslateService, TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../../core/services/auth.service';
import { finalize } from 'rxjs/operators';

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
  isLoading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private snackBar: MatSnackBar,
    private translate: TranslateService,
    private authService: AuthService
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
    if (this.loginForm.valid && !this.isLoading) {
      this.isLoading = true;
      
      // Deshabilitar el formulario durante el login
      this.loginForm.disable();
      
      const credentials = {
        username: this.loginForm.get('username')?.value,
        password: this.loginForm.get('password')?.value
      };

      // Limpiar cache del navegador para forzar verificación en tiempo real
      this.clearBrowserCache();

      // Primero verificar el estado de la cuenta
      this.authService.checkAccountStatus(credentials.username)
        .pipe(
          finalize(() => {
            this.isLoading = false;
            // Habilitar el formulario después del login
            this.loginForm.enable();
          })
        )
        .subscribe({
          next: (accountStatus) => {
            console.log('Estado de cuenta:', accountStatus);
            
            // Si la cuenta está bloqueada, mostrar mensaje simple
            if (accountStatus.status === 'locked') {
              let errorMessage = this.translate.instant('LOGIN.ERROR_ACCOUNT_LOCKED');
              this.snackBar.open(
                errorMessage,
                this.translate.instant('COMMON.CLOSE'),
                { 
                  duration: 8000,
                  panelClass: ['error-snackbar']
                }
              );
              return;
            }
            
            // Si la cuenta no está bloqueada, proceder con el login
            this.performLogin(credentials);
          },
          error: (error) => {
            console.error('Error verificando estado de cuenta:', error);
            // Si hay error al verificar estado, proceder con el login normal
            this.performLogin(credentials);
          }
        });
    }
  }

  private clearBrowserCache(): void {
    // Forzar limpieza de cache del navegador
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name);
        });
      });
    }
  }

  private performLogin(credentials: any): void {
    console.log('=== INICIANDO performLogin ===');
    this.authService.login(credentials)
      .subscribe({
        next: (response) => {
          console.log('Login exitoso:', response);
          
          // Mostrar mensaje de éxito
          this.snackBar.open(
            this.translate.instant('LOGIN.SUCCESS_MESSAGE'),
            this.translate.instant('COMMON.CLOSE'),
            { duration: 3000, panelClass: ['success-snackbar'] }
          );

          // Redirigir al dashboard
          this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          console.log('=== ERROR EN performLogin ===');
          console.error('Error en login:', error);
          console.error('Error status:', error.status);
          console.error('Error detail:', error.error?.detail);
          
          let errorMessage = this.translate.instant('LOGIN.ERROR_GENERIC');
          console.log('Mensaje genérico inicial:', errorMessage);
          
          if (error.status === 401) {
            errorMessage = this.translate.instant('LOGIN.ERROR_INVALID_CREDENTIALS');
          } else if (error.status === 403) {
            // Usuario no registrado en OneSite
            console.log('=== STATUS 403 DETECTADO ===');
            console.log('Aplicando mensaje de usuario no registrado');
            errorMessage = this.translate.instant('LOGIN.ERROR_USER_NOT_REGISTERED');
            console.log('Mensaje traducido:', errorMessage);
            // Si el servidor envía un mensaje específico, usarlo
            if (error.error && error.error.detail) {
              console.log('Usando mensaje del servidor:', error.error.detail);
              errorMessage = error.error.detail;
            }
          } else if (error.status === 423) {
            // Usuario bloqueado
            errorMessage = this.translate.instant('LOGIN.ERROR_ACCOUNT_LOCKED');
          } else if (error.status === 404) {
            // Usuario no encontrado
            errorMessage = this.translate.instant('LOGIN.ERROR_USER_NOT_FOUND');
          } else if (error.status === 429) {
            errorMessage = this.translate.instant('LOGIN.ERROR_TOO_MANY_ATTEMPTS');
          } else if (error.status === 0 || error.status === 503) {
            errorMessage = this.translate.instant('LOGIN.ERROR_SERVER_UNAVAILABLE');
          } else if (error.status === 400) {
            // Manejar errores de validación del backend
            if (error.error && error.error.detail) {
              if (Array.isArray(error.error.detail)) {
                errorMessage = error.error.detail.join(', ');
              } else {
                errorMessage = error.error.detail;
              }
            }
          }

          console.log('=== MENSAJE FINAL ===');
          console.log('Mensaje que se mostrará:', errorMessage);
          
          this.snackBar.open(
            errorMessage,
            this.translate.instant('COMMON.CLOSE'),
            { 
              duration: error.status === 423 ? 8000 : 5000, // Más tiempo para usuarios bloqueados
              panelClass: ['error-snackbar']
            }
          );
        }
      });
  }

  // Método para probar conexión con el backend
  testConnection(): void {
    this.authService.testConnection().subscribe({
      next: (response) => {
        console.log('Conexión exitosa con el backend:', response);
        this.snackBar.open(
          this.translate.instant('LOGIN.CONNECTION_SUCCESS'),
          this.translate.instant('COMMON.CLOSE'),
          { duration: 3000, panelClass: ['success-snackbar'] }
        );
      },
      error: (error) => {
        console.error('Error de conexión con el backend:', error);
        this.snackBar.open(
          this.translate.instant('LOGIN.CONNECTION_ERROR'),
          this.translate.instant('COMMON.CLOSE'),
          { duration: 5000, panelClass: ['error-snackbar'] }
        );
      }
    });
  }

  // Método para verificar manualmente el estado de una cuenta
  checkAccountStatus(): void {
    const username = this.loginForm.get('username')?.value;
    if (!username) {
      // Si no hay usuario en el formulario, pedir que lo ingrese
      const promptMessage = this.translate.instant('LOGIN.ACCOUNT_STATUS.PROMPT_USERNAME');
      const inputUsername = prompt(promptMessage);
      if (!inputUsername) {
        return; // Usuario canceló
      }
      
      this.verifyAccountStatus(inputUsername);
    } else {
      this.verifyAccountStatus(username);
    }
  }

  private verifyAccountStatus(username: string): void {
    this.authService.checkAccountStatus(username).subscribe({
      next: (accountStatus) => {
        console.log('Estado de cuenta verificado:', accountStatus);
        let message: string;
        
        if (accountStatus.status === 'locked') {
          message = this.translate.instant('LOGIN.ACCOUNT_STATUS.ACCOUNT_LOCKED');
        } else {
          message = this.translate.instant('LOGIN.ACCOUNT_STATUS.ACCOUNT_ACTIVE');
        }
        
        this.snackBar.open(
          message,
          this.translate.instant('COMMON.CLOSE'),
          { duration: 5000, panelClass: ['info-snackbar'] }
        );
      },
      error: (error) => {
        console.error('Error verificando estado de cuenta:', error);
        this.snackBar.open(
          this.translate.instant('LOGIN.ACCOUNT_STATUS.ERROR_VERIFYING'),
          this.translate.instant('COMMON.CLOSE'),
          { duration: 5000, panelClass: ['error-snackbar'] }
        );
      }
    });
  }
} 