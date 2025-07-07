import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Company, CompanyList, CompanyCreate, CompanyUpdate } from '../models/company.model';

@Injectable({
  providedIn: 'root'
})
export class CompanyService {
  private apiUrl = `${environment.apiUrl}/api/v1/companies`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene una lista paginada de empresas
   */
  getCompanies(
    skip: number = 0, 
    limit: number = 100, 
    activeOnly: boolean = true
  ): Observable<CompanyList> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString())
      .set('active_only', activeOnly.toString());

    return this.http.get<CompanyList>(this.apiUrl, { params });
  }

  /**
   * Obtiene todas las empresas activas (sin paginación)
   * Útil para selectores y dropdowns
   */
  getActiveCompanies(): Observable<Company[]> {
    return this.http.get<Company[]>(`${this.apiUrl}/active`);
  }

  /**
   * Obtiene una empresa específica por su ID
   */
  getCompany(id: number): Observable<Company> {
    return this.http.get<Company>(`${this.apiUrl}/${id}`);
  }

  /**
   * Crea una nueva empresa
   */
  createCompany(company: CompanyCreate): Observable<Company> {
    return this.http.post<Company>(this.apiUrl, company);
  }

  /**
   * Actualiza una empresa existente
   */
  updateCompany(id: number, company: CompanyUpdate): Observable<Company> {
    return this.http.put<Company>(`${this.apiUrl}/${id}`, company);
  }

  /**
   * Elimina una empresa (soft delete)
   */
  deleteCompany(id: number): Observable<Company> {
    return this.http.delete<Company>(`${this.apiUrl}/${id}`);
  }
} 