import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Obtener el token del localStorage
    const token = localStorage.getItem('access_token');
    
    // Si hay token, agregarlo a la petición
    if (token && this.authService.isAuthenticated()) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    // Procesar la petición y manejar errores
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        // Si es error 401 (Unauthorized), limpiar la sesión
        if (error.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('current_user');
          this.router.navigate(['/auth/login']);
        }
        
        return throwError(() => error);
      })
    );
  }
}