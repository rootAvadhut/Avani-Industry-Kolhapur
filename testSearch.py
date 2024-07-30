import pandas as pd
import os

search_result = [{'Date': 'NA', 'Time': 'NA', 'BODY': 2406089, 'COVER': 'C0624120', '12T NB': '"2E24"', '12T WB': '"2E24"', '26T': '2D24', '28T': '"2E24"', 'LPM': 'NA', 'WP1': 'NA', 'BP1': 'NA', 'BP2': 'NA', 'Noise': 'NA', 'Box No': 'NA'}]

# Check if search_result is empty
if not search_result:
    print("No data found for the given search criteria.")
else:
    # Replace spaces with underscores in dictionary keys
    search_result_modified = []
    for d in search_result:
        modified_dict = {}
        for k, v in d.items():
            modified_dict[k.replace(' ', '_')] = v
        search_result_modified.append(modified_dict)

    # Create a DataFrame from the modified search_result list
    df = pd.DataFrame(search_result_modified)

    # Remove double quotes from specified columns
    for col in ['12T_NB', '12T_WB', '28T']:
        df[col] = df[col].astype(str).str.replace('"', '', regex=False)

    # Remove 'D' from the '26T' column
    df['26T'] = df['26T'].astype(str).str.replace('D', '', regex=False)

    # Create the 'temp' directory if it doesn't exist
    os.makedirs('temp', exist_ok=True)

    # Write the DataFrame to a CSV file
    df.to_csv('temp/search_one.csv', index=False)

    print("Data saved to temp/search_one.csv")
