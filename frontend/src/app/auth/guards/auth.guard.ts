import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    if (this.authService.isAuthenticated()) {
      // Verificar si la ruta requiere roles específicos
      const requiredRoles = route.data['roles'] as Array<string>;
      if (requiredRoles) {
        const hasRequiredRole = requiredRoles.some(role => this.authService.hasRole(role));
        if (!hasRequiredRole) {
          this.router.navigate(['/unauthorized']);
          return false;
        }
      }
      return true;
    }

    // No autenticado, redirigir a login
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }
} 