import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { finalize } from 'rxjs';

import { City } from './models/city.model';
import { WeatherApiService } from './services/weather-api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  cities: City[] = [];
  isLoading = false;
  isSubmitting = false;
  errorMessage = '';
  refreshingCityIds = new Set<number>();

  cityForm = this.formBuilder.nonNullable.group({
    name: ['', [Validators.required, Validators.maxLength(120)]],
  });

  constructor(
    private readonly api: WeatherApiService,
    private readonly formBuilder: FormBuilder,
  ) {}

  ngOnInit(): void {
    this.loadCities();
  }

  loadCities(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.api
      .getCities()
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (cities) => {
          this.cities = cities;
        },
        error: () => {
          this.errorMessage = 'Could not load cities. Please try again.';
        },
      });
  }

  addCity(): void {
    if (this.cityForm.invalid) {
      this.cityForm.markAllAsTouched();
      return;
    }

    const name = this.cityForm.controls.name.value.trim();
    if (!name) {
      this.cityForm.controls.name.setErrors({ required: true });
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';

    this.api
      .createCity(name)
      .pipe(finalize(() => (this.isSubmitting = false)))
      .subscribe({
        next: () => {
          this.cityForm.reset();
          this.loadCities();
        },
        error: () => {
          this.errorMessage = 'Could not add the city. Please try again.';
        },
      });
  }

  refreshWeather(cityId: number): void {
    this.refreshingCityIds.add(cityId);
    this.errorMessage = '';

    this.api
      .refreshCity(cityId)
      .pipe(finalize(() => this.refreshingCityIds.delete(cityId)))
      .subscribe({
        next: () => {
          window.setTimeout(() => this.loadCities(), 1200);
        },
        error: () => {
          this.errorMessage = 'Could not refresh weather. Please try again.';
        },
      });
  }

  isRefreshing(cityId: number): boolean {
    return this.refreshingCityIds.has(cityId);
  }

  trackByCityId(_index: number, city: City): number {
    return city.id;
  }
}
