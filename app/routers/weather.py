from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings

router = APIRouter()

@router.get("/{location}")
async def get_weather(location: str):
    async with httpx.AsyncClient() as client:
        
        # Step 1 — Convert location name to coordinates
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {
            "q": location,
            "limit": 1,
            "appid": settings.WEATHER_API_KEY
        }
        geo_response = await client.get(geo_url, params=geo_params)
        geo_data = geo_response.json()

        if not geo_data:
            raise HTTPException(
                status_code=404,
                detail=f"Location '{location}' not found. Try a nearby town or city name."
            )

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        found_name = geo_data[0]["name"]
        country = geo_data[0].get("country", "")
        state = geo_data[0].get("state", "")

        # Step 2 — Get weather using coordinates
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric"
        }
        weather_response = await client.get(weather_url, params=weather_params)
        data = weather_response.json()

        return {
            "searched": location,
            "found_location": f"{found_name}, {state}, {country}",
            "latitude": lat,
            "longitude": lon,
            "temperature_c": data["main"]["temp"],
            "feels_like_c": data["main"]["feels_like"],
            "humidity_percent": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed_ms": data["wind"]["speed"],
            "advice": get_farming_advice(data["weather"][0]["main"], data["main"]["temp"])
        }

def get_farming_advice(weather: str, temp: float):
    if weather in ["Rain", "Drizzle"]:
        return "Good time for planting. Avoid spraying pesticides."
    elif weather == "Thunderstorm":
        return "Stay indoors. Protect crops with covers."
    elif weather == "Clear" and temp > 35:
        return "Very hot. Water crops early morning or evening."
    elif weather == "Clear":
        return "Good weather for harvesting and drying crops."
    elif weather == "Clouds":
        return "Moderate weather. Good for field work."
    elif weather in ["Haze", "Fog"]:
        return "Low visibility. Watch out for fungal diseases."
    else:
        return "Check local conditions before farm work."