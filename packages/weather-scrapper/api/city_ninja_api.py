import json

import requests
from dtos.city import CityDTO

class CityNinjaApi:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self.load_pre_fetched_cities()

    def load_pre_fetched_cities(self) -> dict[str, CityDTO]:
        """
        Parse the cities.json file and return a list of CityDTO objects
        """   
        self.pre_loaded_cities = {}
        with open('./cities.json') as file:
            data = json.load(file)
            for city in data:
                self.pre_loaded_cities[city['City']] = CityDTO(city['City'], city['Latitude'], city['Longitude'])
            return self.pre_loaded_cities
    
    def fetch_cities(self, cities_names: list[str]) -> list[CityDTO]:
        """
        Fetches the list of cities from the API_NINJA_CITY_API_URL
        """

        cities = []
        for city_name in cities_names:
            if city_name in self.pre_loaded_cities:
                cities.append(self.pre_loaded_cities[city_name])
                continue
            
            params = {
                'name': city_name,
            }

            response = requests.get(self.url, params=params, headers={'X-Api-Key': self.api_key})
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

            cities.append(CityDTO(data[0]['name'], data[0]['latitude'], data[0]['longitude']))

        return cities
    
    def get_pre_loaded_cities(self) -> dict[str, CityDTO]:
        return self.pre_loaded_cities
