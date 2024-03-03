import pandas as pd

# Placeholder for the actual path to your VAERSSYMPTOMS.CSV file
file_path = './VAERSSymptoms.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Initialize an empty list to store the normalized data
normalized_data = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    vaers_id = row['VAERS_ID']
    # Loop through each symptom and its version
    for i in range(1, 6):  # Assuming up to 5 symptoms per VAERS_ID
        symptom = row.get(f'SYMPTOM{i}', '')
        version = row.get(f'SYMPTOMVERSION{i}', None)
        # Check if the symptom is non-empty
        if pd.notnull(symptom) and symptom != '':
            # Append a new row to the normalized_data list
            normalized_data.append({
                'VAERS_ID': vaers_id,
                'SYMPTOM': symptom,
                'SYMPTOMVERSION': version
            })

# Create a new DataFrame from the normalized data
normalized_df = pd.DataFrame(normalized_data)

# Optionally, save the normalized DataFrame to a new CSV file
normalized_df.to_csv('normalized_vaerssymptoms.csv', index=False)

