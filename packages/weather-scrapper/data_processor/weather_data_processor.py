from scrapper.dtos.city import CityWeatherApiResponseDTO
from data_processor.dtos.weather import CityWeather

class WeatherDataProcessor:
    def __init__(self):
        self.fieldExtractors = []
        self.consumers = []

    def with_field_extractor(self, fieldExtractor):
        self.fieldExtractors.append(fieldExtractor)
        return self
    
    def with_consumer(self, consumer):
        self.consumers.append(consumer)
        return self
    
    def process(self, data: list[CityWeatherApiResponseDTO]):
        rows = []

        # Extract the fields from the data
        for entry in data:
            fields = []
            for fieldExtractor in self.fieldExtractors:
                fields.append(fieldExtractor.extract(entry))
            rows.append(CityWeather(entry.name, fields))

        # Consume the rows
        for consumer in self.consumers:
            consumer.consume(rows)
