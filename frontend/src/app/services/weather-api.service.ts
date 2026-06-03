import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { City, CityCreate, RefreshResponse } from '../models/city.model';

@Injectable({ providedIn: 'root' })
export class WeatherApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(`${this.apiUrl}/cities`);
  }

  addCity(payload: CityCreate): Observable<City> {
    return this.http.post<City>(`${this.apiUrl}/cities`, payload);
  }

  refreshCity(cityId: number): Observable<RefreshResponse> {
    return this.http.post<RefreshResponse>(
      `${this.apiUrl}/cities/${cityId}/refresh`,
      {},
    );
  }
}
