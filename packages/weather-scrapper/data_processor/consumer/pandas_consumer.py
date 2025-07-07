import pandas as pd
from data_processor.dtos import CityWeather

class PandasConsumer:
    def consume(self, rows: list[CityWeather]):
        self.fields = {}
        df_data = {"City": []}
        for row in rows:
            df_data["City"].append(row.name) 
            for field in row.fields:
                if not field.name in self.fields:
                    self.fields[field.key] = field.name
                if not field.name in df_data:
                    df_data[field.name] = []

                df_data[field.name].append(field.value)

        self.df = pd.DataFrame(df_data)
    
    def get_fields(self):
        return self.fields.keys()
    
    def apply_filter(self, field_key: str, min_value: float, max_value: float):
        if not field_key in self.fields:
            raise Exception(f"Field '{field_key}' not found.")
        
        filtered_df = self.df[self.df[self.fields[field_key]].between(min_value, max_value)]

        if filtered_df.empty:
            print("No cities matched the specified filter criteria.\n")
            return
    
        print(filtered_df)

    def apply_ranking(self, field_key: str, order: str):
        if not field_key in self.fields:
            raise Exception(f"Field '{field_key}' not found.")
        
        is_ascending = True if order == 'asc' else False
        sorted_df = self.df.sort_values(by=[self.fields[field_key]], ascending=is_ascending)
        print(sorted_df)
    
    def print(self):
        print(self.df)
    
    def export_to_csv(self, file_path: str):
        self.df.to_csv(file_path, index=False)
    