import pandas as pd

# Read the CSV file
df = pd.read_csv('test_gear.xlsx - Sheet1.csv')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

# Remove quotes and spaces from columns with object datatype
for col in df.select_dtypes(include='object'):
    df[col] = df[col].astype(str).str.replace(r'[ "]+', '', regex=True)

# Convert the DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Print the list of dictionaries (ready for MongoDB insertion)
print(data_list)

