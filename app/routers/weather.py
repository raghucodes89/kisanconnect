from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings

router = APIRouter()

@router.get("/{city}")
async def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"City not found: {response.text}")
        data = response.json()
        return {
            "city": data["name"],
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