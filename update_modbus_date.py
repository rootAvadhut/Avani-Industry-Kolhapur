from pymongo import MongoClient
from db_connection import get_db_collection

def update_mongodb(data_list):
    """
    Updates the MongoDB collection with values from the data_list based on the BODY field.
    
    Parameters:
    data_list (list): A list containing 'Date', 'Time', 'BODY', 'COVER', 'LPM', 'WP1', 'BP1', 'BP2', 'Noise'.
    """
    # Connect to the MongoDB collection
    collection = get_db_collection()
    
    # Extract values from data_list
    date_str = data_list[0]
    time_str = data_list[1]
    body = data_list[2]
    cover = data_list[3]  # This is still in the list but not used for filtering
    lpm = data_list[4]
    wp1 = data_list[5]
    bp1 = data_list[6]
    bp2 = data_list[7]
    noise = data_list[8]
    
    # Create an update document with the new values
    update_document = {
        'Date': date_str,
        'Time': time_str,
        'LPM': lpm,
        'WP1': wp1,
        'BP1': bp1,
        'BP2': bp2,
        'Noise': noise
    }
    
    # Update the document in MongoDB based on BODY
    result = collection.update_one(
        {'BODY': body},   # Filter by BODY only
        {'$set': update_document},  # Update fields
        upsert=False      # Only update existing documents
    )
    
    if result.matched_count > 0:
        print(f"Document with BODY {body} updated successfully.")
    else:
        print(f"No document found with BODY {body}.")

# Sample data_list

# Sample data_list
data_list = [
    '2024-09-04',  # Date
    '07:58',  # Time
   2406089,  # BODY
   2406089,  # COVER
    724311,  # LPM
    74.26,  # WP1
    257,  # BP1
    333,  # BP2
    335  # Noise
]

# Call the function with the provided data_list
update_mongodb(data_list)


