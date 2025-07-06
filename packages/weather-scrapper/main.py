import os
import json
from dotenv import load_dotenv
from dtos.city import CityDTO
from scrapper.http_weather_data_scrapper import HttpWeatherDataScrapper
from data_processor import WeatherDataProcessor, WeatherFieldExtractor, WeatherTemperatureFieldExtractor, TemperatureUnit, WeatherWindFieldExtractor, WindSpeedUnit

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
    print(cities_weather[0])

    weatherDataProcessor = WeatherDataProcessor()
    weatherDataProcessor.with_field_extractor(WeatherFieldExtractor("Humidity", "humidity", "relative_humidity_2m"))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature", "temperature_celsius", "temperature_2m", TemperatureUnit.CELSIUS))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature", "temperature_fahrenheit", "temperature_2m", TemperatureUnit.FAHRENHEIT))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind", "wind_ms", "wind_speed_10m", WindSpeedUnit.METERS_PER_SECOND))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind", "wind_mph", "wind_speed_10m", WindSpeedUnit.MILES_PER_HOUR))

    rows = weatherDataProcessor.process(cities_weather)
    print(rows[0])


if __name__ == "__main__":
    main()
