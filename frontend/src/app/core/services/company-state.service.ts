import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CompanyStateService {
  // BehaviorSubject para mantener el ID de la empresa actual.
  // Inicia con '1' como valor por defecto.
  private selectedCompanySubject = new BehaviorSubject<string>('1');

  // Observable público para que los componentes se suscriban.
  public selectedCompany$: Observable<string> = this.selectedCompanySubject.asObservable();

  constructor() {
    this.loadInitialCompany();
  }

  /**
   * Carga el ID de la empresa desde localStorage al iniciar el servicio.
   * Esto permite que la selección del usuario persista entre sesiones.
   */
  private loadInitialCompany(): void {
    const savedCompanyId = localStorage.getItem('selectedCompanyId');
    if (savedCompanyId) {
      this.selectedCompanySubject.next(savedCompanyId);
    }
  }

  /**
   * Actualiza el ID de la empresa seleccionada y lo guarda en localStorage.
   * @param companyId El ID de la nueva empresa seleccionada.
   */
  setSelectedCompany(companyId: string): void {
    this.selectedCompanySubject.next(companyId);
    localStorage.setItem('selectedCompanyId', companyId);
  }

  /**
   * Devuelve el valor actual del ID de la empresa de forma síncrona.
   * @returns El ID de la empresa seleccionada actualmente.
   */
  getSelectedCompany(): string {
    return this.selectedCompanySubject.getValue();
  }
} 