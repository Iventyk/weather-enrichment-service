import { Weather } from './weather.model';

export interface City {
  id: number;
  name: string;
  created_at: string;
  latest_weather: Weather | null;
}

export interface CityCreate {
  name: string;
}

export interface RefreshResponse {
  task_id: string;
  status: string;
}
