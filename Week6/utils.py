import json
import pandas as pd
from datetime import datetime

def json_to_df(file_path):
    # Open the JSON file
    with open(file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)

    # Create a new dictionary with the desired format
    parsed_data = {}
    for key, value in data.items():
        parsed_data[key] = {}
        for inner_key, inner_value in value.items():
            parsed_data[key][inner_value['ISU_SRT_CD']] = int(inner_value['TDD_CLSPRC'].replace(',', ''))

    # Convert the new dictionary to a pandas DataFrame
    df = pd.DataFrame.from_dict(parsed_data, orient='index')

    # Convert the index to datetime format
    df.index = pd.to_datetime(df.index, format='%Y%m%d')

    # Return the DataFrame
    return df

# Test the function
if __name__ == '__main__':
    df = json_to_df('./fai/2023-FBA-quant-team3/Week6/fai_close_data.json')
    print(df.head())