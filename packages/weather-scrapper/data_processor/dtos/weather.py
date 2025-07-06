from dataclasses import dataclass

@dataclass
class Field:
    name: str
    key: str
    unit: str
    value: any

@dataclass
class CityWeather:
    name: str
    fields: list[Field]