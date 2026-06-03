export interface Weather {
  id: number;
  city_id: number;
  temperature: number;
  humidity: number;
  wind_speed: number;
  feels_like: number;
  description: string;
  recommendation: string;
  created_at: string;
}
