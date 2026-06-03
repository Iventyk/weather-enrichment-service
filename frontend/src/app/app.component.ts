import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';

import { CityWithWeather } from './models';
import { WeatherApiService } from './weather-api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  readonly cityName = new FormControl('', {
    nonNullable: true,
    validators: [Validators.required, Validators.maxLength(120)],
  });

  cities: CityWithWeather[] = [];
  isLoading = false;
  isAdding = false;
  errorMessage = '';
  refreshingCityIds = new Set<number>();

  constructor(private readonly weatherApi: WeatherApiService) {}

  ngOnInit(): void {
    this.loadCities();
  }

  loadCities(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.weatherApi
      .getCities()
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (cities) => (this.cities = cities),
        error: () => {
          this.errorMessage = 'Unable to load cities. Please try again.';
        },
      });
  }

  addCity(): void {
    const name = this.cityName.value.trim();

    if (!name || this.cityName.invalid) {
      this.cityName.markAsTouched();
      return;
    }

    this.isAdding = true;
    this.errorMessage = '';

    this.weatherApi
      .addCity(name)
      .pipe(finalize(() => (this.isAdding = false)))
      .subscribe({
        next: (city) => {
          this.cities = [
            city,
            ...this.cities.filter((item) => item.id !== city.id),
          ];
          this.cityName.reset('');
          window.setTimeout(() => this.loadCities(), 1500);
        },
        error: () => {
          this.errorMessage =
            'Unable to add this city. Please check the name and try again.';
        },
      });
  }

  refreshCity(city: CityWithWeather): void {
    this.refreshingCityIds.add(city.id);
    this.errorMessage = '';

    this.weatherApi
      .refreshCity(city.id)
      .pipe(finalize(() => this.refreshingCityIds.delete(city.id)))
      .subscribe({
        next: () => window.setTimeout(() => this.loadCities(), 1500),
        error: () => {
          this.errorMessage = `Unable to refresh weather for ${city.name}.`;
        },
      });
  }

  isRefreshing(cityId: number): boolean {
    return this.refreshingCityIds.has(cityId);
  }

  trackByCityId(_: number, city: CityWithWeather): number {
    return city.id;
  }
}
