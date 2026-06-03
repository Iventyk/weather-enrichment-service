import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { finalize } from 'rxjs';

import { CityFormComponent } from './components/city-form/city-form.component';
import { CityListComponent } from './components/city-list/city-list.component';
import { City } from './models/city.model';
import { WeatherApiService } from './services/weather-api.service';

@Component({
  selector: 'app-root',
  imports: [CommonModule, CityFormComponent, CityListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  private readonly weatherApi = inject(WeatherApiService);

  protected readonly cities = signal<City[]>([]);
  protected readonly isLoading = signal(true);
  protected readonly isAdding = signal(false);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly refreshingCityIds = signal(new Set<number>());
  protected readonly hasCities = computed(() => this.cities().length > 0);

  ngOnInit(): void {
    this.loadCities();
  }

  protected loadCities(): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.weatherApi
      .getCities()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (cities) => this.cities.set(cities),
        error: () =>
          this.errorMessage.set(
            'Could not load cities. Check that the backend is running.',
          ),
      });
  }

  protected addCity(name: string): void {
    this.isAdding.set(true);
    this.errorMessage.set(null);

    this.weatherApi
      .addCity({ name })
      .pipe(finalize(() => this.isAdding.set(false)))
      .subscribe({
        next: () => this.loadCities(),
        error: () =>
          this.errorMessage.set(
            'Could not add the city. Try another name or try again later.',
          ),
      });
  }

  protected refreshCity(cityId: number): void {
    this.updateRefreshingCityIds(cityId, true);
    this.errorMessage.set(null);

    this.weatherApi
      .refreshCity(cityId)
      .pipe(finalize(() => this.updateRefreshingCityIds(cityId, false)))
      .subscribe({
        next: () => this.loadCities(),
        error: () =>
          this.errorMessage.set(
            'Could not start the weather refresh for the selected city.',
          ),
      });
  }

  private updateRefreshingCityIds(cityId: number, isRefreshing: boolean): void {
    const nextIds = new Set(this.refreshingCityIds());

    if (isRefreshing) {
      nextIds.add(cityId);
    } else {
      nextIds.delete(cityId);
    }

    this.refreshingCityIds.set(nextIds);
  }
}
