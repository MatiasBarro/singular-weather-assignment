from dataclasses import dataclass

@dataclass
class CityDTO:
    name: str
    latitude: float
    longitude: float


@dataclass
class CityWeatherApiResponseDTO(CityDTO):
    current_units: dict
    current: dict
