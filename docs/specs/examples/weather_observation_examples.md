# Weather Observation Examples

Illustrative payloads that comply with `schema/fields/weather_observation.json`
and the weather extension workflow.

## Open-Meteo style observation
```json
{
  "observed_at": "2025-10-23T09:00:00Z",
  "location": {
    "latitude": 48.137,
    "longitude": 11.575,
    "altitude": 520
  },
  "temperature": { "value": 12.4, "unit": "Cel" },
  "humidity": { "value": 72, "unit": "%" },
  "dew_point": { "value": 7.6, "unit": "Cel" },
  "apparent_temperature": { "value": 11.1, "unit": "Cel" },
  "pressure": { "value": 1012.3, "unit": "hPa" },
  "precipitation": { "value": 0.0, "unit": "mm" },
  "rain": { "value": 0.0, "unit": "mm" },
  "snowfall": { "value": 0.0, "unit": "cm" },
  "weather_code": "03",
  "weather_code_text": "Clouds generally forming or developing during the past hour",
  "cloud_cover": {
    "percent": 62,
    "category": "scattered"
  },
  "cloud_cover_layers": {
    "low": 40,
    "mid": 65,
    "high": 20
  },
  "wind": {
    "speed": { "value": 15.8, "unit": "km/h" },
    "direction": "WSW",
    "gust": { "value": 28.4, "unit": "km/h" }
  },
  "visibility": { "value": 18, "unit": "km" },
  "solar_radiation": { "value": 320, "unit": "W/m2" },
  "ozone": { "value": 300, "unit": "DU" },
  "air_quality_index": 52,
  "uv_index": 2.4,
  "source": {
    "object_type": "weather-station",
    "object_id": "de-bayern-001",
    "display_name": "Munich Central Station",
    "uri": "eirenhall://station/de-bayern-001"
  }
}
```

## Minimal observation
```json
{
  "observed_at": "2025-10-23T09:00:00Z",
  "location": {
    "latitude": 40.7128,
    "longitude": -74.006,
    "altitude": 10
  },
  "weather_code": "00",
  "weather_code_text": "Clear, No significant weather observed"
}
```
