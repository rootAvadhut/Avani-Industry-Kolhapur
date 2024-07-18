import pandas as pd
from pymongo import MongoClient
import os
def search_body_no(body_number):
    """
    Search MongoDB for a specific BODY number and return selected columns.
    
    Parameters:
    - body_number (str): The BODY number to search for.
    
    Returns:
    - result (list of dicts): List of dictionaries containing the selected columns.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['avani_test']
    collection = db['test']
    
    # Query MongoDB for the specified BODY number
    query = {'BODY': body_number}
    projection = {
        'Date': 1, 'Time': 1, 'BODY': 1, 'COVER': 1, '12T NB': 1, 
        '12T WB': 1, '26T': 1, '28T': 1, 'LPM': 1, 'WP1': 1, 
        'BP1': 1, 'BP2': 1, 'Noise': 1, 'Box No': 1, '_id': 0
    }
    
    # Execute the query
    result = list(collection.find(query, projection))
    
    return result

# Example usage:
body_number = 2406148  # Replace with the BODY number you want to search for
columns_to_return = [
    'Date', 'Time', 'BODY', 'COVER', '12T NB', '12T WB', '26T', 
    '28T', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise', 'Box No'
]


# Call the function
search_result = search_body_no(body_number)



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



