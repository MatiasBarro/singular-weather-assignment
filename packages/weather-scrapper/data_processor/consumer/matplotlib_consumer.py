import matplotlib.pyplot as plt
from data_processor.dtos import CityWeather

class MatPlotLibConsumer:
    def __init__(self):
        self.output_folder = 'output'

    def consume(self, rows: list[CityWeather]):
        # Get city names
        self.cities = [row.name for row in rows]
        # Get fields and values
        self.field_values = {}
        for row in rows:
            for field in row.fields:
                if field.key not in self.field_values:
                    self.field_values[field.key] = {'name': field.name, 'values': []}
                self.field_values[field.key]['values'].append(field.value)
    
    def plot(self):
        # Plot the data
        for field_key, field in self.field_values.items():
            plt.figure(figsize=(10, 5))
            plt.bar(self.cities, field['values'])
            plt.xlabel('City')
            plt.ylabel(field['name'])
            plt.title(f'Bar Chart for {field['name']}')
            plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a horizontal grid
            plt.tight_layout() # Adjust layout to prevent labels from overlapping
            plt.savefig(f'{self.output_folder}/{field_key}_plot.png', dpi=300, bbox_inches='tight')
        
        
