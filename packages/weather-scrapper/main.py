import os
import json
from dotenv import load_dotenv
from dtos.city_dto import CityDTO
from scrapper.http_weather_data_scrapper import HttpWeatherDataScrapper

load_dotenv()

# Parse the cities.json file and return a list of CityDTO objects
def load_cities() -> list[CityDTO]:
    cities = []
    with open('./cities.json') as file:
        data = json.load(file)
        for city in data:
            cities.append(CityDTO(city['City'], city['Latitude'], city['Longitude']))
    return cities


def main():
    if not os.getenv('OPEN_METEO_API_URL'):
       raise Exception("OPEN_METEO_API_URL is not set")

    cities = load_cities()
    scrapper = HttpWeatherDataScrapper(os.getenv('OPEN_METEO_API_URL'))
    cities_weather = scrapper.get_cities_current_weather(cities)
    print(cities_weather)
    


if __name__ == "__main__":
    main()
