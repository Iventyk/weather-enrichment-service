export interface WeatherRead {
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

export interface CityWithWeather {
  id: number;
  name: string;
  created_at: string;
  latest_weather: WeatherRead | null;
}
