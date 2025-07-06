from dataclasses import dataclass
from dtos.city import CityDTO

@dataclass
class CityWeatherApiResponseDTO(CityDTO):
    current_units: dict
    current: dict
