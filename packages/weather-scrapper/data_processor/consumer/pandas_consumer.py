import pandas as pd
from data_processor.dtos import CityWeather

class PandasConsumer:
    def consume(self, rows: list[CityWeather]):
        df_data = {"City": []}
        for row in rows:
            df_data["City"].append(row.name) 
            for field in row.fields:
                if not field.name in df_data:
                    df_data[field.name] = []

                df_data[field.name].append(field.value)

        self.df = pd.DataFrame(df_data)
    
    def print(self):
        print(self.df)
    
    def export_to_csv(self, file_path: str):
        self.df.to_csv(file_path, index=False)
    