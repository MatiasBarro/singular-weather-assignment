from dataclasses import dataclass

@dataclass
class CityDTO:
    name: str
    latitude: float
    longitude: float