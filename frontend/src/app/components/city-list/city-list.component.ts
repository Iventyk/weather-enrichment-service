import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

import { City } from '../../models/city.model';

@Component({
  selector: 'app-city-list',
  imports: [CommonModule],
  templateUrl: './city-list.component.html',
  styleUrl: './city-list.component.css',
})
export class CityListComponent {
  @Input({ required: true }) cities: City[] = [];
  @Input({ required: true }) refreshingCityIds = new Set<number>();
  @Output() refreshCity = new EventEmitter<number>();

  protected trackByCityId(_: number, city: City): number {
    return city.id;
  }

  protected isRefreshing(cityId: number): boolean {
    return this.refreshingCityIds.has(cityId);
  }
}
