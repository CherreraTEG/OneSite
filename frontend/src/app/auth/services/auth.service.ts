import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

export interface User {
  id: string;
  username: string;
  email: string;
  roles: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;
  private readonly TOKEN_KEY = 'access_token';

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<User | null>(null);
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  login(username: string, password: string): Observable<User> {
    return this.http.post<any>(`${environment.apiUrl}/auth/login`, { username, password })
      .pipe(
        map(response => {
          // Almacenar token y datos del usuario
          localStorage.setItem(this.TOKEN_KEY, response.token);
          const user = response.user;
          this.currentUserSubject.next(user);
          return user;
        }),
        catchError(error => {
          console.error('Error en login:', error);
          return of(null);
        })
      );
  }

  logout(): void {
    // Remover token y datos del usuario
    localStorage.removeItem(this.TOKEN_KEY);
    this.currentUserSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!this.currentUserValue;
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  // Método para verificar si el usuario tiene un rol específico
  hasRole(role: string): boolean {
    return this.currentUserValue?.roles.includes(role) || false;
  }
} 