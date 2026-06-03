import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { CityWithWeather } from './models';

@Injectable({ providedIn: 'root' })
export class WeatherApiService {
  private readonly apiUrl = '/api';

  constructor(private readonly http: HttpClient) {}

  getCities(): Observable<CityWithWeather[]> {
    return this.http.get<CityWithWeather[]>(`${this.apiUrl}/cities`);
  }

  addCity(name: string): Observable<CityWithWeather> {
    return this.http.post<CityWithWeather>(`${this.apiUrl}/cities`, { name });
  }

  refreshCity(cityId: number): Observable<{ status: string }> {
    return this.http.post<{ status: string }>(
      `${this.apiUrl}/cities/${cityId}/refresh`,
      {},
    );
  }
}
