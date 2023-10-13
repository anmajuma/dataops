import requests

url = "https://api.tomorrow.io/v4/timelines"

# replace the location using the corresponding lat,long
#location = "47.75,-120.74"  # washington
location = "36.11,-115.17"  # las vegas

# replace apikey with your own API key
querystring = {"location": location, "fields": ["temperature", "humidity", "windSpeed", "windDirection", "windGust", "precipitationType", "solarGHI", "visibility", "weatherCode"],
               "units": "metric", "timesteps": "1d", "apikey": "o3BuPNTgB1yN3ApGJipYyE7PIvPL6LWk"}

response = requests.request("GET", url, params=querystring)

# replace the name based on your own preferences
with open('data.txt', 'w', encoding='utf8') as f:
    f.write(response.text)
