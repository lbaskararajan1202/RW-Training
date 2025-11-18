import os
import sys
import argparse
from datetime import datetime
import requests

#API endpoint for OpenWeatherMap
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str, api_key: str) -> dict:
    params = {"q": city, "appid": api_key, "units": "metric"}
    resp = requests.get(OWM_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def format_weather(data: dict) -> str:
    name = f"{data.get('name')}, {data.get('sys', {}).get('country', '')}"
    weather = data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
    main = data.get('main', {})
    temp = main.get('temp', 'N/A')
    feels = main.get('feels_like', 'N/A')
    humidity = main.get('humidity', 'N/A')
    sunrise = data.get('sys', {}).get('sunrise')
    sunset = data.get('sys', {}).get('sunset')
    def fmt_ts(ts):
        return datetime.fromtimestamp(ts).strftime("%H:%M") if ts else "N/A"
    return (
        f"{name}\n"
        f"Weather: {weather}\n"
        f"Temperature: {temp}°C (feels like {feels}°C)\n"
        f"Humidity: {humidity}%\n"
        f"Sunrise: {fmt_ts(sunrise)}  Sunset: {fmt_ts(sunset)}"
    )

def main(argv):
    p = argparse.ArgumentParser(description="Simple CLI Weather app (OpenWeatherMap)")
    p.add_argument("city", nargs="?", default="London", help="City name (e.g. London)")
    args = p.parse_args(argv[1:])

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        api_key = input("Enter OpenWeatherMap API key (or set OPENWEATHER_API_KEY): ").strip()
        if not api_key:
            print("API key required. Get one from https://openweathermap.org/ and set OPENWEATHER_API_KEY.")
            return 1

    try:
        data = get_weather(args.city, api_key)
        print(format_weather(data))
        return 0
    except requests.HTTPError as e:
        try:
            detail = e.response.json().get("message", "") if e.response is not None else ""
        except Exception:
            detail = ""
        print(f"Failed to fetch weather: {e}. {detail}")
        return 2
    except Exception as e:
        print(f"Error: {e}")
        return 3

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))