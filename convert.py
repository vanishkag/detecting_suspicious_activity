import pandas as pd

# Define column names
DATASET_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('sentiment140.csv', names=DATASET_COLUMNS)

# Convert the DataFrame to a JSON string
json_str = data.to_json(orient='records', lines=True)

# Write the JSON string to a file
with open('sentiment140.json', 'w') as f:
    f.write(json_str)

print("CSV file successfully converted to JSON with specified tags.")
