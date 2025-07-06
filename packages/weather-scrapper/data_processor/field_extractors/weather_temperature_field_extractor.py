from enum import Enum
from .weather_field_extractor import WeatherFieldExtractor
from scrapper.dtos.city import CityWeatherApiResponseDTO
from data_processor.dtos.weather import Field

class TemperatureUnit(Enum):
    CELSIUS = "c"
    FAHRENHEIT = "f"

class WeatherTemperatureFieldExtractor(WeatherFieldExtractor):
    def __init__(self, field_name: str, field_key: str, data_key: str, unit: TemperatureUnit):
        super().__init__(field_name,field_key, data_key)
        self.unit = unit

    def extract(self, data: CityWeatherApiResponseDTO):
        unit = self.parse_unit(data.current_units[self.data_key])
        value = self.convert_to_temperature(data.current[self.data_key], unit, self.unit)

        return Field(self.field_name, self.field_key, self.unit.value, value)

    def parse_unit(self, unit: str):
        if TemperatureUnit.CELSIUS.value in unit.lower():
            return TemperatureUnit.CELSIUS
        elif TemperatureUnit.FAHRENHEIT.value in unit.lower():
            return TemperatureUnit.FAHRENHEIT
        else:
            raise Exception("Invalid unit")
        
    def convert_to_temperature(self, value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit):
        if from_unit == to_unit:
            return value
        
        if from_unit == TemperatureUnit.CELSIUS:
            if to_unit == TemperatureUnit.FAHRENHEIT:
                return (value * 9) / 5 + 32
            else:
                raise Exception("Invalid unit")
        elif from_unit == TemperatureUnit.FAHRENHEIT:
            if to_unit == TemperatureUnit.CELSIUS:
                return (value - 32) * 5 / 9
            else:
                raise Exception("Invalid unit")
        else:
            raise Exception("Invalid unit")