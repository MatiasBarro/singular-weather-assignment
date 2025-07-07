import os
import json
import argparse
from dotenv import load_dotenv
from dtos.city import CityDTO
from scrapper.http_weather_data_scrapper import HttpWeatherDataScrapper
from data_processor import WeatherDataProcessor, WeatherFieldExtractor, WeatherTemperatureFieldExtractor, TemperatureUnit, WeatherWindFieldExtractor, WindSpeedUnit
from data_processor.consumer import PandasConsumer

load_dotenv()

def load_cities() -> list[CityDTO]:
    """
    Parse the cities.json file and return a list of CityDTO objects
    """   
    cities = {}
    with open('./cities.json') as file:
        data = json.load(file)
        for city in data:
            cities[city['City']] = CityDTO(city['City'], city['Latitude'], city['Longitude'])
    return cities

def create_output_directory():
    if not os.path.exists("./output"):
        os.makedirs("./output")

def get_cities_from_args():
    # Load the cities from the cities.json file
    cityMap = load_cities()
    parser = argparse.ArgumentParser(description='Singular - Weather Application')
    parser.add_argument('--cities', type=str, help='List of cities separated by commas (e.g., London,Paris,New York). Allowed cities: ' + ', '.join([city for city in cityMap]))

    # Parse the command line arguments
    args = parser.parse_args()
    if not args.cities:
        print("No cities entered. Using default cities.")
        return cityMap.values()
    
    argsCities = args.cities.strip().split(',')
    cities = []
    for city in argsCities:
        if city not in cityMap:
            raise Exception(f"City '{city}' is not an allowed city")
        cities.append(cityMap[city])
    
    return cities


def main():
    """
    Main interactive loop for the weather application.
    """
    if not os.getenv('OPEN_METEO_API_URL'):
       raise Exception("OPEN_METEO_API_URL is not set")

    cities = get_cities_from_args()

    # Initialize the scrapper with the API URL
    scrapper = HttpWeatherDataScrapper(os.getenv('OPEN_METEO_API_URL'))

    # Initialize the weather data processor with the field extractors and consumers
    weatherDataProcessor = WeatherDataProcessor()
    pandasConsumer = PandasConsumer()

    weatherDataProcessor.with_field_extractor(WeatherFieldExtractor("Humidity (%)", "humidity", "relative_humidity_2m"))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature (C)", "temperature_celsius", "temperature_2m", TemperatureUnit.CELSIUS))
    weatherDataProcessor.with_field_extractor(WeatherTemperatureFieldExtractor("Temperature (F)", "temperature_fahrenheit", "temperature_2m", TemperatureUnit.FAHRENHEIT))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind (m/s)", "wind_mps", "wind_speed_10m", WindSpeedUnit.METERS_PER_SECOND))
    weatherDataProcessor.with_field_extractor(WeatherWindFieldExtractor("Wind (mph)", "wind_mph", "wind_speed_10m", WindSpeedUnit.MILES_PER_HOUR))

    weatherDataProcessor.with_consumer(pandasConsumer)

    # Get the current weather for each city using the Open Meteo API
    print("Fetching weather data...\n")
    cities_weather = scrapper.get_cities_current_weather(cities)

     # Process the weather data
    weatherDataProcessor.process(cities_weather)

    # Print the result
    pandasConsumer.print()
    print("\n")

    # Export the result to a CSV file
    create_output_directory()
    pandasConsumer.export_to_csv("./output/weather_data.csv")

    while True:
        print("1. Filter Weather Data")
        print("2. Rank Weather Data")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            print('filter_weather')
        elif choice == '2':
            print('rank_weather')
        elif choice == '3':
            print("Exiting application...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3. \n")

if __name__ == "__main__":
    main()
