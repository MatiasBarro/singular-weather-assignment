from data_processor.dtos.weather import Field
from scrapper.dtos.city import CityWeatherApiResponseDTO

class WeatherFieldExtractor:
    def __init__(self, field_name: str, field_key: str, data_key: str):
        self.field_name = field_name
        self.field_key = field_key
        self.data_key = data_key

    def extract(self, data: CityWeatherApiResponseDTO):
        unit = data.current_units[self.data_key]
        value = data.current[self.data_key]
        return Field(self.field_name, self.field_key, unit, value)