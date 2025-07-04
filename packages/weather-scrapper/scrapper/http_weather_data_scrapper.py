import requests
from dtos.city_dto import CityDTO, CityWeatherApiResponseDTO

class HttpWeatherDataScrapper:
    def __init__(self, url):
        self.url = url

    def get_cities_current_weather(self, cities: list[CityDTO]) -> list[CityWeatherApiResponseDTO]:
        if not cities:
            return []

        # Per your request, we iterate over the list of cities, map the latitude and longitude,
        # and create a dictionary with comma-separated values for the API call.
        params = {
            "latitude": ",".join([str(city.latitude) for city in cities]),
            "longitude": ",".join([str(city.longitude) for city in cities]),
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "wind_speed_unit": "ms",
        }

        response = requests.get(self.url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        results = []
        num_locations = len(data)

        for i in range(num_locations):
            dto = CityWeatherApiResponseDTO(
                name=cities[i].name,
                latitude=data[i]["latitude"],
                longitude=data[i]["longitude"],
                current_units=data[i]["current_units"],
                current=data[i]["current"],
            )
            results.append(dto)

        return results