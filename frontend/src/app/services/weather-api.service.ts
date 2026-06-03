import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { City } from '../models/city.model';

@Injectable({ providedIn: 'root' })
export class WeatherApiService {
  private readonly baseUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(`${this.baseUrl}/cities`);
  }

  createCity(name: string): Observable<City> {
    return this.http.post<City>(`${this.baseUrl}/cities`, { name });
  }

  refreshCity(cityId: number): Observable<{ status: string }> {
    return this.http.post<{ status: string }>(
      `${this.baseUrl}/cities/${cityId}/refresh`,
      {},
    );
  }
}
