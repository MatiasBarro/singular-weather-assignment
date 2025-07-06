from enum import Enum
from .weather_field_extractor import WeatherFieldExtractor
from scrapper.dtos.city import CityWeatherApiResponseDTO
from data_processor.dtos.weather import Field

class WindSpeedUnit(Enum):
    METERS_PER_SECOND = "m/s"
    MILES_PER_HOUR = "miles/h"

class WeatherWindFieldExtractor(WeatherFieldExtractor):
    def __init__(self, field_name: str, field_key: str, data_key: str, unit: WindSpeedUnit):
        super().__init__(field_name,field_key, data_key)
        self.unit = unit

    def extract(self, data: CityWeatherApiResponseDTO):
        unit = self.parse_unit(data.current_units[self.data_key])
        value = self.convert_to_speed(data.current[self.data_key], unit, self.unit)

        return Field(self.field_name, self.field_key, self.unit.value, value)

    def parse_unit(self, unit: str):
        if WindSpeedUnit.METERS_PER_SECOND.value in unit.lower():
            return WindSpeedUnit.METERS_PER_SECOND
        elif WindSpeedUnit.MILES_PER_HOUR.value in unit.lower():
            return WindSpeedUnit.MILES_PER_HOUR
        else:
            raise Exception("Invalid unit")
        
    def convert_to_speed(self, value: float, from_unit: WindSpeedUnit, to_unit: WindSpeedUnit):
        if from_unit == to_unit:
            return value
        
        if from_unit == WindSpeedUnit.METERS_PER_SECOND:
            if to_unit == WindSpeedUnit.MILES_PER_HOUR:
                return (value * 3600) / 1609.34
            else:
                raise Exception("Invalid unit")
        elif from_unit == WindSpeedUnit.MILES_PER_HOUR:
            if to_unit == WindSpeedUnit.METERS_PER_SECOND:
                return (value * 1609.34) / 3600
            else:
                raise Exception("Invalid unit")
        else:
            raise Exception("Invalid unit")