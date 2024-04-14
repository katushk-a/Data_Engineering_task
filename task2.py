import pandas as pd
from datetime import datetime
import os

saturday_data = 'data_2023-02-11.csv'
sunday_data = 'data_2023-02-12.csv'

def concatenate_dates(dates):
    return ' and '.join(dates.unique())

def combine_csv_files(saturday, sunday, output_filepath):
    try:
        saturday_data = pd.read_csv(saturday, delimiter=';')
        sunday_data = pd.read_csv(sunday, delimiter=';')
        combined_data = pd.concat([saturday_data, sunday_data])
        #i assumed that same id-s should not be twice in the file, and that the result should be aggregated properly
        #if 2 files need to be just simply combined, then the next expression is not needed
        combined_data = combined_data.groupby(['metric_id', 'metric_desc'], as_index=False).agg({
            'metric_value' : 'sum',
            'metric_date': concatenate_dates
        })
        combined_data['file_generation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_file_path = os.path.join(output_filepath, 'data_2023_02_11-12.csv')
        combined_data.to_csv(output_file_path, index=False)   
        return output_file_path
    except Exception as e:
        return str(e)

combine_csv_files(saturday_data, sunday_data, 'result_dataset')