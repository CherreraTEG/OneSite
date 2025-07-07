import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Truck } from './truck.model';

@Injectable({ providedIn: 'root' })
export class TrucksService {
  private apiUrl = '/api/v1/trucks';

  constructor(private http: HttpClient) {}

  getTrucks(params?: any): Observable<Truck[]> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<Truck[]>(this.apiUrl, { params: httpParams });
  }

  getTruck(id: number): Observable<Truck> {
    return this.http.get<Truck>(`${this.apiUrl}/${id}`);
  }

  createTruck(truck: Truck): Observable<Truck> {
    return this.http.post<Truck>(this.apiUrl, truck);
  }

  updateTruck(id: number, truck: Truck): Observable<Truck> {
    return this.http.put<Truck>(`${this.apiUrl}/${id}`, truck);
  }

  deleteTruck(id: number): Observable<Truck> {
    return this.http.delete<Truck>(`${this.apiUrl}/${id}`);
  }
} 