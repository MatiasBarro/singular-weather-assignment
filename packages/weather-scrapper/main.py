import os
import argparse
from dotenv import load_dotenv
from dtos.city import CityDTO
from api import CityNinjaApi
from scrapper.http_weather_data_scrapper import HttpWeatherDataScrapper
from data_processor import WeatherDataProcessor, WeatherFieldExtractor, WeatherTemperatureFieldExtractor, TemperatureUnit, WeatherWindFieldExtractor, WindSpeedUnit
from data_processor.consumer import PandasConsumer

load_dotenv()


def create_output_directory():
    if not os.path.exists("./output"):
        os.makedirs("./output")

def get_cities_from_args() -> list[CityDTO]:
    parser = argparse.ArgumentParser(description='Singular - Weather Application')
    parser.add_argument('--cities', type=str, help='List of cities separated by commas (e.g., London,Paris,New York)')

    cityApi = CityNinjaApi(os.getenv('API_NINJA_CITY_API_URL'), os.getenv('API_NINJA_CITY_API_KEY'))
    
    # Parse the command line arguments
    args = parser.parse_args()
    if not args.cities:
        print("No cities entered. Using default cities.")
        return list(cityApi.get_pre_loaded_cities().values())
    
    argsCities = args.cities.strip().split(',')
    print('Fetching cities...\n')
    cities = cityApi.fetch_cities(argsCities)
    
    return cities

def filter_weather(pandas_consumer: PandasConsumer):
    """
    Interactively prompts the user for filter criteria and applies them.
    """

    print("\n--- Filter Weather Data ---\n")
    available_fields = pandas_consumer.get_fields()
    
    field_filter = input(f"Enter field to filter by (available: {','.join(available_fields)}): ").strip()

    if not field_filter or field_filter not in available_fields:
        print("Invalid field. Please enter a valid field.\n")
        return

    filter_range = input(f"Enter range for {field_filter} (e.g., 10-25): ").strip()
    min_value, max_value = [float(part.strip()) for part in filter_range.split('-')] 
    if not min_value or not max_value or max_value < min_value:
        print("Invalid range. Please enter a valid range.\n")
        return
    
    pandas_consumer.apply_filter(field_filter, min_value, max_value)
    print('\n------------------------------\n')

def rank_cities(pandas_consumer: PandasConsumer):
    """
    Interactively prompts the user for ranking criteria and ranks the data.
    """
    print("\n--- Rank Weather Data ---\n")
    available_fields = pandas_consumer.get_fields()
    rank_field = input(f"Enter fields to rank by (available: {','.join(available_fields)}): ").strip()
    if not rank_field or rank_field not in available_fields:
        print("Invalid field. Please enter a valid field.\n")
        return

    order = input("Order (asc for ascending, desc for descending): ").strip().lower()
    if order not in ['asc', 'desc']:
        print("Invalid order. Please enter 'asc' or 'desc'.\n")
        return
    
    print(f"Ranking cities by '{rank_field}' in {order}ending order...")
    pandas_consumer.apply_ranking(rank_field, order)
    print('\n------------------------------\n')

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

    # Export the result to a CSV file
    create_output_directory()
    pandasConsumer.export_to_csv("./output/weather_data.csv")

    # Print the result
    pandasConsumer.print()

    while True:
        print("\n")
        print("1. Show Weather Data")
        print("2. Filter Weather Data")
        print("3. Rank Weather Data")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            pandasConsumer.print()
        elif choice == '2':
            filter_weather(pandasConsumer)
        elif choice == '3':
            rank_cities(pandasConsumer)
        elif choice == '4':
            print("Exiting application...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4. \n")

if __name__ == "__main__":
    main()
