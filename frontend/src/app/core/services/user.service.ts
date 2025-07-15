import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface UserCompanyPermission {
  company_code: string;
  permission_type: string;
}

export interface UserWithPermissions {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  companies: UserCompanyPermission[];
  roles: string[];
}

export interface UserCreateRequest {
  username: string;
  email: string;
  full_name?: string;
  password: string;
  is_active: boolean;
  is_superuser: boolean;
  company_permissions: UserCompanyPermission[];
}

export interface UsersListResponse {
  users: UserWithPermissions[];
  total: number;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}/api/v1/users`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene una lista paginada de usuarios
   */
  getUsers(
    skip: number = 0,
    limit: number = 100,
    search?: string,
    activeOnly: boolean = true
  ): Observable<UserWithPermissions[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString())
      .set('active_only', activeOnly.toString());

    if (search) {
      params = params.set('search', search);
    }

    return this.http.get<UserWithPermissions[]>(this.apiUrl, { params });
  }

  /**
   * Obtiene un usuario específico por ID
   */
  getUser(id: number): Observable<UserWithPermissions> {
    return this.http.get<UserWithPermissions>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crea un nuevo usuario
   */
  createUser(userData: UserCreateRequest): Observable<UserWithPermissions> {
    return this.http.post<UserWithPermissions>(this.apiUrl, userData);
  }

  /**
   * Actualiza un usuario existente
   */
  updateUser(id: number, userData: UserCreateRequest): Observable<UserWithPermissions> {
    return this.http.put<UserWithPermissions>(`${this.apiUrl}/${id}`, userData);
  }

  /**
   * Desactiva un usuario (soft delete)
   */
  deleteUser(id: number): Observable<{message: string}> {
    return this.http.delete<{message: string}>(`${this.apiUrl}/${id}`);
  }

  /**
   * Endpoint de prueba
   */
  testConnection(): Observable<any> {
    return this.http.get(`${this.apiUrl}/test`);
  }
}