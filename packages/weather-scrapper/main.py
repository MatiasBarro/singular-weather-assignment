import os
import json
from dotenv import load_dotenv
from dtos.city import CityDTO
from scrapper.http_weather_data_scrapper import HttpWeatherDataScrapper
from data_processor import WeatherDataProcessor, WeatherFieldExtractor, WeatherTemperatureFieldExtractor, TemperatureUnit, WeatherWindFieldExtractor, WindSpeedUnit
from data_processor.consumer import PandasConsumer

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

    # Load the cities from the cities.json file
    cities = load_cities()

    # Get the current weather for each city using the Open Meteo API
    scrapper = HttpWeatherDataScrapper(os.getenv('OPEN_METEO_API_URL'))
    cities_weather = scrapper.get_cities_current_weather(cities)
    
    # Initialize the weather data processor with the field extractors and consumers
    weatherDataProcessor = WeatherDataProcessor()
    pandasConsumer = PandasConsumer()

    weatherDataProcessor.with_field_extractor(WeatherFieldExtractor("Humidity (%)", "humidity", "relative_humidity_2m"))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature (C)", "temperature_celsius", "temperature_2m", TemperatureUnit.CELSIUS))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature (F)", "temperature_fahrenheit", "temperature_2m", TemperatureUnit.FAHRENHEIT))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind (m/s)", "wind_mps", "wind_speed_10m", WindSpeedUnit.METERS_PER_SECOND))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind (mph)", "wind_mph", "wind_speed_10m", WindSpeedUnit.MILES_PER_HOUR))

    weatherDataProcessor.with_consumer(pandasConsumer)

    # Process the weather data
    weatherDataProcessor.process(cities_weather)

    # Print the result
    pandasConsumer.print()

if __name__ == "__main__":
    main()
